from resources.constants import *
from resources.error import *
import re

# =======================================================================================
# =======================================================================================
class Token:
    def __init__(self, type, line, col, value = None):
        self.value = value
        self.type = type
        self.line = line
        self.col = col

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
    
    def match(self, type, value = None):
        """
        Returns True if token has the given type and value.
        """
        return self.type == type and self.value == value

# =======================================================================================
# =======================================================================================  
class Lexer:
    def __init__(self, text):
        self.text = text
        self.curr_char = None
        self.line = 1
        self.col = 0
        self.index = -1
        self.text_len = len(self.text)

    def next_char(self):
        """ 
        Progresses self.curr_char to the next char in the text while also updating the 
        line and col variable to the appropriate values. 
        """
        self.col += 1
        self.index += 1

        if self.index < self.text_len:
            self.curr_char = self.text[self.index]
        else:
            self.curr_char = None

        if self.curr_char == '\n':
            self.line += 1
            self.col = 0

    def check_indentation(self):
        """
        Returns a list of TAB_T tokens if they exist starting at curr_token or an error 
        if there is an indentation error. A tab is defined as a \t character or four 
        consecutive space characters that apear at a start of line. At a start of line, 
        there can be more than more tabs hence why the method returns a list.
        """
        tabs = []
        space_counter = 0
        start_col = self.col
        start_line = self.line

        if start_col != 1: 
            """ Any space or tab not on the start of line is ignored """
            while self.curr_char != None and self.curr_char in ' \t':
                self.next_char()
            return [], None

        while self.curr_char != None and self.curr_char in ' \t':
            if self.curr_char == '\t':
                tabs.append(Token(TAB_T, start_line, start_col))
                self.next_char()
                start_col = self.col

                if self.curr_char == '\n' or self.curr_char == None:
                    return [], None
            else:
                space_counter += 1
                self.next_char()

                if self.curr_char == '\n' or self.curr_char == None:
                    return [], None
                
                if space_counter == 4:
                    tabs.append(Token(TAB_T, start_line, start_col))
                    space_counter = 0
                    start_col = self.col

        if space_counter:
            return [], IndentationError(start_line, start_col + 1, -1)
        return tabs, None

    def num_token(self):
        """
        Returns a number token.
        """
        num = ''
        dot = False
        start_col = self.col
        start_line = self.line
        while self.curr_char != None and (
                self.curr_char in NUMS or (self.curr_char == '.' and not dot)):
            if self.curr_char == '.':
                dot = True
            num += self.curr_char
            self.next_char()
        if dot:
            return Token(INT_T, start_line, start_col, float(num))
        return Token(INT_T, start_line, start_col, int(num))
    
    def alpha_token(self):
        """
        Returns a keyword token is the word is in the keyword list. Otherwise, returns an 
        identifier token.
        """
        word = ''
        start_col = self.col
        start_line = self.line

        if self.curr_char == '\u12e8':
            self.next_char()
            return Token(OF_T, start_line, start_col)
        
        while self.curr_char != None and re.match(ALPHANUMERAL, 
                                                  self.curr_char):
            word += self.curr_char
            self.next_char()
        
        if word in KEYWORS:
            if KEYWORS[word] == WHILE_T and self.curr_char == ' ' and (
                self.text[self.index + 1: self.index + 4] == WHILE):
                for _ in range(4):
                    self.next_char()
                return Token(KEYWORD_T, start_line, start_col, WHILE_T)
            else:
                return Token(KEYWORD_T, start_line, start_col, KEYWORS[word])
        else:
            return Token(IDENTIFIER_T, start_line, start_col, word)
        
    def check_equal(self):
        """
        Returns an EQ_T token if the equal sign is followed by another equal sign or an 
        EQUAL_T token otherwise.
        """
        start_line = self.line
        start_col = self.col
        self.next_char()
        if self.curr_char == '=':
            self.next_char()
            return Token(EQ_T, start_line, start_col)
        return Token(EQUAL_T, start_line, start_col)
    
    def check_greater_than(self):
        """
        Returns an GTE_T token if the greater than sign is followed by an equal sign or 
        an GT_T token otherwise.
        """
        start_line = self.line
        start_col = self.col
        self.next_char()
        if self.curr_char == '=':
            self.next_char()
            return Token(GTE_T, start_line, start_col)
        return Token(GT_T, start_line, start_col)
    
    def check_less_than(self):
        """
        Returns an LTE_T token if the less than sign is followed by an equal sign or an 
        LT_T token otherwise.
        """
        start_line = self.line
        start_col = self.col
        self.next_char()
        if self.curr_char == '=':
            self.next_char()
            return Token(LTE_T, start_line, start_col)
        return Token(LT_T, start_line, start_col)
    
    def check_negation(self):
        """
        Returns an NEQ_T token if the exclaimtion sign is followed by an eqaul sign or an 
        KEYWORD_T:NOT token otherwise.
        """
        start_line = self.line
        start_col = self.col
        self.next_char()
        if self.curr_char == '=':
            self.next_char()
            return Token(NEQ_T, start_line, start_col)
        return Token(KEYWORD_T, start_line, start_col, NOT_T)
    
    def check_then(self):
        """
        Returns a Token of type then if ':' is folloed by '-' or a colon token if it is 
        not.
        """
        start_line = self.line
        start_col = self.col
        self.next_char()
        if self.curr_char == '-':
            self.next_char()
            return Token(THEN_T, start_line, start_col)
        return Token(COLON_T, start_line, start_col)
    
    def check_string(self):
        """
        Creates a string token for a string literal.
        """
        start_line = self.line
        start_col = self.col
        curr_col = start_col + 1

        string = ''
        escape = False
        quote = "'" if self.curr_char == "'" else '"'
        self.next_char()

        while self.curr_char != None and (self.curr_char != quote or escape):
            if self.curr_char == '\n' or self.curr_char == '\r' or (
                self.curr_char == '\r\n'):
                return None, IllegalCharacterError(self.line - 1, curr_col, 
                                                   INCOMPELTE_STR)
            if escape:
                string += ESCAPE.get(self.curr_char, self.curr_char)
                escape = False
            else:
                if self.curr_char == '\\':
                    escape = True
                else:
                    string += self.curr_char
            curr_col += 1
            self.next_char()
        self.next_char()
        return Token(STRING_T, start_line, start_col, string), None
    
    def comment_line(self):
        """
        Removes a line of comment
        """
        while self.curr_char != '\n' and self.curr_char != '\r' and (
                self.curr_char != '\r\n'):
            self.next_char()
        self.next_char()
    
    def lexer(self):
        """
        Returns a list of tokens from self.text and an IllegalCharacter error if it 
        exists (unknown character exists).
        """
        self.next_char()

        tokens = []

        while self.curr_char != None:
            if self.curr_char == '#':
                self.comment_line()
            elif self.curr_char == '\n':
                tokens.append(Token(NEWLINE_T, self.line, self.col))
                self.next_char()
            elif self.curr_char == '\r\n':
                tokens.append(Token(NEWLINE_T, self.line, self.col))
                self.next_char()
            elif self.curr_char == '\r':
                tokens.append(Token(NEWLINE_T, self.line, self.col))
                self.next_char()
            elif self.curr_char in ' \t':
                tab_tokens, err = self.check_indentation()
                if err:
                    return [], err
                tokens += tab_tokens
            elif self.curr_char == '"' or self.curr_char == "'":
                str, error = self.check_string()
                if error: return None, error
                tokens.append(str)
            elif self.curr_char in NUMS:
                tokens.append(self.num_token())
            elif re.match(ALPHANUMERAL, self.curr_char):
                tokens.append(self.alpha_token())
            elif self.curr_char == '=':
                tokens.append(self.check_equal())
            elif self.curr_char in '>\u203a':
                tokens.append(self.check_greater_than())
            elif self.curr_char in '<\u2039':
                tokens.append(self.check_less_than())
            elif self.curr_char == '!':
                tokens.append(self.check_negation())
            elif self.curr_char == '&':
                tokens.append(Token(KEYWORD_T, self.line, self.col, AND_T))
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
            elif self.curr_char == '[':
                tokens.append(Token(LBRACKET_T, self.line, self.col))
                self.next_char()
            elif self.curr_char == ']':
                tokens.append(Token(RBRACKET_T, self.line, self.col))
                self.next_char()
            elif self.curr_char == '^':
                tokens.append(Token(POWER_T, self.line, self.col))
                self.next_char()
            elif self.curr_char == ',':
                tokens.append(Token(COMMA_T, self.line, self.col))
                self.next_char()
            elif self.curr_char == '\u1363':
                tokens.append(Token(COMMA_T, self.line, self.col))
                self.next_char()
            elif self.curr_char == '.':
                tokens.append(Token(DOT_T, self.line, self.col))
                self.next_char()
            elif self.curr_char in ':\u1361':
                tokens.append(self.check_then())
            elif self.curr_char == '\u1366':
                tokens.append(Token(THEN_T, self.line, self.col))
                self.next_char()
            else:
                return [], IllegalCharacterError(self.line, self.col, self.curr_char)
            
        tokens.append(Token(EOF_T, self.line, self.col))
        return tokens, None
    
# =======================================================================================
# =======================================================================================