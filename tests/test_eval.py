import unittest
from pylisp.parser import Program


class TestEval(unittest.TestCase):
    def _test_output(self, output, program):
        self.assertEqual(output, program.eval())

    def test_arithmetic(self):
        self._test_output("3", Program("(1 2 +)"))
        self._test_output("76", Program("(1 (100 25 -) +)"))
        self._test_output("True", Program("(1 1 eq?)"))
        self._test_output("False", Program("(1 0 eq?)"))

    def test_define(self):
        self._test_output("5", Program("(a 5 define) a"))
        self._test_output("False", Program("(a 5 define) (a 7 eq?)"))
        self._test_output("True", Program("(a 5 define) (a 5 eq?)"))

    def test_list_manip(self):
        self._test_output("'(3 4)", Program("(3 4 cons)"))
        self._test_output("'(5 3 4)", Program("(5 (3 4 cons) cons)"))
        self._test_output("3", Program("(arr (3 4 cons) define) (arr car)"))
        self._test_output("'(4)", Program("(arr (3 4 cons) define) (arr cdr)"))
        self._test_output("'(3 4)", Program("(arr (5 (3 4 cons) cons) define) (arr cdr)"))

    @unittest.expectedFailure  # Unimplemented
    def test_list_parsing(self):
        self._test_output("'(3 4)", Program("(arr '(5 3 4) define) (arr cdr)"))

    def test_quote(self):
        self._test_output("a", Program("(a quote)"))

    def test_atom(self):
        self._test_output("True", Program("(2 atom?)"))
        self._test_output("True", Program("(a atom?)"))
        self._test_output("True", Program("((3 4 +) atom?)"))
        self._test_output("False", Program("((3 4 cons) atom?)"))

    def test_lambda(self):
        self._test_output("3", Program("(plus-one ((x) (x 1 +) lambda) define) (2 plus-one)"))
        self._test_output("12", Program("(5 3 ((x y) ((x 1 -) y *) lambda))"))
        self._test_output("10", Program("(3 5 ((x y) ((x 1 -) y *) lambda))"))

    def test_cond(self):
        self._test_output("two",
                          Program("(a 2 define)"
                                  "(((1 a eq?) one) ((2 a eq?) two) ((3 a eq?) three) (t nope) cond)"))
        self._test_output("nope",
                          Program("(a whatev define)"
                                  "(((1 a eq?) one) ((2 a eq?) two) ((3 a eq?) three) (t nope) cond)"))

    def test_fibonacci(self):
        """
        (defun fibo (x)
          (cond
            ((< x 2) x)
            (t (+ (fibo (- x 1)) (fibo (- x 2))))))
        """
        self._test_output("55", Program("(fibo ((x) (((x 2 <) x) (t (((x 1 -) fibo) ((x 2 -) fibo) +)) cond) lambda)"
                                        " define)"
                                        "(10 fibo)"))

    def test_arithmetic(self):
        self._test_output("10", Program("(1 2 3 4 +)"))
        self._test_output("-8", Program("(1 2 3 4 -)"))
        self._test_output("24", Program("(1 2 3 4 *)"))
        self._test_output("0.125", Program("(1 2 4 /)"))

