import unittest
from pylisp.parser import Program


class TestEval(unittest.TestCase):
    def test_arithmetics(self):
        self.assertEqual(3, Program("(1 2 +)").eval())
        self.assertEqual(76, Program("(1 (100 25 -) +)").eval())
        self.assertEqual(True, Program("(1 1 eq?)").eval())
        self.assertEqual(False, Program("(1 0 eq?)").eval())

    def test_define(self):
        self.assertEqual(5, Program("(a 5 define) a").eval())
        self.assertEqual(False, Program("(a 5 define) (a 7 eq?)").eval())
        self.assertEqual(True, Program("(a 5 define) (a 5 eq?)").eval())
