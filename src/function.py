from error import *
from type import *

class DefaultFunction(DefaultType):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return f'[Function: {self.name}]'

    def check_args(self, args_from_def, args_from_call, func_context):
        """
        
        """
        if len(args_from_call) < len(args_from_def):
            return RTError(args_from_call.line, args_from_call.col, 
                                 "Too few args", self.context)
        elif len(args_from_call) > len(args_from_def):
            return RTError(args_from_call.line, args_from_call.col, 
                                 "Too many args", self.context)
        
        for i in range(len(args_from_call)):
            func_context.symbol_table.set(args_from_def[i].value, (
                args_from_call[i].set_context(func_context)))
            
        return None
    

###############################################################################
###############################################################################

class Function(DefaultFunction):
    def __init__(self, name, args, body, return_present):
        super().__init__(name)
        self.args = args
        self.body = body
        self.should_return = return_present   

    def run(self, args, interpreter, func_context):
        """
        
        """
        print(f'{self.name}: {str(func_context.symbol_table.symbols)}')
        error = self.check_args(self.args, args, func_context)
        print(f'{self.name}: {str(func_context.symbol_table.symbols)}')
        if error: return None, error

        value, error = interpreter.visit(self.body, func_context)
        if error: return None, error

        print(f'Body = {value}')
        if not self.should_return:
            value = None

        print(f'Value = {value}')
        return value, None