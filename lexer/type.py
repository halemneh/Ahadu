from error import *

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
    
    def add(self, x):
        """
        Returns an error since the defaultType doen't allow addition.
        """
        return None, RuntimeError(x.line, x.col, "Illegal Operation")
    
    def subtract(self, x):
        """
        Returns an error since the defaultType doen't allow subtraction.
        """
        return None, RuntimeError(x.line, x.col, "Illegal Operation")
    
    def multiply(self, x):
        """
        Returns an error since the defaultType doen't allow multiplication.
        """
        return None, RuntimeError(x.line, x.col, "Illegal Operation")
    
    def divide(self, x):
        """
        Returns an error since the defaultType doen't allow division.
        """
        return None, RuntimeError(x.line, x.col, "Illegal Operation")
    
    def power(self, x):
        """
        Returns an error since the defaultType doen't allow exponential.
        """
        return None, RuntimeError(x.line, x.col, "Illegal Operation")
    
    def lt(self, x):
        """
        Returns an error since the defaultType doen't allow less than 
        comparison.
        """
        return None, RuntimeError(x.line, x.col, "Illegal Operation")
    
    def lte(self, x):
        """
        Returns an error since the defaultType doen't allow less than or equal
        to comparison.
        """
        return None, RuntimeError(x.line, x.col, "Illegal Operation")
    
    def gt(self, x):
        """
        Returns an error since the defaultType doen't allow greater than 
        comparison.
        """
        return None, RuntimeError(x.line, x.col, "Illegal Operation")
    
    def gte(self, x):
        """
        Returns an error since the defaultType doen't allow greater than or 
        equal to comparison.
        """
        return None, RuntimeError(x.line, x.col, "Illegal Operation")    

    def eq(self, x):
        """
        Returns an error since the defaultType doen't allow equal to  
        comparison.
        """
        return None, RuntimeError(x.line, x.col, "Illegal Operation")
    
    def neq(self, x):
        """
        Returns an error since the defaultType doen't allow not equal to 
        comparison.
        """
        return None, RuntimeError(x.line, x.col, "Illegal Operation")     

    def or_(self, x):
        """
        Returns an error since the defaultType doen't allow or combinator.
        """
        return None, RuntimeError(x.line, x.col, "Illegal Operation")
    
    def and_(self, x):
        """
        Returns an error since the defaultType doen't allow and combinator.
        """
        return None, RuntimeError(x.line, x.col, "Illegal Operation")
    
    def at(self, x):
        """
        Returns an error since the defaultType doen't allow indexing.
        """
        return None, RuntimeError(x.line, x.col, "Illegal Operation")
    
    def not_(self):
        """
        Returns an error since the defaultType doen't allow negation.
        """
        return None, RuntimeError(self.line, self.col, "Illegal Operation")
    
    def run(self):
        """
        Returns an error since the defaultType doen't allow execution.
        """
        return None, RuntimeError(self.line, self.col, "Illegal Operation")
    
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
    
    def add(self, other):
        """
        Return self + other
        """
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(
                self.context), None
        else:
            return None, RuntimeError(self.line, self.col, "Illegal Operation")
        
    def subtract(self, other):
        """
        Return self - other
        """
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(
                self.context), None
        else:
            return None, RuntimeError(self.line, self.col, "Illegal Operation")
        
    def multiply(self, other):
        """
        Return self * other
        """
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(
                self.context), None
        else:
            return None, RuntimeError(self.line, self.col, "Illegal Operation")
    
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
            return None, RuntimeError(self.line, self.col, "Illegal Operation")
        
    def power(self, other):
        """
        Return self ^ other
        """
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(
                self.context), None
        else:
            return None, RuntimeError(self.line, self.col, "Illegal Operation")
        
    def lt(self, other):
        """
        Return 1 if self is less than other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(
                self.context), None
        else:
            return None, RuntimeError(self.line, self.col, "Illegal Operation")
        
    def lte(self, other):
        """
        Return 1 if self is less than or equal to other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(
                self.context), None
        else:
            return None, RuntimeError(self.line, self.col, "Illegal Operation")
        
    def gt(self, other):
        """
        Return 1 if self is greater than other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(
                self.context), None
        else:
            return None, RuntimeError(self.line, self.col, "Illegal Operation")
        
    def gte(self, other):
        """
        Return 1 if self is greater than or equal to other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(
                self.context), None
        else:
            return None, RuntimeError(self.line, self.col, "Illegal Operation")
        
    def eq(self, other):
        """
        Return 1 if self is equal to other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(
                self.context), None
        else:
            return None, RuntimeError(self.line, self.col, "Illegal Operation")
    
    def neq(self, other):
        """
        Return 1 if self is not equal other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(
                self.context), None
        else:
            return None, RuntimeError(self.line, self.col, "Illegal Operation")
        
    def or_(self, other):
        """
        Return 1 if self OR other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(
                self.context), None
        else:
            return None, RuntimeError(self.line, self.col, "Illegal Operation")
        
    def and_(self, other):
        """
        Return 1 if self AND other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(
                self.context), None
        else:
            return None, RuntimeError(self.line, self.col, "Illegal Operation")
        
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

    def add(self, x):
        """
        Returns the a String object with x concatinated at the end of self or 
        an error if x is not a String object.
        """
        if isinstance(x, String):
            return String(self.value + x.value).set_context(
                self.context), None
        else:
            return None, RuntimeError(x.line, x.col, "Illegal Operation")
        
    def multiply(self, x):
        """
        Returns a String object with self multiplied x times or an error if x 
        is not a Number object.
        """
        if isinstance(x, Number):
            return String(self.value * x.value).set_context(
                self.context), None
        else:
            return None, RuntimeError(x.line, x.col, "Illegal Operation")
        
    def at(self, x):
        """
        Returns the character at the x-th index or an error if x is not an 
        error or out of bounds.
        """
        if isinstance(x, Number):
            if x.value > 0 or x.value >= len(self.value):
                return None, RuntimeError(x.line, x.col, "Index Out Of Bounds")
            return String(self.value[x]).set_context(
                self.context), None
        else:
            return None, RuntimeError(x.line, x.col, "Illegal Operation")
        
###############################################################################
###############################################################################
        

 
    
