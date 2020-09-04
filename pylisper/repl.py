from parser import parser

from interpreter.ast_walk import AstWalkEvaluator, Env
from lexer import lexer


def main():
    env = Env()
    eval = AstWalkEvaluator(env)
    while True:
        print(">>>", end=" ")
        expr = input()
        try:
            ast = parser.parse(lexer.lex(expr))
            # print(ast)
            # if isinstance(ast, List):
            #     for expr in ast:
            #         print(expr)
            print(ast.accept(eval))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
