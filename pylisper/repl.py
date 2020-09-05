from pylisper.interpreter.ast_walk import AstWalkEvaluator
from pylisper.interpreter.env import STD_ENV, Env
from pylisper.interpreter.exceptions import EvaluationError
from pylisper.lexer import lexer
from pylisper.parser import parser


def main():
    env = Env(STD_ENV)
    eval = AstWalkEvaluator(env)
    while True:
        print(">>>", end=" ")
        expr = input()
        try:
            ast = parser.parse(lexer.lex(expr))
            print(ast.accept(eval))
        except EvaluationError as e:
            print(f"error: {e}")


if __name__ == "__main__":
    main()
