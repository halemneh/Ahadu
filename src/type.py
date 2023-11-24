from error import RTError
from constants import ILLEGAL_OPERATION, INDEX_OUT_OF_BOUNDS, DIVISION_BY_ZERO_ERROR, NO_OF_ARGS_PASSED
import copy

class DefaultType:
    def __init__(self):
        self.set_position()
        self.set_context()

    def set_context(self, context = None):
        """
        Set the context of the defaultType.
        """
        self.context = context
        return self
    
    def set_position(self, line = None, col = None):
        """
        Set the position, line and column, of the defaultType.
        """
        self.line = line
        self.col = col
        return self
    
    def copy():
        return None
    
    def add(self, x):
        """
        Returns an error since the defaultType doen't allow addition.
        """
        return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                             ((x, self), "መደመር"))
    
    def subtract(self, x):
        """
        Returns an error since the defaultType doen't allow subtraction.
        """
        return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                             ((x, self), "መቀነስ"))
    
    def multiply(self, x):
        """
        Returns an error since the defaultType doen't allow multiplication.
        """
        return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                             ((x, self), "ማባዛት"))
    
    def divide(self, x):
        """
        Returns an error since the defaultType doen't allow division.
        """
        return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                             ((x, self), "ማካፈል"))
    
    def power(self, x):
        """
        Returns an error since the defaultType doen't allow exponential.
        """
        return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                             ((x, self), "ፓወር"))
    
    def lt(self, x):
        """
        Returns an error since the defaultType doen't allow less than comparison.
        """
        return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                             ((x, self), "ማወዳደር"))
    
    def lte(self, x):
        """
        Returns an error since the defaultType doen't allow less than or equal to 
        comparison.
        """
        return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                             ((x, self), "ማወዳደር"))
    
    def gt(self, x):
        """
        Returns an error since the defaultType doen't allow greater than comparison.
        """
        return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                             ((x, self), "ማወዳደር"))
    
    def gte(self, x):
        """
        Returns an error since the defaultType doen't allow greater than or equal to 
        comparison.
        """
        return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                             ((x, self), "ማወዳደር"))

    def eq(self, x):
        """
        Returns an error since the defaultType doen't allow equal to comparison.
        """
        return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                             ((x, self), "ማወዳደር"))
    
    def neq(self, x):
        """
        Returns an error since the defaultType doen't allow not equal to comparison.
        """
        return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                             ((x, self), "ማወዳደር"))     

    def or_(self, x):
        """
        Returns an error since the defaultType doen't allow or combinator.
        """
        return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                             ((x, self), "ማወዳደር"))
    
    def and_(self, x):
        """
        Returns an error since the defaultType doen't allow and combinator.
        """
        return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                             ((x, self), "ማወዳደር"))
    
    def at(self, x):
        """
        Returns an error since the defaultType doen't allow indexing.
        """
        return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                             ((x, self), "indexing"))
    
    def slice(self, start, end):
        """
        Returns an error since the defaultType doen't allow slicing.
        """
        return None, RTError(start.line, start.col, ILLEGAL_OPERATION , self.context, 
                             ((self), "slicing"))
    
    def not_(self):
        """
        Returns an error since the defaultType doen't allow negation.
        """
        return None, RTError(self.line, self.col, ILLEGAL_OPERATION , self.context, 
                             ((self), "negating"))
    
    def run(self, args, interpreter, func_context, line, col):
        """
        Returns an error since the defaultType doen't allow execution.
        """
        return None, RTError(args.line, args.col, ILLEGAL_OPERATION , self.context,
                             ((self), "excuting"))
    
    def dot(self, args):
        """
        Returns an error since the defaultType doen't allow execution.
        """
        return None, RTError(args.line, args.col, ILLEGAL_OPERATION , self.context,
                             ((self), "dot"))
    
    def true(self):
        """
        Returns False since the defaultType represents False.
        """
        return False
    
# =======================================================================================
# =======================================================================================

