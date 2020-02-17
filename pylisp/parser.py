import operator
from collections import deque

SEPARATOR = " "

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
            sexp.add(parse(tokens))
        assert tokens.popleft() == ")"
        return sexp
    elif token == ")":
        raise SyntaxError("Unexpected ")
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
        }
        values = [sexp.eval(env) for sexp in self.sexps]
        print("program values:", values)
        return values[-1]


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

    def eval(self, env=None):
        if isinstance(self.x, str) and self.x in env:
            return env[self.x]
        return self.x

    def __repr__(self):
        return str(self.x)

    def __str__(self):
        return str(self.x)


class List:
    def __init__(self):
        self.x = []

    def add(self, y):
        self.x.append(y)

    def __repr__(self):
        return "(List " + " ".join(map(repr, self.x)) + ")"

    def __str__(self):
        return " ".join(map(str, self.x))

    def eval(self, env=None):
        values = [component.eval(env) for component in self.x]
        print("values:", values)
        return values[-1](*values[:-1])
