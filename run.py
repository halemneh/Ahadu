from src.lexer import Lexer
from src.parser_ import Parser
from src.interpreter import *
from resources.type import *
from resources.constants import RUNTIME_ERROR

import argparse
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
    html = ''
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

def main():
    parser = argparse.ArgumentParser(description='Run Ahadu code')
    parser.add_argument('filepath', help='Ahadu filepath')
    args = parser.parse_args()
    with open(args.filepath) as file:
        text = file.read()
    val, error = run(text)
    if error:
        print(error.msg_as_string())

    
if __name__ == '__main__':
    main()
    