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

    def __repr__(self):
        return f'({self.name.value} = {self.value})'

class VarAccessNode:
    def __init__(self, identifier):
        self.name = identifier
        self.line = identifier.line
        self.col = identifier.col

    def __repr__(self):
        return f'({self.name.value})'
    
class StatementNode:
    def __init__(self, expr_list):
        self.expr_list = expr_list
        self.line = expr_list[0].line
        self.col = expr_list[0].col

    def __repr__(self):
        result = '['
        for expr in self.expr_list:
            result += f'({expr}),\n'

        return result + ']'
    
class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case
        self.line = self.cases[0][0].line
        self.col = self.cases[0][0].col

    def __repr__(self):
        res = ''
        for i in range(len(self.cases)):
            if i == 0:
                if isinstance(self.cases[i][1], StatementNode):
                    res += f'(IF: {self.cases[i][0]} :- \n {self.cases[i][1]})\n'
                else:
                    res += f'(IF: {self.cases[i][0]} :- {self.cases[i][1]})\n'
            else:
                if isinstance(self.cases[i][1], StatementNode):
                    res += f' (ELIF: {self.cases[i][0]} :- \n {self.cases[i][1]})\n'
                else:
                    res += f' (ELIF: {self.cases[i][0]} :- {self.cases[i][1]})\n'
        if self.else_case != None:
            if isinstance(self.cases[i][1], StatementNode):
                res += f' (ELSE:- \n {self.else_case})\n'
            else:
                res += f' (ELSE:- {self.else_case})\n'
        
        return res

class WhileNode:
    def __init__(self, condition, statements):
        self.condition = condition
        self.statement = statements
        self.line = self.condition.line
        self.col = self.condition.col

    def __repr__(self):
        return f'(WHILE: {self.condition}:-\n {self.statement}\n)'

