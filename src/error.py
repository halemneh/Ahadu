from constants import *

# =======================================================================================
# =======================================================================================
class Error:
    def __init__(self, line, col, type, extra_info, text = None):
        self.line = line
        self.col = col
        self.type = type
        self.text = text
        self.details = extra_info

    def code_snippit(self):
        """
        Returns a string with the snippit of the code where the error occured
        with an arrow pointing to the specific location of the error.
        Note: a snipit of code is one line of code.
        """
        snippit = ''
        snippit += f'\n\t{self.line}: {self.text}\n'
        arrow_index = ' ' * (self.col + len(str(self.line)) + 1)
        snippit += f'\t{arrow_index}\u2191'
        return snippit

    def msg_as_string(self):
        """
        Returns an error message as a string.
        """
        result = f'{self.type}: መስመር {self.line} ላይ: {self.col}ኛው ካራክተ '
        result += f'\u2192 "{self.details}" \n{self.code_snippit()}'
        return result


# =======================================================================================
# =======================================================================================
class IllegalCharacterError(Error):
    def __init__(self, line, col, text, details):
        super().__init__(line, col, ILLEGAL_CHARACTER_ERROR, text, details)


# =======================================================================================
# =======================================================================================
class IndentationError(Error):
    """
    Note: One indentation is a tab or four spaces.
    """
    def __init__(self, line, col, indent_expected):
        super().__init__(line, col - 1, INDENTATION_ERROR, '')
        self.indent = indent_expected

    def msg_as_string(self):
        """
        Returns an error message as a string for an indentation error
        """
        
        result = f'{self.type}: መስመር {self.line} ላይ: {self.col}ኛው ካራክተ \n'
        result += f'{self.code_snippit()}\n'
        if self.indent == -1:
            result += f'Indentaions have to be a tab or four spaces!'
        else:
            result += f'More indentation than expected. Expected {self.indent} indents!'
        return result


# =======================================================================================
# =======================================================================================
class IllegalSyntaxError(Error):
    def __init__(self, line, col, details):
        if details in (RPARAM_MISSING_ERROR, RBRACKET_MISSING_ERROR): col += 1
        super().__init__(line, col, ILLEGAL_SYNTAX_ERROR, details)

# =======================================================================================
# =======================================================================================
class RTError(Error):
    def __init__(self, line, col, details, context, extra_info = None):
        super().__init__(line, col, RUNTIME_ERROR, details, '')
        self.context = context
        self.extra_info = extra_info

    def msg_as_string(self):
        result = f'{self.generate_traceback()}\n'
        result += f'{self.type}: መስመር {self.line} ላይ: {self.col}ኛው ካራክተ ላይ\n'
        result += f'{self.code_snippit()}\n'
        if self.details == ILLEGAL_OPERATION:
            (obj, op) = self.extra_info
            result += f'{obj} doesnot allow {op}'
        else:
            return result + f'"{self.details}"' 
        return result
    
    def generate_traceback(self):
        result = ''
        line = self.line
        context = self.context

        while context:
            result = f' መስመር {str(line)} ላይ {context.name}\n' + result
            line = context.parent_line
            context = context.parent

        return 'Traceback (most recent call last):\n' + result


        