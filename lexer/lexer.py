from constants import *

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
        if self.value: return f'{self.type}:{self.value}:{self.line}:{self.col}'
        return f'{self.type}:{self.line}:{self.col}'
    


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
    ## next_char Function - progresses self.curr_char to the next char in 
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
    ## check_indentation Function - checks and creates a TAB token 
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
    ## num_token Function - creates a number token
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
    ## Lexer Function
    ## @param filepath - the path of the file to be tokenized
    ## @return a list the tokens from the file specified at filepath and 
    ## an error or None if there were no errors.
    #####################################################################
    def lexer(self):
        self.next_char()

        tokens = []

        while self.curr_char != None:
            if self.curr_char in ' \t':
                self.next_char()
            elif self.curr_char in NUMS:
                tokens.append(self.num_token())
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
            else:
                print("Error: Unknown Character at line " + str(self.line) + " and col " + str(self.col))
                self.next_char()

        return tokens
                    

                        




