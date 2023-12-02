from resources.constants import *

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
        Returns a string with the snippit of the code where the error occured with an 
        arrow pointing to the specific location of the error.
        
        Note: a snipit of code is one line of code.
        """
        snippit = '------------------------------------------------------------\n'
        snippit += f'\n\t{self.line}: {self.text}\n'
        arrow_index = ' ' * (self.col + len(str(self.line)) + 1)
        snippit += f'\t{arrow_index}\u2191\n'
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
    """ An error if the program includes a character that is not recognized. """
    def __init__(self, line, col, details):
        super().__init__(line, col, ILLEGAL_CHARACTER_ERROR, details, "")


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
        Returns an error message as a string for an indentation error.
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
    """ An error if the program structure doesn't follow the defined grammer."""
    def __init__(self, line, col, details):
        if details in (RPARAM_MISSING_ERROR, RBRACKET_MISSING_ERROR): col += 1
        super().__init__(line, col, ILLEGAL_SYNTAX_ERROR, details)

# =======================================================================================
# =======================================================================================
class RTError(Error):
    """ 
    An error that occurs while running the program. It can happen when type rules are
    broken or undefined identifiers are accesed.
    """
    def __init__(self, line, col, details, context, extra_info = None):
        super().__init__(line, col, RUNTIME_ERROR, details, '')
        self.context = context
        self.extra_info = extra_info

    def msg_as_string(self):
        """
        Returns an error message as a string for a runtime error.
        """
        result = f'{self.type} መስመር {self.line} ላይ: {self.col}ኛው ካራክተ ላይ\n'
        result += f'{self.code_snippit()}\n'
        if self.details == ILLEGAL_OPERATION:
            (args, op) = self.extra_info
            type_ = None
            type_extracted = None
            if isinstance(args, tuple):
                (x, self_) = args
                type_ = self.type_of(x)
                other_type = self.type_of(self_)
                if other_type and type_:
                    result += f'{other_type} እና {type_}ን {op} አይቻልም።'
                else:
                    result += f'እዚህ ላይ ያለው {op} አይፈቅድም።'
            else:
                type_extracted = self.type_of(args)
                if type_extracted:
                    result += f'{type_extracted} {op}ን አይፈቅድም።'
                else:
                    result += f'እዚህ ላይ ያለው {op} አይፈቅድም።'
        else:
            return result + f'"{self.details}"' 
        return result + f'\n\n{self.generate_traceback()}\n'
    
    def generate_traceback(self):
        """
        Generates function call traceback to be shown alomg the error message.
        """
        result = ''
        result = f'\n\t\t \u2193 \t {self.context.name} ውስጥ {self.details}\n' + result
        line = self.line
        context = self.context

        while context:
            result = f' መስመር {str(line)} ላይ {context.name}\n' + result
            name = context.name
            line = context.parent_line
            context = context.parent
            if context:
                result = f'\n\t\t \u2193 \t {context.name} {name}ን ጠራ\n\n' + result          
        result = '------------------------------------------------------------\n' + result
        result = ' የጥሪ መልሶ ምልከታ ፦ \n' + result
        result = '------------------------------------------------------------\n' + result
        return result

    def type_of(self, obj):
        """
        Returns the type of obj in Amharic text.
        """
        type_ = type(obj)
        type_extracted = None
        if str(type_) == "<class 'type.String'>":
            type_extracted = 'ፅሁፍ'
        elif str(type_) == "<class 'type.Number'>":
            type_extracted = 'ቁጥር'
        elif str(type_) == "<class 'type.Array'>":
            type_extracted = 'ስብስብ'
        elif str(type_) == "<class 'type.Class'>":
            type_extracted = 'ክላስ'
        elif str(type_) == "<class 'type.Object'>":
            type_extracted = 'ኦብጀክት'
        elif str(type_) == "<class 'type.Function'>":
            type_extracted = 'ፋንክሽን'
        return type_extracted
