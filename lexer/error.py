from constants import *

class Error:
    def __init__(self, line, col, type, details):
        self.line = line
        self.col = col
        self.type = type
        self.details = details

    def msg_as_string(self):
        return f'{self.type}: መስመር {self.line} ላይ: {self.col}ኛው ካራክተ \n => "{self.details}"'
    
class IllegalCharacterError(Error):
    def __init__(self, line, col, details):
        super().__init__(line, col, ILLEGAL_CHARACTER_ERROR, details + ' ፤')

class IllegalSyntaxError(Error):
    def __init__(self, line, col, details):
        super().__init__(line, col, ILLEGAL_SYNTAX_ERROR, details)

class RTError(Error):
    def __init__(self, line, col, details, context):
        super().__init__(line, col, RUNTIME_ERROR, details)
        self.context = context

    def msg_as_string(self):
        return f'{self.generate_traceback()} \n {self.type}: መስመር {self.line} ላይ: {self.col}ኛው ካራክተ \n => "{self.details}"'
    
    def generate_traceback(self):
        result = ''
        line = self.line
        context = self.context

        while context:
            result = f' መስመር {str(line)} ላይ {context.name}\n' + result
            line = context.parent_line
            context = context.parent

        return 'Traceback (most recent call last):\n' + result


        