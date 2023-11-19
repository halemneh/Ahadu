from lexer import *
from error import *

class NumberNode:
    def __init__(self, token):
        self.token = token
        self.line = token.line
        self.col = token.col

    def __repr__(self):
        return f'NN {self.token}'
    
class BoolNode:
    def __init__(self, token):
        self.value = token.value
        self.line = token.line
        self.col = token.col
    
class BinaryOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.right_node = right_node
        self.op_token = op_token
        self.line = left_node.line
        self.col = left_node.col

    def __repr__(self):
        return f'(BN {self.left_node}, {self.op_token}, {self.right_node})'

class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node
        self.line = op_token.line
        self.col = op_token.col

    def __repr__(self):
        return f'(UN {self.op_token}, {self.node})'
    
class VarAssignNode:
    def __init__(self, identifier, value):
        self.name = identifier
        self.value = value
        self.line = identifier.line
        self.col = identifier.col

    def __repr__(self):
        return f'({self.name.value} = {self.value})'

class VarAccessNode:
    def __init__(self, identifier):
        self.name = identifier
        self.line = identifier.line
        self.col = identifier.col

    def __repr__(self):
        return f'({self.name.value})'

# -----------------------------------------------------------------------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.next_token()

    def next_token(self):
        """
        Returns the next token in self.tokens after assigning it to 
        self.curr_token and advancing self.index by one.
        """
        self.index += 1
        if self.index < len(self.tokens):
            self.curr_token = self.tokens[self.index]
        return self.curr_token
    
    def parse(self):
        """
        Returns an node object and an error if there is any after parsing 
        self.tokens
        """
        nodes, error = self.experssion()

        if not error and self.curr_token.type != EOF_T:
            return None, IllegalSyntaxError(self.curr_token.line,
                                            self.curr_token.col, 'MISSING OPS')
        return nodes, None
    
    def statement(self):
        """
        
        """
        pass
    
    def binary_op(self, func_a, ops, func_b=None):
        """
        Returns a BinaryOpNode and an error if there is any.
        """
        if func_b == None:
            func_b = func_a

        left, error = func_a()
        if error: return None, error

        while self.curr_token.type in ops or (
                self.curr_token.type, self.curr_token.value) in ops:
            op_tok = self.curr_token
            self.next_token()
            right, err = func_b()
            if err: return None, err
            left = BinaryOpNode(left, op_tok, right)
        return left, None

    def atom(self):
        """
        
        """
        token = self.curr_token

        if token.type == INT_T:
            self.next_token()
            return NumberNode(token), None
        elif token.type == IDENTIFIER_T:
            self.next_token()
            return VarAccessNode(token), None
        elif token.type == LPARAM_T:
            self.next_token()
            experssion, error = self.experssion()
            if error: return None, error
            if self.curr_token.type == RPARAM_T:
                self.next_token()
                return experssion, None
            else:
                return None, IllegalSyntaxError(self.curr_token.line, 
                                                self.curr_token.col, 
                                                RPARAM_MISSING_ERROR)
            
        return None, IllegalSyntaxError(token.line, token.col, 
                                        "MISSING OPERATIONS")
    
    def power(self):
        """
        
        """
        return self.binary_op(self.atom, (POWER_T, ), self.factor)

    def factor(self):
        """
        
        """
        token = self.curr_token
        if token.type in (PLUS_T, MINUS_T):
            self.next_token()
            number, error = self.factor()
            if error: return None, error
            return UnaryOpNode(token, number), None
        return self.power()
            
    def term(self):
        """
        
        """
        return self.binary_op(self.factor, (MULT_T, DIVIDE_T))
    
    def experssion(self):
        """
        Return a BinaryOpNode or an error
        """
        if self.curr_token.match(KEYWORD_T, INT_T):
            self.next_token()
            if self.curr_token.type != IDENTIFIER_T:
                return None, IllegalSyntaxError(self.curr_token.line, 
                                                self.curr_token.col, 
                                                EXPECTED_IDENTIFIER)
            
            identifier = self.curr_token
            self.next_token()
            if self.curr_token.type != EQUAL_T:
                return None, IllegalSyntaxError(self.curr_token.line,
                                                self.curr_token.col,
                                                EXPECTED_EQUALS)
            
            self.next_token()
            value, error = self.experssion()
            if error: return None, error
            return VarAssignNode(identifier, value), None
        return self.binary_op(self.comp_expr, ((KEYWORD_T, AND_T), (KEYWORD_T, 
                                                                    OR_T)))

        
    def comp_expr(self):
        """
        
        """
        token = self.curr_token

        if token.match(KEYWORD_T, NOT_T):
            self.next_token()
            expr, error = self.comp_expr()
            if error: return None, error
            return UnaryOpNode(token, expr), None
        return self.binary_op(self.arith_expr, (EQ_T, LT_T, LTE_T, GTE_T, GT_T, 
                                                GTE_T, NEQ_T))
    
    def arith_expr(self):
        """
        
        """
        return self.binary_op(self.term, (PLUS_T, MINUS_T))