import operator
from collections import Iterable
from collections import deque

SEPARATOR = " "
KW_ATOM = "atom?"
KW_QUOTE = "quote"
KW_DEFINE = "define"


def tokenize(s):
    """
    We rely on " " to identify each token. For the open and close parentheses,
    simply surround each with a " ".
    """
    return deque(s.replace("(", " ( ").replace(")", " ) ").split())


def parse(tokens):
    token = tokens.popleft()
    if token == "(":
        sexp = List()
        while tokens[0] != ")":
            sexp.append(parse(tokens))
            if not tokens:
                raise SyntaxError("Missing )")
        assert tokens.popleft() == ")"
        return sexp
    elif token == ")":
        raise SyntaxError("Unexpected )")
    else:
        return Atom(token)


class Program:
    """
    Essentially a list of S-expressions.
    """
    def __init__(self, s):
        self.sexps = []
        if not s:
            raise SyntaxError("Empty program")
        tokens = tokenize(s)

        while tokens:
            self.sexps.append(parse(tokens))

    def __repr__(self):
        return "\n".join(map(repr, self.sexps))

    def __str__(self):
        return "\n".join(map(str, self.sexps))

    def eval(self):
        env = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "eq?": operator.eq,  # is_
            "car": lambda x: x[0],
            "cdr": lambda x: List(x[1:]),
            "cons": lambda x, y: List([x] + y) if isinstance(y, List) else List([x] + [y]),
        }
        values = [sexp.eval(env) for sexp in self.sexps]
        print("program values:", values)
        return str(values[-1])


class Atom:
    def __init__(self, token):
        self.x = None
        try:
            self.x = int(token)
        except ValueError:
            try:
                self.x = float(token)
            except ValueError:
                self.x = token

    def __repr__(self):
        return str(self.x)

    def __str__(self):
        return str(self.x)

    def eval(self, env=None):
        if isinstance(self.x, str) and self.x in env:
            return env[self.x]
        return self.x


class List(list):
    def __repr__(self):
        return "(List " + " ".join(map(repr, self)) + ")"

    def __str__(self):
        return f'\'({" ".join(map(str, self))})'

    def eval(self, env=None):
        args = self[:-1]
        op = self[-1].eval(env)
        print("op:", op)
        if op == KW_QUOTE:
            assert len(args) == 1
            return args[0]
        elif op == KW_ATOM:
            assert len(args) == 1
            return isinstance(args[0], Atom) or not isinstance(args[0].eval(env), list)
        elif op == KW_DEFINE:
            assert len(args) == 2
            env[args[0].eval(env)] = args[1].eval(env)
            return None

        values = [item.eval(env) for item in self[:-1]]
        print("values:", values)
        return op(*values)
