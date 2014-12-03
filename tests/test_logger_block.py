from os import path, remove
from datetime import datetime
from ..logger_block import LoggerBlock
from nio.util.attribute_dict import AttributeDict
from nio.util.support.block_test_case import NIOBlockTestCase
from nio.modules.logging import LoggingModule
from nio.modules.logging.factory import LoggerFactory
from nio.configuration.settings import Settings


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
        self.now = datetime.utcnow()
        LoggerFactory._configuration['prefix'] = 'loggertest'
        self.log_filename = "loggertest.log"

    def tearDown(self):
        super().tearDown()
        if path.isfile(self.log_filename):
            remove(self.log_filename)

    def test_logger_block(self):
        logger = LoggerBlock()
        self.configure_block(logger, {
            'name': 'loggerblock',
            'log_level': 'DEBUG',
            'log_at': 'DEBUG'
        })

        logger.start()

        signals = ['signal1', 'signal2']

        logger.process_signals(signals)

        self.assertTrue(path.isfile(self.log_filename))
        with open(self.log_filename, 'r') as log:
            log_data = log.read()
            self.assertTrue('signal1' in log_data)
            self.assertTrue('signal2' in log_data)

        # logger block should not notify any signals
        self.assert_num_signals_notified(0)
