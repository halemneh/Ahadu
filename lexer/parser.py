from lexer import *
from error import *

class NumberNode:
    def __init__(self, token):
        self.token = token
        self.line = token.line
        self.col = token.col

    def __repr__(self):
        return f'{self.token}'
    
class BinaryOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.right_node = right_node
        self.op_token = op_token
        self.line = left_node.line
        self.col = left_node.col

    def __repr__(self):
        return f'({self.left_node}, {self.op_token}, {self.right_node})'

class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node
        self.line = op_token.line
        self.col = op_token.col

    def __repr__(self):
        return f'({self.op_token}, {self.node})'
    
class VarAssignNode:
    def __init__(self, identifier, value):
        self.name = identifier
        self.value = value
        self.line = identifier.line
        self.col = identifier.col

class VarAccessNode:
    def __init__(self, identifier):
        self.name = identifier
        self.line = identifier.line
        self.col = identifier.col

#####################################################################
## ParserResult Object
#####################################################################
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
    
    def register(self, result):
        if isinstance(result, ParseResult):
            if result.error: self.error = result.error
            return result.node
        return result
    
    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

#####################################################################
## Parser Object
#####################################################################
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.next_token()

    #####################################################################
    ## next_token Function - tokenizes advances self.index by one and 
    ## self.curr_token to the next token in self.token. 
    #####################################################################
    def next_token(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.curr_token = self.tokens[self.index]
        return self.curr_token
    
    #####################################################################
    ## parser Function - parse self.token into nodes.
    #####################################################################
    def parse(self):
        nodes = self.experssion()

        if not nodes.error and self.curr_token.type != EOF_T:
            return nodes.failure(IllegalSyntaxError(self.curr_token.line, self.curr_token.col, 'MISSING OPS'))
        return nodes
    
    def binary_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a
        
        # result = ParseResult()
        # left = result.register(func_a())
        # if result.error: return result

        # while self.curr_token.type in ops:
        #     op_tok = self.curr_token
        #     result.register(self.next_token())
        #     right = result.register(func_b())
        #     if result.error: return result
        #     left = BinaryOpNode(left, op_tok, right)

        # return result.success(left)

        left, error = func_a()
        if error: return None, error

        while self.curr_token.type in ops:
            op_tok = self.curr_token
            self.next_token()
            right, error = func_b
            if error: return None, error
            left = BinaryOpNode(left, op_tok, right)
        return left, None

    def atom(self):
        result = ParseResult()
        token = self.curr_token

        if token.type == INT_T:
            result.register(self.next_token())
            return result.success(NumberNode(token)) 
        elif token.type == LPARAM_T:
            result.register(self.next_token())
            expression = result.register(self.experssion())

            if result.error: return result
            if self.curr_token.type == RPARAM_T:
                result.register(self.next_token())
                return result.success(expression)
            else:
                return result.failure(IllegalSyntaxError(self.curr_token.line, self.curr_token.col, RPARAM_MISSING_ERROR)) 
        return result.failure(IllegalSyntaxError(token.line, token.col, "MISSING OPS"))
    
    def power(self):
        return self.binary_op(self.atom, (POWER_T, ), self.factor)

    def factor(self):
        result = ParseResult()
        token = self.curr_token

        if token.type in (PLUS_T, MINUS_T):
            result.register(self.next_token())
            num = result.register(self.factor())
            if result.error: return result
            return result.success(UnaryOpNode(token, num))
        
        return self.power()
            
    def term(self):
        return self.binary_op(self.factor, (MULT_T, DIVIDE_T))
    
    def experssion(self):
        result = ParseResult()

        return self.binary_op(self.term, (PLUS_T, MINUS_T))