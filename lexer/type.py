from error import *
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
        return None, RTError(x.line, x.col, "Illegal Operation", self.context)
    
    def subtract(self, x):
        """
        Returns an error since the defaultType doen't allow subtraction.
        """
        return None, RTError(x.line, x.col, "Illegal Operation", self.context)
    
    def multiply(self, x):
        """
        Returns an error since the defaultType doen't allow multiplication.
        """
        return None, RTError(x.line, x.col, "Illegal Operation", self.context)
    
    def divide(self, x):
        """
        Returns an error since the defaultType doen't allow division.
        """
        return None, RTError(x.line, x.col, "Illegal Operation", self.context)
    
    def power(self, x):
        """
        Returns an error since the defaultType doen't allow exponential.
        """
        return None, RTError(x.line, x.col, "Illegal Operation", self.context)
    
    def lt(self, x):
        """
        Returns an error since the defaultType doen't allow less than 
        comparison.
        """
        return None, RTError(x.line, x.col, "Illegal Operation", self.context)
    
    def lte(self, x):
        """
        Returns an error since the defaultType doen't allow less than or equal
        to comparison.
        """
        return None, RTError(x.line, x.col, "Illegal Operation", self.context)
    
    def gt(self, x):
        """
        Returns an error since the defaultType doen't allow greater than 
        comparison.
        """
        return None, RTError(x.line, x.col, "Illegal Operation", self.context)
    
    def gte(self, x):
        """
        Returns an error since the defaultType doen't allow greater than or 
        equal to comparison.
        """
        return None, RTError(x.line, x.col, "Illegal Operation", self.context)

    def eq(self, x):
        """
        Returns an error since the defaultType doen't allow equal to  
        comparison.
        """
        return None, RTError(x.line, x.col, "Illegal Operation" , self.context)
    
    def neq(self, x):
        """
        Returns an error since the defaultType doen't allow not equal to 
        comparison.
        """
        return None, RTError(x.line, x.col, "Illegal Operation" , self.context)     

    def or_(self, x):
        """
        Returns an error since the defaultType doen't allow or combinator.
        """
        return None, RTError(x.line, x.col, "Illegal Operation" , self.context)
    
    def and_(self, x):
        """
        Returns an error since the defaultType doen't allow and combinator.
        """
        return None, RTError(x.line, x.col, "Illegal Operation" , self.context)
    
    def at(self, x):
        """
        Returns an error since the defaultType doen't allow indexing.
        """
        return None, RTError(x.line, x.col, "Illegal Operation" , self.context)
    
    def slice(self, start, end):
        """
        Returns an error since the defaultType doen't allow slicing.
        """
        return None, RTError(start.line, start.col, "Illegal Operation" , self.context)
    
    def not_(self):
        """
        Returns an error since the defaultType doen't allow negation.
        """
        return None, RTError(self.line, self.col, "Illegal Operation" , self.context)
    
    def run(self, args):
        """
        Returns an error since the defaultType doen't allow execution.
        """
        return None, RTError(args.line, args.col, "Illegal Operation" , self.context)
    
    def true(self):
        """
        Returns False since the defaultType represents False.
        """
        return False
    
###############################################################################
###############################################################################

class Number(DefaultType):
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def __repr__(self):
        return str(self.value)
    
    def copy(self):
        """
        Return a copy Number object of self.
        """
        return Number(self.value).set_context(self.context).set_position(
            self.line, self.col)
    
    def add(self, other):
        """
        Return self + other
        """
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(
                self.context), None
        else:
            return None, RTError(self.line, self.col, "Illegal Operation" , self.context)
        
    def subtract(self, other):
        """
        Return self - other
        """
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(
                self.context), None
        else:
            return None, RTError(self.line, self.col, "Illegal Operation" , self.context)
        
    def multiply(self, other):
        """
        Return self * other
        """
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(
                self.context), None
        else:
            return None, RTError(self.line, self.col, "Illegal Operation" , self.context)
    
    def divid(self, other):
        """
        Return self / other
        """
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.line, other.col, 
                                     DIVISION_BY_ZERO_ERROR, self.context)
            return Number(self.value / other.value).set_context(
                self.context), None
        else:
            return None, RTError(self.line, self.col, "Illegal Operation" , self.context)
        
    def power(self, other):
        """
        Return self ^ other
        """
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(
                self.context), None
        else:
            return None, RTError(self.line, self.col, "Illegal Operation" , self.context)
        
    def lt(self, other):
        """
        Return 1 if self is less than other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(
                self.context), None
        else:
            return None, RTError(self.line, self.col, "Illegal Operation" , self.context)
        
    def lte(self, other):
        """
        Return 1 if self is less than or equal to other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(
                self.context), None
        else:
            return None, RTError(self.line, self.col, "Illegal Operation" , self.context)
        
    def gt(self, other):
        """
        Return 1 if self is greater than other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(
                self.context), None
        else:
            return None, RTError(self.line, self.col, "Illegal Operation" , self.context)
        
    def gte(self, other):
        """
        Return 1 if self is greater than or equal to other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(
                self.context), None
        else:
            return None, RTError(self.line, self.col, "Illegal Operation" , self.context)
        
    def eq(self, other):
        """
        Return 1 if self is equal to other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(
                self.context), None
        else:
            return None, RTError(self.line, self.col, "Illegal Operation" , self.context)
    
    def neq(self, other):
        """
        Return 1 if self is not equal other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(
                self.context), None
        else:
            return None, RTError(self.line, self.col, "Illegal Operation" , self.context)
        
    def or_(self, other):
        """
        Return 1 if self OR other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(
                self.context), None
        else:
            return None, RTError(self.line, self.col, "Illegal Operation" , self.context)
        
    def and_(self, other):
        """
        Return 1 if self AND other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(
                self.context), None
        else:
            return None, RTError(self.line, self.col, "Illegal Operation" , self.context)
        
    def not_(self):
        """
        Return 1 if self is 0 or 0 otherwise.
        """
        return Number(1 if self.value == 0 else 0).set_context(self.context
                                                               ), None
    
    def true(self):
        return self.value != 0
    