class Number(DefaultType):
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def __repr__(self):
        return str(self.value)
    
    
    def add(self, x):
        """
        Return self + x
        """
        if isinstance(x, Number):
            return Number(self.value + x.value).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION , self.context, 
                                 ((x, self), "መደመር"))
        
    def subtract(self, x):
        """
        Return self - x
        """
        if isinstance(x, Number):
            return Number(self.value - x.value).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION , self.context, 
                                 ((x, self), "መቀነስ"))
        
    def multiply(self, x):
        """
        Return self * x
        """
        if isinstance(x, Number):
            return Number(self.value * x.value).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION , self.context, 
                                 ((x, self), "ማባዛት"))
    
    def divide(self, x):
        """
        Return self / x
        """
        if isinstance(x, Number):
            if x.value == 0:
                return None, RTError(x.line, x.col, DIVISION_BY_ZERO_ERROR, self.context)
            return Number(self.value / x.value).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION , self.context,
                                 ((x, self), "ማካፈል"))
        
    def power(self, x):
        """
        Return self ^ x
        """
        if isinstance(x, Number):
            return Number(self.value ** x.value).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION , self.context,
                                 ((x, self), "ፓወር"))
        
    def lt(self, x):
        """
        Return 1 if self is less than x or 0 xwise.
        """
        if isinstance(x, Number):
            return Number(int(self.value < x.value)).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION , self.context,
                                 ((x, self), "ማወዳደር"))
        
    def lte(self, x):
        """
        Return 1 if self is less than or equal to x or 0 xwise.
        """
        if isinstance(x, Number):
            return Number(int(self.value <= x.value)).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION , self.context,
                                 ((x, self), "ማወዳደር"))
        
    def gt(self, x):
        """
        Return 1 if self is greater than x or 0 xwise.
        """
        if isinstance(x, Number):
            return Number(int(self.value > x.value)).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION , self.context,
                                 ((x, self), "ማወዳደር"))
        
    def gte(self, x):
        """
        Return 1 if self is greater than or equal to x or 0 xwise.
        """
        if isinstance(x, Number):
            return Number(int(self.value >= x.value)).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION , self.context,
                                 ((x, self), "ማወዳደር"))
        
    def eq(self, x):
        """
        Return 1 if self is equal to x or 0 xwise.
        """
        if isinstance(x, Number):
            return Number(int(self.value == x.value)).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION , self.context,
                                 ((x, self), "ማወዳደር"))
    
    def neq(self, x):
        """
        Return 1 if self is not equal x or 0 xwise.
        """
        if isinstance(x, Number):
            return Number(int(self.value != x.value)).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION , self.context,
                                 ((x, self), "ማወዳደር"))
        
    def or_(self, x):
        """
        Return 1 if self OR x or 0 xwise.
        """
        if isinstance(x, Number):
            return Number(int(self.value or x.value)).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION , self.context,
                                 ((x, self), "ማወዳደር"))
        
    def and_(self, x):
        """
        Return 1 if self AND x or 0 xwise.
        """
        if isinstance(x, Number):
            return Number(int(self.value and x.value)).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION , self.context,
                                 ((x, self), "ማወዳደር"))
        
    def not_(self):
        """
        Return 1 if self is 0 or 0 xwise.
        """
        return Number(1 if self.value == 0 else 0).set_context(self.context), None
    
    def true(self):
        return self.value != 0
    
###############################################################################
###############################################################################

class String(DefaultType):
    """
    Strings are zero indexed.
    """
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return f'{self.value}'
    

    def add(self, x):
        """
        Returns the a String object with x concatinated at the end of self or an error if
        x is not a String object.
        """
        if isinstance(x, String):
            return String(self.value + x.value).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                                 ((x, self), "መደመር"))
        
    def multiply(self, x):
        """
        Returns a String object with self multiplied x times or an error if x is not a 
        Number object.
        """
        if isinstance(x, Number):
            return String(self.value * x.value).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                                 ((x, self), "መቀነስ"))
        
    def at(self, x):
        """
        Returns the character at the x-th index or an error if x is not an error or out 
        of bounds.
        Note: negative indicies are allowed. [if x < 0: index = len(self.value) - x]
        """
        if isinstance(x, Number):
            if abs(x.value) >= len(self.value):
                return None, RTError(x.line, x.col, INDEX_OUT_OF_BOUNDS, self.context, 
                                     (x.value, self))
            return String(self.value[x.value]).set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                                 ((x, self), "indexing"))
        
    def slice(self, start, end):
        """
        Returns a String object with self.value sliced starting from the start-th element 
        (inclusive) and ending at the end-th element (exclusive).
        Note: if start is not specified it is assumed to be 0 and if end is not specified
        it is assumed to be len(self.value) - 1.
        """
        if not start: start = Number(0)
        if not end: end = Number(len(self.value) - 1)
        if not isinstance(start, Number):
            return None, RTError(start.line, start.col, ILLEGAL_OPERATION, self.context,
                                 ((start), "indexing"))
        elif not isinstance(end, Number):
            return None, RTError(end.line, end.col, ILLEGAL_OPERATION, self.context, 
                                 ((end), "indexing"))
        elif abs(start.value) >= len(self.value):
            return None, RTError(start.line, start.col, INDEX_OUT_OF_BOUNDS, 
                                 self.context, (start.value, self))
        elif abs(end.value) >= len(self.value):
            return None, RTError(end.line, end.col, INDEX_OUT_OF_BOUNDS, self.context, 
                                 (end.value, self))
        else:
            return String(self.value[start.value: end.value]), None
        
    def eq(self, x):
        """
        Returns True(1) is self.value and x are the same or else returns False. If x is 
        not a String object an ILLEGAL_OPERATIONS error is returned.
        """
        if isinstance(x, String):
            return String(int(self.value == x.value)).set_context(
                self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                                 ((x, self), "ማወዳደር"))


