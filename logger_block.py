from nio.block.base import Block
from nio.command import command
from nio.command.params.string import StringParameter
from nio.properties import SelectProperty, BoolProperty
from nio.util.logging.levels import LogLevel


@command("log", StringParameter("phrase", default='Default phrase'))
class Logger(Block):

    """ Logger block.

    A NIO block for logging arbitrary signals.

    """

    # this is overidden here to change the default log_level from the base
    # block
    log_level = SelectProperty(LogLevel, title="Log Level", default="INFO")
    log_at = SelectProperty(LogLevel, title="Log At", default="INFO")
    log_as_list = BoolProperty(title="Log as a list",
                               default=False, visible=False)

    def process_signals(self, signals):
        """ Overridden from the block interface.

        When an instance of Logger is in the receivers list for some
        other block, this method allows the sending block to deliver its
        outgoing signal object to the logger, which logs them individually.

        Args:
            signals (list of Signal): a list of signals to be logged.

        Returns:
            None
        """
        log_func = self._get_logger()

        try:
            logged = 0
            if self.log_as_list():
                log_func([signal.to_dict() for signal in signals])
            else:
                for s in signals:
                    log_func(s.to_dict())
                    logged += 1
        except:
            self.logger.exception("Failed to log {} signals"
                                  .format(len(signals) - logged if logged else
                                          len(signals)))

    def _get_logger(self):
        """ Returns a function that can log, based on the current config.

        This will return a different log level function based on what this
        block is configured to log at.
        """
        if isinstance(self.log_at(), LogLevel):
            log_str = self.log_at().name.lower()
        else:
            log_str = str(self.log_at()).lower()

        return getattr(self.logger, log_str, self.logger.error)

    def log(self, phrase="None provided"):
        self._get_logger()("Command log called with phrase: {0}".format(phrase))