###############################################################################
###############################################################################

class String(DefaultType):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return f'"{self.value}"'
    
    def copy(self):
        """
        Return a copy String object of self.
        """
        return String(self.value).set_context(self.context).set_position(
            self.line, self.col)

    def add(self, x):
        """
        Returns the a String object with x concatinated at the end of self or 
        an error if x is not a String object.
        """
        if isinstance(x, String):
            return String(self.value + x.value).set_context(
                self.context), None
        else:
            return None, RTError(x.line, x.col, "Illegal Operation" , self.context)
        
    def multiply(self, x):
        """
        Returns a String object with self multiplied x times or an error if x 
        is not a Number object.
        """
        if isinstance(x, Number):
            return String(self.value * x.value).set_context(
                self.context), None
        else:
            return None, RTError(x.line, x.col, "Illegal Operation" , self.context)
        
    def at(self, x):
        """
        Returns the character at the x-th index or an error if x is not an 
        error or out of bounds.
        """
        if isinstance(x, Number):
            if x.value > 0 or x.value >= len(self.value):
                return None, RTError(x.line, x.col, "Index Out Of Bounds" , self.context)
            return String(self.value[x]).set_context(
                self.context), None
        else:
            return None, RTError(x.line, x.col, "Illegal Operation" , self.context)
        
    def slice(self, start, end):
        """
        Returns a String object with self.value sliced starting from the 
        start-th element (inclusive) and ending at the end-th element 
        (exclusive).
        """
        if not start: start = Number(0)
        if not end: end = Number(len(self.value))
        if not isinstance(start, Number):
            return None, RTError(start.line, start.col, "Illegal Operation1" , self.context)
        elif not isinstance(end, Number):
            return None, RTError(end.line, end.col, "Illegal Operation2" , self.context)
        else:
            return String(self.value[start.value: end.value]), None
        
    def eq(self, x):
        """
        
        """
        if isinstance(x, String):
            return String(int(self.value == x.value)).set_context(
                self.context), None
        else:
            return None, RTError(x.line, x.col, "Illegal Operation" , self.context)

        
###############################################################################
###############################################################################
        
class Array(DefaultType):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return str(self.value)
    
    def copy(self):
        """
        Return a copy Number object of self.
        """
        copy = Array(self.value)
        copy.set_context(self.context).set_position(self.line, self.col)
        return copy
    
    def add(self, x):
        """
        Returns an Array object with x concatinated at the end of self.
        """
        new_array = copy.deepcopy(self)
        new_array.value.append(x)
        return new_array, None
    
    def join(self, x):
        """
        Returns an Array object with x concatinated at the end of self or an 
        error if x is not an Array object.
        """
        if isinstance(x, Array):
            return Array(self.value + x.value).set_context(
                self.context), None
        else:
            return None, RTError(x.line, x.col, "Illegal Operation" , self.context)
        
    def at(self, x):
        """
        Returns the element at the x-th index or an error if x is not an 
        error or out of bounds.
        """
        if isinstance(x, Number):
            if x.value >= len(self.value):
                return None, RTError(x.line, x.col, "Index Out Of Bounds" , self.context)
            return self.value[x.value].set_context(self.context), None
        else:
            return None, RTError(x.line, x.col, "Illegal Operation" , self.context)
        
    def slice(self, start, end):
        """
        Returns an Array object with self.value sliced starting from the 
        start-th element (inclusive) and ending at the end-th element 
        (exclusive).
        """
        if not start: start = Number(0)
        if not end: end = Number(len(self.value))
        if not isinstance(start, Number):
            return None, RTError(start.line, start.col, "Illegal Operation", self.context)
        elif not isinstance(end, Number):
            return None, RTError(end.line, end.col, "Illegal Operation" , self.context)
        else:
            return Array(self.value[start.value: end.value]), None

###############################################################################
###############################################################################


    
        