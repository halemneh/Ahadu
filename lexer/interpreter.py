from type import *
from constants import *
from error import *

class Context:
    def __init__(self, name, parent = None, parent_line = None):
        self.name = name
        self.parent = parent
        self.parent_line = parent_line
        self.symbol_table = None

class SymbolTable:
    def __init__(self):
        self.parent = None
        self.symbols = {}

    def get(self, identifier):
        value = self.symbols.get(identifier, None)
        if not value and self.parent:
            return self.parent.get(identifier)
        return value
    
    def set(self, identifier, value):
        self.symbols[identifier] = value

    def remove(self, identifier):
        return self.symbols[identifier]

class Interpreter:
    def visit(self, node, context):
        """
        Call the correspnding visit method for the node.
        """
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit)
        return method(node, context)
    
    def no_visit(self, node, _):
        """
        Raises an exception if no visit method is found for a node. 
        """
        #print(node)
        raise Exception(f'No visit_{type(node).__name__} method defined!')
    
    def visit_StatementNode(self, node, context):
        """
        
        """
        for expr in node.expr_list:
            value, error = self.visit(expr, context)
            if error: return None, error
            print(value)

        return None, None
        
    
    def visit_NumberNode(self, node, context):
        """
        Creates and returns a Number object for the NumberNode.
        """
        return Number(node.token.value).set_position(
            node.line, node.col).set_context(context), None

    def visit_BinaryOpNode(self, node, context):
        """
        Returns a Number after executing the binary operation expressed in the
        node.
        """
        left, error = self.visit(node.left_node, context)
        if error: return None, error
        if node.op_token.type != SLICE_T:
            right, error = self.visit(node.right_node, context)
            if error: return None, error
        
        error = None
        result = None

        if node.op_token.type == PLUS_T:
            result, error = left.add(right)
        elif node.op_token.type == MINUS_T:
            result, error = left.subtract(right)
        elif node.op_token.type == MULT_T:
            result, error = left.multiply(right)
        elif node.op_token.type == DIVIDE_T:
            result, error = left.divid(right)
        elif node.op_token.type == POWER_T:
            result, error = left.power(right)
        elif node.op_token.type == LT_T:
            result, error = left.lt(right)
        elif node.op_token.type == LTE_T:
            result, error = left.lte(right)
        elif node.op_token.type == GT_T:
            result, error = left.gt(right)
        elif node.op_token.type == GTE_T:
            result, error = left.gte(right)
        elif node.op_token.type == EQ_T:
            result, error = left.eq(right)
        elif node.op_token.type == NEQ_T:
            result, error = left.neq(right)
        elif node.op_token.match(KEYWORD_T, AND_T):
            result, error = left.and_(right)
        elif node.op_token.match(KEYWORD_T, OR_T):
            result, error = left.or_(right)
        elif node.op_token.type == AT_T:
            result, error = left.at(right)
        elif node.op_token.type == SLICE_T:
            start = None
            end = None
            right = node.right_node
            if right[0] != None:
                start, error = self.visit(right[0], context)
                if error: return None, error
            if right[1] != None:
                end, error = self.visit(right[1], context)
                if error: return None, error

            result, error = left.slice(start, end)
        

        if error:
            return None, error
        else:
            return result.set_position(node.line, node.col), None
        
    def visit_UnaryOpNode(self, node, context):
        """
        
        """
        number, error = self.visit(node.node, context)
        if error: return None, error
        
        error = None

        if node.op_token.type == MINUS_T:
            number, error = number.multiply(Number(-1))
        elif node.op_token.match(KEYWORD_T, NOT_T):
            number, error = number.not_()

        if error:
            return None, error
        else:
            return number.set_position(node.line, node.col), None
    
    def visit_VarAssignNode(self, node, context):
        """
        
        """
        identifier = node.name.value
        value, error = self.visit(node.value, context)
        if error: return None, error

        context.symbol_table.set(identifier, value)
        return value, None
    
    def visit_VarAccessNode(self, node, context):
        """
        
        """
        identifier = node.name.value
        value = context.symbol_table.get(identifier)

        if not value:
            return None, RTError(node.line, node.col, UNDEFINED_IDENTIFIER, 
                                 context, identifier)
        # Need copy 
        return value.set_context(context).set_position(node.line, node.col), None
        
    def visit_IfNode(self, node, context):
        """
        
        """
        for case in node.cases:
            cond, error = self.visit(case[0], context)
            if error: return None, error
            
            if cond.value != 0:
                value, error = self.visit(case[1], context)
                if error: return None, error
                return value, None
            
        if node.else_case != None:
            value, error = self.visit(node.else_case, context)
            if error: return None, error
            return value, None
        
    def visit_WhileNode(self, node, context):
        """
        
        """
        cond, error = self.visit(node.condition, context)
        if error: return None, error

        value = None
        while cond.value != 0:
            value, error = self.visit(node.statement, context)
            if error: return None, error

            cond, error = self.visit(node.condition, context)
            if error: return None, error
        
        return value, None
    
    def visit_StringNode(self, node, context):
        """
        Creates and returns a String object for the StringNode.
        """
        return String(node.string.value).set_position(
            node.line, node.col).set_context(context), None
    
    def visit_ArrayNode(self, node, context):
        """
        Creates and Returns an Array object fron the ArrayNode
        """
        elements = []
        for elem in  node.array:
            elem, error = self.visit(elem, context)
            if error: return None, error
            elements.append(elem)
        return Array(elements).set_position(
            node.line, node.col).set_context(context), None
            