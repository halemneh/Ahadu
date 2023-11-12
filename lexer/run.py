from lexer import Lexer
from parser import Parser
from interpreter import *

with open("sample.txt") as file:
    text = file.read()

tokens, error = Lexer(text).lexer()

if error == None:

    print("####################################################")
    print("##                 Lexer Result                  ###")
    print("####################################################")

    for i in range(len(tokens)):
        print(tokens[i])

    print("####################################################")
    print("##                 Parser Result                 ###")
    print("####################################################")

    ast = Parser(tokens).parse()

    if ast.error:
        print(ast.error.msg_as_string())
    else:
        print(ast.node)
        
        interpter = Interpreter()
        context = Context("ዋና ፕሮግራም")
        rt = interpter.visit(ast.node, context)

        if rt.error:
            print(rt.error.msg_as_string())
        else:
            print(rt.value)
    
else:
    print(error.msg_as_string())