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
from pylisper.interpreter.ast_walk import AstWalkEvaluator
from pylisper.interpreter.env import STD_ENV, Env
from pylisper.interpreter.exceptions import EvaluationError
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
        self.eval = AstWalkEvaluator(env)
        # TODO: setup autocompletion and a history file
        # TODO: for the readline

    def runcode(self, code):
        "stub for the new object model"
        raise NotImplementedError

    def runsource(self, source, ignored_filename="<input>", symbol="single"):
        """
        Evaluates input source.

        Instead of the default implementation uses `AstWalkEvaluator`
        to evaluate the source and then prints the result
        to the console.
        """
        try:
            ast = parser.parse(lexer.lex(source))
            res = ast.accept(self.eval)
        except pylisper.parser.IncompleteInput:
            return True
        except UnexpectedCharacter as e:
            self.print_error(e)
            self.write(source.split("\n")[e.line - 1])
            return False
        except (EvaluationError, LexingError) as e:
            self.print_error(e)
            return False
        # TODO: to be replaced with self.runcode later on
        self.write(res)
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
