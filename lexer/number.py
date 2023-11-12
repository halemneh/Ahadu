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
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        
    def subbed_to(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        
    def multiplied_to(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
    
    def divided_to(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.line, other.col, DIVISION_BY_ZERO_ERROR, self.context)
            return Number(self.value / other.value).set_context(self.context), None
        
    def powered_to(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None