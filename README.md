# Basic postfix Lisp interpreter

Support:
```
+
-
*
/
eq?
atom?
define
lambda
cons
car
cdr
cond
quote
```

Sample usage:
```
Program("(plus-one ((x) (x 1 +) lambda) define)"
        "(2 plus-one)").eval()
# output: "3"
```

REPL: (`python repl.py`)

```
> (1 2 +)
3
> (1 2 -)
-1
> (3 (1 2 +) eq?)
True
> (arr (3 4 cons) define)
> (arr car)
3
> (arr cdr)
'(4)
> (foofunc ((x y) ((x 1 -) y *) lambda) define)
> (5 3 foofunc)
12
> (3 5 foofunc)
10
> (a 2 define)
> (((1 a eq?) one) ((2 a eq?) two) ((3 a eq?) three) (else nope) cond)
two
```

Note: an s-expression can be either an atom or a list.

## Setup (development environment)

Run locally in a standard Python 3 virtual enviroment:

- Create environment
```
$ virtualenv -p /usr/bin/python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

- Run all tests

```
$ python -m pytest tests/
```

## Run REPL

```
$ python repl.py
```

## References

Ideas and chunks of code come from:

- http://norvig.com/lispy.html
- http://pythonpracticeprojects.com/lisp.html
