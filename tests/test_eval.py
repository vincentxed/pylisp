import unittest
from pylisp.parser import Program


class TestEval(unittest.TestCase):
    def test_arithmetics(self):
        self.assertEqual("3", Program("(1 2 +)").eval())
        self.assertEqual("76", Program("(1 (100 25 -) +)").eval())
        self.assertEqual("True", Program("(1 1 eq?)").eval())
        self.assertEqual("False", Program("(1 0 eq?)").eval())

    def test_define(self):
        self.assertEqual("5", Program("(a 5 define) a").eval())
        self.assertEqual("False", Program("(a 5 define) (a 7 eq?)").eval())
        self.assertEqual("True", Program("(a 5 define) (a 5 eq?)").eval())

    def test_list_manip(self):
        self.assertEqual("'(3 4)", Program("(3 4 cons)").eval())
        self.assertEqual("'(5 3 4)", Program("(5 (3 4 cons) cons)").eval())
        self.assertEqual("3", Program("(arr (3 4 cons) define) (arr car)").eval())
        self.assertEqual("'(4)", Program("(arr (3 4 cons) define) (arr cdr)").eval())
        self.assertEqual("'(3 4)", Program("(arr (5 (3 4 cons) cons) define) (arr cdr)").eval())

    @unittest.expectedFailure
    def test_list_parsing(self):
        self.assertEqual("'(3 4)", Program("(arr '(5 3 4) define) (arr cdr)").eval())

    def test_quote(self):
        self.assertEqual("a", Program("(a quote)").eval())

    def test_atom(self):
        self.assertEqual("True", Program("(2 atom?)").eval())
        self.assertEqual("True", Program("(a atom?)").eval())
        self.assertEqual("True", Program("((3 4 +) atom?)").eval())
        self.assertEqual("False", Program("((3 4 cons) atom?)").eval())

    def test_lambda(self):
        self.assertEqual("3", Program("(plus-one ((x) (x 1 +) lambda) define) (2 plus-one)").eval())
        self.assertEqual("12", Program("(5 3 ((x y) ((x 1 -) y *) lambda))").eval())
        self.assertEqual("10", Program("(3 5 ((x y) ((x 1 -) y *) lambda))").eval())

    def test_cond(self):
        self.assertEqual("two",
                         Program("(a 2 define)"
                                 "(((1 a eq?) one) ((2 a eq?) two) ((3 a eq?) three) (nope else) cond)").eval())
        self.assertEqual("nope",
                         Program("(a whatev define)"
                                 "(((1 a eq?) one) ((2 a eq?) two) ((3 a eq?) three) (else nope) cond)").eval())
