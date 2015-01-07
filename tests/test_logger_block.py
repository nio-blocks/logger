from os import path, remove
from datetime import datetime
from ..logger_block import LoggerBlock
from nio.util.attribute_dict import AttributeDict
from nio.util.support.block_test_case import NIOBlockTestCase
from nio.modules.logging import LoggingModule
from nio.modules.logging.factory import LoggerFactory
from nio.configuration.settings import Settings
from nio.modules.threading import Event
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


class TestLoggerBlock(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        Settings.clear()
        LoggingModule.module_init(LoggerConfiguration()['logging'])
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
