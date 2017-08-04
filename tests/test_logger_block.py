from unittest.mock import MagicMock, call
from ..logger_block import Logger
from nio.testing.block_test_case import NIOBlockTestCase
from nio import Signal
import logging


class TestLogger(NIOBlockTestCase):

    def test_logger_not_enabled(self):
        blk = Logger()
        self.configure_block(blk, {
            'name': 'loggerblock',
            'log_level': 'INFO',
            'log_at': 'DEBUG',
        })
        self.assertFalse(blk.logger.isEnabledFor(
            getattr(logging, blk.log_at().name)))

    def test_logger_enabled(self):
        blk = Logger()
        self.configure_block(blk, {
            'name': 'loggerblock',
            'log_level': 'DEBUG',
            'log_at': 'INFO',
        })
        self.assertTrue(blk.logger.isEnabledFor(
            getattr(logging, blk.log_at().name)))

    def test_logger_equal(self):
        blk = Logger()
        self.configure_block(blk, {
            'name': 'loggerblock',
            'log_level': 'DEBUG',
            'log_at': 'DEBUG',
        })
        self.assertTrue(blk.logger.isEnabledFor(
            getattr(logging, blk.log_at().name)))

    def test_default_process_signals(self):
        blk = Logger()
        self.configure_block(blk, {})
        blk.logger = MagicMock()
        signal = Signal({"I <3": "n.io"})
        blk.process_signals([signal])
        blk.logger.info.assert_called_once_with(signal.to_dict())
        self.assertEqual(blk.logger.error.call_count, 0)

    def test_list_process_signals(self):
        blk = Logger()
        self.configure_block(blk, {})
        blk.logger = MagicMock()
        signal = Signal({"I <3": "n.io"})
        blk.process_signals([signal, signal])
        blk.logger.info.assert_has_calls([
            call(signal.to_dict()),
            call(signal.to_dict()),
        ])
        self.assertEqual(blk.logger.error.call_count, 0)

    def test_exception_on_logging(self):
        blk = Logger()
        self.configure_block(blk, {})
        blk.logger = MagicMock()
        blk.logger.info.side_effect = Exception()
        signal = Signal({"I <3": "n.io"})
        blk.process_signals([signal])
        blk.logger.info.assert_called_once_with(signal.to_dict())
        blk.logger.exception.assert_called_once_with("Failed to log signal")

    def test_list_logging(self):
        blk = Logger()
        self.configure_block(blk, {"log_as_list": True})
        blk.logger = MagicMock()
        signal = Signal({"I <3": "n.io"})
        blk.process_signals([signal, signal])
        blk.logger.info.assert_called_once_with([
            signal.to_dict(),
            signal.to_dict(),
        ])
        self.assertEqual(blk.logger.error.call_count, 0)
