from unittest.mock import MagicMock
from ..logger_block import LoggerBlock
from nio.util.attribute_dict import AttributeDict
from nioext.util.support.block_test_case import NIOExtBlockTestCase
from nio.common.signal.base import Signal
from nio.modules.logging import LoggingModule
from nio.modules.logging.factory import LoggerFactory
from nio.configuration.settings import Settings
import logging


class LoggerConfiguration(AttributeDict):

    def __init__(self):
        super().__init__()
        self['logging'] = AttributeDict({
            'handlers': {
                'flat_file': {
                    'level': 'DEBUG',
                    'class': ('nioext.modules.logging.flat_file.'
                              'file_handler.NIOFileHandler'),
                    'formatter': 'default',
                    'filename': 'loggertest'
                }
            },
            'root': {
                'handlers': ['flat_file'],
                'level': 'DEBUG'
            },
            'loggers': {
                'loggerblock': {
                    'level': 'DEBUG'
                },
            }
        })


class TestLoggerBlock(NIOExtBlockTestCase):

    def setUp(self):
        super().setUp()
        Settings.clear()
        LoggingModule.module_init(LoggerConfiguration()['logging'],
                                  self.get_module_locations())
        LoggerFactory._configuration['prefix'] = 'loggertest'


    def test_logger_not_enabled(self):
        blk = LoggerBlock()
        self.configure_block(blk, {
            'name': 'loggerblock',
            'log_level': 'INFO',
            'log_at': 'DEBUG'
        })
        self.assertFalse(blk._logger.isEnabledFor(
            getattr(logging, blk.log_at.name))
        )

    def test_logger_enabled(self):
        blk = LoggerBlock()
        self.configure_block(blk, {
            'name': 'loggerblock',
            'log_level': 'DEBUG',
            'log_at': 'INFO'
        })
        self.assertTrue(blk._logger.isEnabledFor(
            getattr(logging, blk.log_at.name))
        )

    def test_logger_equal(self):
        blk = LoggerBlock()
        self.configure_block(blk, {
            'name': 'loggerblock',
            'log_level': 'DEBUG',
            'log_at': 'DEBUG'
        })
        self.assertTrue(blk._logger.isEnabledFor(
            getattr(logging, blk.log_at.name))
        )

    def test_default_process_signals(self):
        blk = LoggerBlock()
        self.configure_block(blk, {})
        blk._logger = MagicMock()
        signal = Signal({"I <3": "n.io"})
        blk.process_signals([signal])
        blk._logger.info.assert_called_once_with(signal)
        self.assertEqual(blk._logger.error.call_count, 0)

    def test_exception_on_logging(self):
        blk = LoggerBlock()
        self.configure_block(blk, {})
        blk._logger = MagicMock()
        blk._logger.info.side_effect = Exception()
        signal = Signal({"I <3": "n.io"})
        blk.process_signals([signal])
        blk._logger.info.assert_called_once_with(signal)
        self.assertEqual(blk._logger.error.call_count, 1)
