import subprocess
import sys
import unittest
from unittest.mock import patch

import dev


class DevTests(unittest.TestCase):
    def test_dead_process_is_not_reported_ready(self):
        process = subprocess.Popen([sys.executable, "-c", "pass"], start_new_session=True)
        process.wait()
        with patch.object(dev, "healthy", return_value=True):
            with self.assertRaisesRegex(RuntimeError, "завершился"):
                dev.wait_ready(process, "http://unused")

    def test_readiness_waits_for_success(self):
        process = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"],
                                   start_new_session=True)
        try:
            with patch.object(dev, "healthy", side_effect=[False, True]) as probe:
                dev.wait_ready(process, "http://unused", timeout=3)
                self.assertEqual(probe.call_count, 2)
        finally:
            dev.stop(process)
        self.assertIsNotNone(process.poll())

    def test_unready_service_times_out(self):
        process = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"],
                                   start_new_session=True)
        try:
            with patch.object(dev, "healthy", return_value=False):
                with self.assertRaisesRegex(RuntimeError, "не готов"):
                    dev.wait_ready(process, "http://unused", timeout=0.1)
        finally:
            dev.stop(process)

    def test_busy_port_is_not_taken_over(self):
        with patch.object(dev.socket.socket, "connect_ex", return_value=0):
            with self.assertRaisesRegex(RuntimeError, "3000 занят"):
                dev.check_ports()
