from nio.common.block.base import Block
from nio.common.command import command
from nio.common.command.params.string import StringParameter
from nio.metadata.properties import SelectProperty
from nio.modules.logging.logger import LogLevel
from nio.common.discovery import Discoverable, DiscoverableType


@command("log", StringParameter("phrase", default='Default phrase'))
@Discoverable(DiscoverableType.block)
class LoggerBlock(Block):

    """ Logger block.

    A NIO block for logging arbitrary signals.

    """

    log_level = SelectProperty(LogLevel, title="Log Level", default="INFO")
    log_at = SelectProperty(LogLevel, title="Log At", default="INFO")

    def process_signals(self, signals):
        """ Overridden from the block interface.

        When an instance of LoggerBlock is in the receivers list for some
        other block, this method allows the sending block to deliver its
        outgoing signal object to the logger, which logs them individually.

        Args:
            signals (list of Signal): a list of signals to be logged.

        Returns:
            None
        """
        log_func = self._get_logger()
        print(log_func)
        print(self._logger)
        print(self._logger.name)
        for s in signals:
            log_func(s)

    def _get_logger(self):
        """ Returns a function that can log, based on the current config.

        This will return a different log level function based on what this
        block is configured to log at.
        """
        if isinstance(self.log_at, LogLevel):
            log_str = self.log_at.name.lower()
        else:
            log_str = str(self.log_at).lower()

        return getattr(self._logger, log_str, self._logger.error)

    def log(self, phrase="None provided"):
        self._get_logger()("Command log called with phrase: {0}".format(phrase))
