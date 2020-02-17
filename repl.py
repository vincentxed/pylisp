from pylisp.parser import Program

PROMPT = '> '


def run():
    program = Program(repl_mode=True)
    while True:
        output = program.add_and_run_statement(input(PROMPT))
        if output != "None":
            print(output)


if __name__ == '__main__':
    run()