# -----------------------------------------------------------------------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.indent = 0
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
    
    def prev_tokens(self):
        """
        Returns the prevous token in self.tokens after assigning it to 
        self.curr_token and reversing self.index by one.
        """
        self.index -= 1
        if self.index >= 0:
            self.curr_token = self.tokens[self.index]
        return self.curr_token
    
    def parse(self):
        """
        Returns an node object and an error if there is any after parsing 
        self.tokens
        """
        nodes, error = self.statements()
        if error: return None, error

        if not error and self.curr_token.type != EOF_T:
            return None, IllegalSyntaxError(self.curr_token.line,
                                            self.curr_token.col, 'MISSING OPS 1')
        return nodes, None
    
    def statements(self):
        """
        
        """
        statements = []
        # start_line = self.curr_token.line
        # start_col = self.curr_token.col
        done = False

        while self.curr_token.type == NEWLINE_T:
            self.next_token()

        tab_count = 0
        while self.curr_token.type == TAB_T:
            tab_count += 1
            self.next_token()

        if tab_count < self.indent:
            for _ in range(tab_count):
                self.prev_tokens()
            done = True
        elif tab_count > self.indent:
            return None, IndentationError(self.curr_token.line, 
                                          self.curr_token.col)

        expr, error = self.experssion()
        if error: return None, error
        statements.append(expr)

        while True:
            line_count = 0
            while self.curr_token.type == NEWLINE_T:
                line_count += 1
                self.next_token()

            if line_count == 0: done = True

            if done:
                if self.curr_token.match(KEYWORD_T, IF_T):
                    self.next_token()
                    if_condition = statements.pop()
                    if_statment, error = self.if_expr(if_condition)
                    if error: return None, error
                    statements.append(if_statment)
                    done = False
                elif self.curr_token.match(KEYWORD_T, WHILE_T):
                    self.next_token()
                    while_condition = statements.pop()
                    if_statment, error = self.while_expr(while_condition)
                    if error: return None, error
                    statements.append(if_statment)
                    done = False

            if done or self.curr_token.type == EOF_T: break
            if self.curr_token.type == NEWLINE_T: continue
        
            tab_count = 0
            while self.curr_token.type == TAB_T:
                tab_count += 1
                self.next_token()

            if tab_count < self.indent:
                for _ in range(tab_count):
                    self.prev_tokens()
                done = True
                continue
            elif tab_count > self.indent:
                return None, IndentationError(self.curr_token.line, 
                                            self.curr_token.col)
            
            expr, error = self.experssion()
            if error: return None, error
            
            statements.append(expr)
        
        return StatementNode(statements), None
    
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
         
        elif token.match(KEYWORD_T, IF_T):
            return None, IllegalSyntaxError(token.line, token.col, 
                                            "Expected Expression before IF")
        elif token.match(KEYWORD_T, WHILE_T):
            return None, IllegalSyntaxError(token.line, token.col, 
                                            "Expected Expression before WHILE")
        elif token.match(KEYWORD_T, ELIF_START_T):
            return None, IllegalSyntaxError(token.line, token.col, 
                                                "IF statement required before ELIF")
        
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
        if self.curr_token.type == IDENTIFIER_T:
            identifier = self.curr_token
            self.next_token()
            if self.curr_token.type == EQUAL_T:
                self.next_token()
                expr, error = self.experssion()
                if error: return None, error
                return VarAssignNode(identifier, expr), None
            self.prev_tokens()
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

    def if_expr(self, if_condition):
        """
        
        """
        cases = []
        else_case = None

        if self.curr_token.type != THEN_T and (self.curr_token 
                                                == NEWLINE_T):
            return None, IllegalSyntaxError(self.curr_token.line,
                                            self.curr_token.col, 
                                            "Expected ':-' ")
        if self.curr_token.type == THEN_T:
            self.next_token()
        
        if self.curr_token.type == NEWLINE_T:
            self.indent += 1
            if_statement, error = self.statements()
            if error: return None, error
            cases.append((if_condition, if_statement))
            self.indent -= 1

            if self.curr_token.type == TAB_T:
                if ((self.tokens[self.index + self.indent].match(KEYWORD_T, 
                                                                 ELIF_START_T)) 
                                                                 or 
                    (self.tokens[self.index + self.indent].match(KEYWORD_T, 
                    ELSE_T))):
                    for _ in range(self.indent):
                        self.next_token()
            while self.curr_token.match(KEYWORD_T, ELIF_START_T):
                self.next_token()
                elif_condition, error = self.experssion()
                if error: return None, error

                #self.next_token()
                if not self.curr_token.match(KEYWORD_T, IF_T):
                    return None, IllegalSyntaxError(self.curr_token.line, 
                                                    self.curr_token.col,
                                                    "Expected Elif End")


                self.next_token()
                if self.curr_token.type != THEN_T and (self.curr_token 
                                                        == NEWLINE_T):
                    return None, IllegalSyntaxError(self.curr_token.line, 
                                                    self.curr_token.col,
                                                    "Expected ':-' ")
                if self.curr_token.type == THEN_T:
                    self.next_token()
                if self.curr_token.type == NEWLINE_T:
                    # self.next_token()
                    self.indent += 1
                    elif_statement, error = self.statements()
                    if error: return None, error
                    cases.append((elif_condition, elif_statement))
                    self.indent -= 1

                else:
                    elif_statement, error = self.experssion()
                    if error: return None, error
                    cases.append((elif_condition, elif_statement))

                if self.curr_token.type == TAB_T:
                    if ((self.tokens[self.index + self.indent].match(
                        KEYWORD_T, ELIF_START_T)) or 
                        (self.tokens[self.index + self.indent].match(KEYWORD_T, 
                                                                     ELSE_T))):
                        for _ in range(self.indent):
                            self.next_token()
                
            if self.curr_token.match(KEYWORD_T, ELSE_T):
                self.next_token()
                if self.curr_token.type != THEN_T and (self.curr_token 
                                                        == NEWLINE_T):
                    return None, IllegalSyntaxError(self.curr_token.line, 
                                                    self.curr_token.col,
                                                    "Expected ':-' ")
                if self.curr_token.type == THEN_T:
                    self.next_token()
                if self.curr_token.type == NEWLINE_T:
                    self.next_token()
                    self.indent += 1
                    else_case, error = self.statements()
                    if error: return None, error
                    self.indent -= 1

                else:
                    self.next_token()
                    else_case, error = self.experssion()
                    if error: return None, error
        else:
            if_expr, error = self.experssion()
            if error: return None, error
            cases.append((if_condition, if_expr))

            while self.curr_token.match(KEYWORD_T, ELIF_START_T):
                self.next_token()
                elif_condition, error = self.experssion()
                if error: return None, error

                
                if not self.curr_token.match(KEYWORD_T, IF_T):
                    return None, IllegalSyntaxError(self.curr_token.line, 
                                                    self.curr_token.col,
                                                    "Expected Elif End")
                self.next_token()
                elif_expr, error = self.experssion()
                if error: return None, error
                cases.append((elif_condition, elif_expr))

            if self.curr_token.match(KEYWORD_T, ELSE_T):
                self.next_token()
                else_case, error = self.experssion()
                if error: return None, error

        return IfNode(cases, else_case), None
    
    def while_expr(self, while_condition):
        print("WHILE_HERE")
        if self.curr_token.type != THEN_T and (self.curr_token 
                                                        == NEWLINE_T):
            return None, IllegalSyntaxError(self.curr_token.line, 
                                            self.curr_token.col,
                                            "Expected ':-' ")
        if self.curr_token.type == THEN_T:
            self.next_token()
        if self.curr_token.type != NEWLINE_T:
            expr, error = self.experssion()
            if error: return None, error
            return WhileNode(while_condition, expr)
        self.indent += 1
        statement, error = self.statements()
        if error: return None, error
        self.indent -= 1
        return WhileNode(while_condition, statement), None


        
        
    