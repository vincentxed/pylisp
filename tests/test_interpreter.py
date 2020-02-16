import unittest
from pylisp.interpreter import Interpreter


class TestEval(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    @unittest.expectedFailure
    def test_simple(self):
        self.assertEqual('3', self.interpreter.eval('(1 2 +)'))
