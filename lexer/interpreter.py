from number import Number
from constants import *
from error import *

#####################################################################
## Context Object
#####################################################################
class Context:
    def __init__(self, name, parent = None, parent_line = None):
        self.name = name
        self.parent = parent
        self.parent_line = parent_line

#####################################################################
## RunTimeResult Object
#####################################################################
class RunTimeResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, result):
        if result.error:
            self.error = result.error
        return result.value
    
    def success(self, value):
        self.value = value
        return self
    
    def failure(self, error):
        self.error = error
        return self

#####################################################################
## Interpreter Object
#####################################################################
class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit)
        return method(node, context)
    
    def no_visit(self, node, context):
        print(node)
        raise Exception(f'No visit_{type(node).__name__} method defined!')
    
    def visit_NumberNode(self, node, context):
        return RunTimeResult().success(Number(node.token.value).set_position(node.line, node.col).set_context(context))

    def visit_BinaryOpNode(self, node, context):
        result = RunTimeResult()
        left = result.register(self.visit(node.left_node, context))
        if result.error:
            return result
        right = result.register(self.visit(node.right_node, context))
        if result.error:
            return result
        
        error = None

        if node.op_token.type == PLUS_T:
            res, error = left.added_to(right)
        elif node.op_token.type == MINUS_T:
            res, error = left.subbed_to(right)
        elif node.op_token.type == MULT_T:
            res, error = left.multiplied_to(right)
        elif node.op_token.type == DIVIDE_T:
            res, error = left.divided_to(right)
        elif node.op_token.type == POWER_T:
            res, error = left.powered_to(right)

        if error:
            return result.failure(error)
        else:
            return result.success(res.set_position(node.line, node.col))
        
    def visit_UnaryOpNode(self, node, context):
        result = RunTimeResult()
        number = result.register(self.visit(node.node, context))
        if result.error:
            return result
        
        error = None

        if node.op_token.type == MINUS_T:
            number, error = number.multiplied_to(Number(-1))

        if error:
            return result.failure(error)
        else:
            return result.success(number.set_position(node.line, node.col))
        
    
