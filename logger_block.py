from nio import Block
from nio.command import command
from nio.command.params.string import StringParameter
from nio.properties import SelectProperty
from nio.util.logging.levels import LogLevel
from nio.util.discovery import discoverable


@command("log", StringParameter("phrase", default='Default phrase'))
@discoverable
class Logger(Block):

    """ Logger block.

    A NIO block for logging arbitrary signals.

    """

    log_level = SelectProperty(LogLevel, title="Log Level", default="INFO")
    log_at = SelectProperty(LogLevel, title="Log At", default="INFO")

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
        for s in signals:
            try:
                log_func(s)
            except:
                self.logger.error("Failed to log signal")

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
