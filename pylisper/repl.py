"""
Can be run as module to start a pylispers repl.

Contains `PylisperConsole` class which is a subclass
of `code.InteractiveConsole`.
"""
import code
import readline
import sys

from rply.errors import LexingError

import pylisper
from pylisper.interpreter.compiler import ObjectCompiler
from pylisper.interpreter.env import Env
from pylisper.interpreter.evaluator import Evaluator
from pylisper.interpreter.exceptions import EvaluationError
from pylisper.interpreter.std_env import STD_ENV
from pylisper.lexer import lexer
from pylisper.parser import UnexpectedCharacter, parser


class PylisperConsole(code.InteractiveConsole):
    """
    An interactive console for the repl.

    Closely modeled after after pypy's 3.6 `PyPyConsole`.
    `code.InteractiveConnsole` class is written in python 2
    however that is the best we can get from pythons std lib
    without writing our own console.
    """

    def __init__(self, env=None):
        super().__init__()
        if env is None:
            env = Env(STD_ENV)
        self.env = env
        self.eval = Evaluator(env)
        self.comp = ObjectCompiler()
        # TODO: setup autocompletion and a history file
        # TODO: for the readline

    def runcode(self, code):
        try:
            res = self.eval.eval(code)
        except EvaluationError as e:
            self.print_error(e)
        res = "()" if res is None else res
        self.write(res)

    def runsource(self, source, ignored_filename="<input>", symbol="single"):
        """
        Evaluates input source.

        Instead of the default implementation uses `AstWalkEvaluator`
        to evaluate the source and then prints the result
        to the console.
        """
        try:
            ast = parser.parse(lexer.lex(source))
            code = ast.accept(self.comp)
        except pylisper.parser.IncompleteInput:
            return True
        except UnexpectedCharacter as e:
            self.print_error(e)
            self.write(source.split("\n")[e.line - 1])
            return False
        except LexingError as e:
            # TODO: do something about lexing errors
            self.print_error(e)
            return False
        self.runcode(code)
        return False

    def interact(self):
        banner = (
            f"Pylisper {pylisper.__version__} on top of Pythons"
            f" {sys.version.split()[0]}"
        )
        exit_msg = "Exiting..."
        super().interact(banner, exit_msg)

    def write(self, msg):
        print(msg)

    def print_error(self, err):
        print(err)


def main():
    PylisperConsole().interact()


if __name__ == "__main__":
    main()
