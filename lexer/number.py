from error import *

class Number:
    def __init__(self, value):
        self.value = value
        self.set_position()
        self.set_context()

    def set_position(self, line = None, col = None):
        self.line = line
        self.col = col
        return self
    
    def set_context(self, context = None):
        self.context = context
        return self

    def __repr__(self):
        return str(self.value)
    
    def added_to(self, other):
        """
        Return self + other
        """
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(
                self.context), None
        
    def subbed_to(self, other):
        """
        Return self - other
        """
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(
                self.context), None
        
    def multiplied_to(self, other):
        """
        Return self * other
        """
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(
                self.context), None
    
    def divided_to(self, other):
        """
        Return self / other
        """
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.line, other.col, 
                                     DIVISION_BY_ZERO_ERROR, self.context)
            return Number(self.value / other.value).set_context(
                self.context), None
        
    def powered_to(self, other):
        """
        Return self ^ other
        """
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(
                self.context), None
        
    def lt_to(self, other):
        """
        Return 1 if self is less than other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(
                self.context), None
        
    def lte_to(self, other):
        """
        Return 1 if self is less than or equal to other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(
                self.context), None
        
    def gt_to(self, other):
        """
        Return 1 if self is greater than other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(
                self.context), None
        
    def gte_to(self, other):
        """
        Return 1 if self is greater than or equal to other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(
                self.context), None
        
    def eq_to(self, other):
        """
        Return 1 if self is equal to other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(
                self.context), None
    
    def neq_to(self, other):
        """
        Return 1 if self is not equal other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(
                self.context), None
        
    def or_to(self, other):
        """
        Return 1 if self OR other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(
                self.context), None
        
    def and_to(self, other):
        """
        Return 1 if self AND other or 0 otherwise.
        """
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(
                self.context), None
        
    def not_to(self):
        """
        Return 1 if self is 0 or 0 otherwise.
        """
        return Number(1 if self.value == 0 else 0).set_context(self.context
                                                               ), None
        