# =======================================================================================
# =======================================================================================
class Array(DefaultType):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return str(self.value)
    
    
    def add(self, x):
        """
        Returns an Array object with x concatinated at the end of self.
        """
        new_array = copy.deepcopy(self)
        new_array.value.append(x)
        return new_array, None
    
    #TODO: at equals and not equals
        
    def at(self, x):
        """
        Returns the element at the x-th index or an error if x is not an error or out of 
        bounds.
        Note: negative indicies are allowed. [if x < 0: index = len(self.value) - x]
        """
        if isinstance(x, Number):
            if abs(x.value) >= len(self.value):
                return None, RTError(x.line, x.col, INDEX_OUT_OF_BOUNDS, self.context,
                                     (x.value, self))
            return self.value[x.value].set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, ILLEGAL_OPERATION, self.context, 
                                 ((x, self), "indexing"))
        
    def slice(self, start, end):
        """
        Returns an Array object with self.value sliced starting from the 
        start-th element (inclusive) and ending at the end-th element 
        (exclusive).
        Note: if start is not specified it is assumed to be 0 and if end is not specified
        it is assumed to be len(self.value) - 1.
        """
        if not start: start = Number(0)
        if not end: end = Number(len(self.value) - 1)
        if not isinstance(start, Number):
            return None, RTError(start.line, start.col, ILLEGAL_OPERATION, self.context,
                                 ((start), "indexing"))
        elif not isinstance(end, Number):
            return None, RTError(end.line, end.col, ILLEGAL_OPERATION, self.context, 
                                 ((end), "indexing"))
        elif abs(start.value) >= len(self.value):
            return None, RTError(start.line, start.col, INDEX_OUT_OF_BOUNDS, 
                                 self.context, (start.value, self))
        elif abs(end.value) >= len(self.value):
            return None, RTError(end.line, end.col, INDEX_OUT_OF_BOUNDS, self.context, 
                                 (end.value, self))
        else:
            return Array(self.value[start.value: end.value]), None


# =======================================================================================
# =======================================================================================
class Function(DefaultType):
    def __init__(self, name, args, body, return_present):
        super().__init__()
        self.name = name
        self.args = args
        self.body = body
        self.should_return = return_present  

    def __repr__(self):
        return f'[Function: <{self.name}>]'

    def check_args(self, args_from_call, func_context, line, col):
        """
        Checks if the number of arguments passed is equal to the number expected based on
        the function addition and add the arguments passed into the function's execution
        context symbol_table.
        """
        if len(args_from_call) != len(self.args):
            return RTError(line, col, NO_OF_ARGS_PASSED, self.context, 
                           (self, len(args_from_call)))
        
        for i in range(len(args_from_call)):
            func_context.symbol_table.set(self.args[i].value, (
                args_from_call[i].set_context(func_context)))
            
        return None 

    def run(self, args, interpreter, func_context, line, col):
        """
        Excutes the body of the function with args in the interpreter passed. Returns the
        return value if self.should_return or returns None.
        """
        error = self.check_args(args, func_context, line, col)
        if error: return None, error

        value, error = interpreter.visit(self.body, func_context)
        if error: return None, error

        if not self.should_return:
            value = None
        return value, None
    

# =======================================================================================
# =======================================================================================
class Class(DefaultType):
    def __init__(self, name, parent, init, attributes, methods, class_context):
        super().__init__()
        self.name = name
        self.parent = parent
        self.init = init
        self.class_context = class_context

        for attribute, value in attributes.items():
            self.class_context.symbol_table.set(attribute, value)

        for method, value in methods.items():
            self.class_context.symbol_table.set(method, value)

        if self.parent: self.class_context.parent = parent.class_context

    def __repr__(self):
        return f'[Class: <{self.name}>]'
    
    def init_obj(self, args, interpreter, init_context, line, col):
        """
        Runs the class init function, if provided, and returns an new object context 
        copied from the class_context
        """
        obj_context = copy.deepcopy(self.class_context)
        init_context.parent = obj_context
        if self.init == None: return obj_context, None
        _, error = self.init.run(args, interpreter, obj_context, line, col)
        if error: return None, error

        return obj_context, None
    

# =======================================================================================
# =======================================================================================
class Object(DefaultType):
    def __init__(self, class_):
        super().__init__()
        self.class_ = class_
        self.obj_context = None
        self.name = None
    
    def init(self, args, init_context, interpreter, line, col):
        """
        Runs the init function for the class the Object is of (self.class_) and populates 
        the object context
        """
        ctx, error = self.class_.init_obj(args, interpreter, init_context, line, col)
        if error: return error
        self.obj_context = ctx
        return None

    def set_name(self, name):
        """
        Set the name of self to name. self.name is set to None when it is initialized.
        """
        self.name = name
        self.obj_context.name = self.name
        
    def __repr__(self):
        return f'[Object: <{self.name}> of type {self.class_.name}]'
    

# =======================================================================================
# =======================================================================================
        


    
    
