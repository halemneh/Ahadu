from lexer import Lexer
from parser_ import Parser
from interpreter import *

import pdb

with open("sample.txt") as file:
    text = file.read()

global_symbol_table = SymbolTable(None)


tokens, error = Lexer(text).lexer()
text = text.split('\n')

if error == None:

    # print("####################################################")
    # print("##                 Lexer Result                  ###")
    # print("####################################################")

    # for i in range(len(tokens)):
    #     print(tokens[i])

    # print("####################################################")
    # print("##                 Parser Result                 ###")
    # print("####################################################")

    #pdb.set_trace()
    ast, err = Parser(tokens, text).parse()

    if err:
        err.text = text[err.line - 1]
        print(err.msg_as_string())
    else:
        print(ast)
        print("####################################################")
        print("##               Interprter Result               ###")
        print("####################################################")

        interpter = Interpreter()
        context = Context("ዋና ፕሮግራም")
        context.symbol_table = global_symbol_table
        
        
        rt, err = interpter.visit(ast, context)
        # print(global_symbol_table.symbols)
        if err:
            err.text = text[err.line - 1]
            print(err.msg_as_string())
        # else:
        #     print(rt)
    
else:
    error.text = text[error.line - 1]
    print(error.msg_as_string())