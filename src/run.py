from lexer import Lexer
from parser_ import Parser
from interpreter import *
from type import *
from constants import RUNTIME_ERROR
import sys
import pdb

def run(text):
    text_split = text.split('\n')

    """ Lexing """
    tokens, error = Lexer(text).lexer()
    if error: 
        error.text = text_split[error.line - 1]
        return None, error
    
    """ Parsing """
    ast, error = Parser(tokens).parse()
    if error: 
        error.text = text_split[error.line - 1]
        return None, error
    
    """ Interpreting """
    global_symbol_table = SymbolTable(None)
    context = Context("ዋና ፕሮግራም")
    context.symbol_table = global_symbol_table

    return_val, error = Interpreter().visit(ast, context)
    if error: 
        error.text = text_split[error.line - 1]

    return return_val, error

def htmlify(val, error):
    html = '<html><head><link rel="stylesheet" href="frame.css"></head><body>'
    if error:
        if error.type != RUNTIME_ERROR:
            error_msg = error.msg_as_string().split('\n')
            html += '<div class="error_container"><p class = "header">'
            html += error_msg[0]
            html += '</p><p class = "code">'
            html += f'{error_msg[1]}</endl>'
            html += f'{error_msg[2]}</endl>'
            html += f'{error_msg[3]}</endl>'
            if len(error_msg) > 4:
                html += '</p><p class = "more">'
                html += error_msg[-1]
            html += '</p></div>'
    else:
        pass
    html += f'</body>'


    return html


""" RUN """
f = open('out.text', 'w')
sys.stdout = f

if len(sys.argv) < 2:
    print("Error: filepath not passed!")
elif len(sys.argv) > 2:
    print("Error: More than 1 arguments passed!")
file_name = sys.argv[1]

with open(file_name) as file:
    text = file.read()

val, error = run(text)
if error:
    f.write(error.msg_as_string())
# elif val != Number(0):
#     f.write(str(val))
        
