from constants import *
from error import *
import re

#####################################################################
## Token Object
#####################################################################
class Token:
    def __init__(self, type, line, col, value = None):
        self.value = value
        self.type = type
        self.line = line
        self.col = col

    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
    

#####################################################################
## Lexer Object
#####################################################################
class Lexer:
    def __init__(self, text):
        self.text = text
        self.curr_char = None
        self.line = 1
        self.col = 0
        self.index = -1
        self.text_len = len(self.text)


    #####################################################################
    ## next_char method - progresses self.curr_char to the next char in 
    ## the text while also updating the line and col variable to the 
    ## appropriate values
    #####################################################################
    def next_char(self):
        self.col += 1
        self.index += 1
        self.curr_char = self.text[self.index] if self.index < self.text_len else None

        if self.curr_char == '\n':
            self.line += 1
            self.col = 0
            self.next_char()

    #####################################################################
    ## check_indentation method - checks and creates a TAB token 
    #####################################################################
    def check_indentation(self):
        space_counter = 0
        tab_tokens = []
        start_col = self.col
        start_line = self.line
        while self.curr_char == ' ':
            space_counter += 1
            self.next_char()

            if self.curr_char == '\n' or self.curr_char == None:
                return []
            
            if space_counter == 4:
                tab_tokens.append(Token(TAB_T, start_line, start_col))
                space_counter = 0
                start_col = self.col
        return tab_tokens


    #####################################################################
    ## num_token method - creates a number token
    #####################################################################
    def num_token(self):
        num = ''
        start_col = self.col
        start_line = self.line
        while self.curr_char != None and self.curr_char in NUMS:
            num += self.curr_char
            self.next_char()
        return Token(INT_T, start_line, start_col, int(num))
    
    #####################################################################
    ## alpha_token method - creates alpha-numberical tokens which can 
    ## be keywords or identifiers
    #####################################################################
    def alpha_token(self):
        word = ''
        start_col = self.col
        start_line = self.line
        while self.curr_char != None and re.match(ALPHANUMERAL, self.curr_char):
            word += self.curr_char
            self.next_char()
        
        if word in KEYWORS:
            if KEYWORS[word] == 'IF' and self.curr_char == ' ' and (self.text[self.index + 1: self.index + 4] == ELIF):
                for _ in range(4):
                    self.next_char()
                return Token(KEYWORD_T, start_line, start_col, 'ELIF')
            elif KEYWORS[word] == 'WHILE_1' and self.curr_char == ' ' and (self.text[self.index + 1: self.index + 4] == WHILE):
                for _ in range(4):
                    self.next_char()
                return Token(KEYWORD_T, start_line, start_col, 'WHILE')
            else:
                return Token(KEYWORD_T, start_line, start_col, KEYWORS[word])
        else:
            return Token(IDENTIFIER_T, start_line, start_col, word)

    #####################################################################
    ## lexer method - tokenizes self.text into a list or Token objects 
    ## or return an Illegal character Error object.
    #####################################################################
    def lexer(self):
        self.next_char()

        tokens = []

        while self.curr_char != None:
            if self.curr_char == ' ':
                tab_tokens = self.check_indentation()
                tokens += tab_tokens
            elif self.curr_char == '\t':
                tokens.append(Token(TAB_T, self.line, self.col))
            elif self.curr_char in NUMS:
                tokens.append(self.num_token())
            elif re.match(ALPHANUMERAL, self.curr_char):
                tokens.append(self.alpha_token())
            elif self.curr_char == '=':
                tokens.append(Token(EQUAL_T, self.line, self.col))
                self.next_char()
            elif self.curr_char == '+':
                tokens.append(Token(PLUS_T, self.line, self.col))
                self.next_char()
            elif self.curr_char == '-':
                tokens.append(Token(MINUS_T, self.line, self.col))
                self.next_char()
            elif self.curr_char == '*':
                tokens.append(Token(MULT_T, self.line, self.col))
                self.next_char()
            elif self.curr_char == '/':
                tokens.append(Token(DIVIDE_T, self.line, self.col))
                self.next_char()
            elif self.curr_char == '(':
                tokens.append(Token(LPARAM_T, self.line, self.col))
                self.next_char()
            elif self.curr_char == ')':
                tokens.append(Token(RPARAM_T, self.line, self.col))
                self.next_char()
            elif self.curr_char == '^':
                tokens.append(Token(POWER_T, self.line, self.col))
                self.next_char()
            else:
                return [], IllegalCharacterError(self.line, self.col, self.curr_char)
       
        tokens.append(Token(EOF_T, self.line, self.col))
        return tokens, None
                    

                        




