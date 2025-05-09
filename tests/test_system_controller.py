
from controller import SystemController
from data_model import *
import unittest


class TestTransaction(unittest.TestCase):
    def test_system_controller_init(self):
        controller = SystemController()
        assert controller.system is not None


if __name__ == '__main__':
    unittest.main()