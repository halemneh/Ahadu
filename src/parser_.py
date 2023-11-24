from lexer import *
from error import *
from nodes import *

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
            print(self.curr_token)
            print(nodes)
            return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col, 
                                            'Incomplete expression#')
        return nodes, None
    
    def statements(self):
        """
        
        """
        statements = []
        expr = None
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
            return None, IndentationError(self.curr_token.line, self.curr_token.col, 
                                          self.indent)

        if self.curr_token.match(KEYWORD_T, CLASS_T):
            self.next_token()
            obj, error = self.class_definition()
            if error: return None, error
            statements.append(obj)
        else:
            expr, error = self.experssion()
            if error: return None, error
            statements.append(expr)
            if isinstance(expr, ReturnNode):
                while self.curr_token.type == NEWLINE_T:
                    self.next_token()
                return StatementNode(statements), None

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
                elif isinstance(expr, FunctionDefNode):
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
                return None, IndentationError(self.curr_token.line, self.curr_token.col, 
                                              self.indent)
            if self.curr_token.match(KEYWORD_T, CLASS_T):
                self.next_token()
                obj, error = self.class_definition()
                if error: return None, error
                statements.append(obj)
            else:
                expr, error = self.experssion()
                if error: return None, error
                statements.append(expr)
                if isinstance(expr, ReturnNode): 
                    while self.curr_token.type == NEWLINE_T:
                        self.next_token()
                    return StatementNode(statements), None
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
            if self.curr_token.type == LBRACKET_T:
                self.next_token()
                index, op, error = self.slice()
                if error: return None, error
                if self.curr_token.type == RBRACKET_T:
                    self.next_token()
                    return BinaryOpNode(VarAccessNode(token), op, index), None
                self.prev_tokens()
                return None, IllegalSyntaxError(self.curr_token.line, 
                                                self.curr_token.col, 
                                                RBRACKET_MISSING_ERROR)
            elif self.curr_token.type == LPARAM_T:
                self.next_token()
                args, error = self.array(True)
                if error: return None, error
                if self.curr_token.type == RPARAM_T:
                    self.next_token()
                    return BinaryOpNode(VarAccessNode(token), 
                                        Token(CALL_T, token.line, token.col), 
                                        args), None
                self.prev_tokens()
                return None, IllegalSyntaxError(self.curr_token.line, 
                                                self.curr_token.col, 
                                                RBRACKET_MISSING_ERROR,
                                                )
            elif self.curr_token.type == DOT_T:
                op_token = self.curr_token
                self.next_token()
                if self.curr_token.type != IDENTIFIER_T:
                    return None, IllegalSyntaxError(self.curr_token.line,
                                                    self.curr_token.col,
                                                    "Expected method or attribute")
                callee = self.curr_token
                self.next_token()
                if self.curr_token.type == LPARAM_T:
                    self.next_token()
                    args, error = self.array(True)
                    if error: return None, error
                    if self.curr_token.type == RPARAM_T:
                        self.next_token()
                        return BinaryOpNode(VarAccessNode(token), op_token, 
                                            (VarAccessNode(callee), args)), None
                    self.prev_tokens()
                    return None, IllegalSyntaxError(self.curr_token.line, 
                                                    self.curr_token.col, 
                                                    RPARAM_MISSING_ERROR)
                return BinaryOpNode(VarAccessNode(token), op_token, 
                                    (VarAccessNode(callee), None)), None
            return VarAccessNode(token), None
        elif token.match(KEYWORD_T, FUNC_T):
            self.next_token()
            func, error = self.function_definition()
            if error: return None, error
            return func, None
        elif token.type == LPARAM_T:
            self.next_token()
            experssion, error = self.experssion()
            if error: return None, error
            if self.curr_token.type == RPARAM_T:
                self.next_token()
                return experssion, None
            self.prev_tokens()
            return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col,
                                            RPARAM_MISSING_ERROR)
        elif token.type == LBRACKET_T:
            self.next_token()
            array, error = self.array()
            if error: return None, error
            if self.curr_token.type == RBRACKET_T:
                self.next_token()
                return ArrayNode(array, token.line, token.col), None
            self.prev_tokens()
            return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col,
                                            RBRACKET_MISSING_ERROR)
        elif token.type == STRING_T:
            self.next_token()
            return StringNode(token), None
        
        elif token.type == KEYWORD_T and token.value in BUILT_IN_FUNCS:
            self.next_token()
            if self.curr_token.type != LPARAM_T:
                return None, IllegalSyntaxError(self.curr_token.line, 
                                                self.curr_token.col,
                                                "'(' expected")
            self.next_token()
            args, error = self.array(True)
            if error: return None, error
            if self.curr_token.type != RPARAM_T:
                return None, IllegalSyntaxError(self.curr_token.line, 
                                                self.curr_token.col,
                                                RPARAM_MISSING_ERROR)
            self.next_token()
            return BuiltInFuncNode(token, args), None
        
        elif token.match(KEYWORD_T, IF_T):
            return None, IllegalSyntaxError(token.line, token.col, 
                                            "Expected Expression before IF")
        elif token.match(KEYWORD_T, WHILE_T):
            return None, IllegalSyntaxError(token.line, token.col, 
                                            "Expected Expression before WHILE")
        elif token.match(KEYWORD_T, ELIF_START_T):
            return None, IllegalSyntaxError(token.line, token.col, 
                                            "IF required before ELIF")
        self.prev_tokens()
        return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col, 
                                        "Incomplete expression!")
    
    def array(self, PARAN = False):
        """
        Parses an array and returns a list of the array elements.
        """
        
        array = []
        boundary = RPARAM_T if PARAN else RBRACKET_T
        error_type = RPARAM_MISSING_ERROR if PARAN else RBRACKET_MISSING_ERROR
        while self.curr_token.type != boundary:
            if self.curr_token.type == NEWLINE_T:
                self.prev_tokens()
                
                return None, IllegalSyntaxError(self.curr_token.line, 
                                                self.curr_token.col,
                                                error_type)
            elem, error = self.experssion()
            if error: return None, error
            array.append(elem)
            if self.curr_token.type != COMMA_T and (self.curr_token.type != boundary):
                self.prev_tokens()
                return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col, 
                                                "Expected Comma")
            
            if self.curr_token.type == COMMA_T: self.next_token()
            
        return array, None
    
    def slice(self):
        """
        
        """
        op = Token(SLICE_T, self.curr_token.line, self.curr_token.col)
        if self.curr_token.type == COLON_T:
            self.next_token()
            if self.curr_token.type == RBRACKET_T:
                return (None, None), op, None
            end, error = self.arith_expr()
            if error: return None, None, error
            return (None, end), op, None
        elif self.curr_token.type == RBRACKET_T:
            return None, None, IllegalSyntaxError(self.curr_token.line, 
                                                  self.curr_token.col, "Index Missing")
        else:
            start, error = self.arith_expr()
            if error: return None, None, error
            if self.curr_token.type == COLON_T:
                self.next_token()
                if self.curr_token.type == RBRACKET_T:
                    return (start, None), op, None
                end, error = self.arith_expr()
                if error: return None, None, error
                return (start, end), op, None
            else:
                op = Token(AT_T, self.curr_token.line, self.curr_token.col)
                return start, op, None

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
            start_index = self.index
            identifier = self.curr_token
            self.next_token()
            if self.curr_token.type == DOT_T:
                self.prev_tokens()
                call, error = self.atom()
                if error: return None, error

                if self.curr_token.type == EQUAL_T:
                    self.next_token()
                    expr, error = self.experssion()
                    if error: return None, error
                    if isinstance(call, BinaryOpNode):
                        return VarAssignNode(call, expr), None
                    return VarAssignNode(identifier, expr), None
                for _ in range(self.index - start_index):
                    self.prev_tokens()
            elif self.curr_token.type == EQUAL_T:
                self.next_token()
                expr, error = self.experssion()
                if error: return None, error
                return VarAssignNode(identifier, expr), None
            else:
                self.prev_tokens()
        elif self.curr_token.match(KEYWORD_T, RETURN_T):
            self.next_token()
            return_expr = None
            if self.curr_token.type != NEWLINE_T:
                return_expr, error = self.experssion()
                if error: return None, error
            return ReturnNode(return_expr), None
        return self.binary_op(self.comp_expr, ((KEYWORD_T, AND_T), (KEYWORD_T, OR_T)))

        
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
            return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col, 
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
        """
        
        """
        if self.curr_token.type != THEN_T and (self.curr_token 
                                                        == NEWLINE_T):
            return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col,
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

    def function_definition(self):
        """
        
        """
        if self.curr_token.type != IDENTIFIER_T and not self.curr_token.match(KEYWORD_T, INIT_T):
            return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col,
                                            "Function name not specified")
        
        func_name = self.curr_token
        self.next_token()
        if self.curr_token.type != LPARAM_T:
            return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col,
                                            "Left PARAM missing")
        
        self.next_token()
        args = []
        while True:
            if self.curr_token.type == RPARAM_T:
                self.next_token()
                break

            if self.curr_token.type != IDENTIFIER_T:
                return None, IllegalSyntaxError(self.curr_token.line, 
                                                self.curr_token.col,
                                                "Args not specified correctly")
            
            args.append(self.curr_token)
            self.next_token()

            if self.curr_token.type != COMMA_T and (
                self.curr_token.type != RPARAM_T):
                return None, IllegalSyntaxError(self.curr_token.line, 
                                                self.curr_token.col,
                                                "Comma expected")
            if self.curr_token.type == COMMA_T:
                self.next_token()
        
        if self.curr_token.type == NEWLINE_T:
            return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col,
                                            "Expected :-")
        
        if self.curr_token.type == THEN_T:
            self.next_token()

        if self.curr_token.type == NEWLINE_T:
            self.next_token()
            self.indent += 1
            body, error = self.statements()
            if error: return None, error
            self.indent -= 1

            return FunctionDefNode(func_name, args, body), None
        
        body, error = self.experssion()
        if error: return None, error

        # if self.curr_token.type != NEWLINE_T:
        #     return None, IllegalSyntaxError(self.curr_token.line, 
        #                                     self.curr_token.col,
        #                                     "Invalid inline Function definition")

        return FunctionDefNode(func_name, args, body), None
    
    def class_definition(self):
        """
        
        """
        init = None
        parent = None
        attributes = []
        methods = []
        if self.curr_token.type != IDENTIFIER_T:
            return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col,
                                            "Class Name expected!")
        
        class_name = self.curr_token
        self.next_token()

        """ Inheritence """
        if self.curr_token.type == LPARAM_T:
            self.next_token()
            if self.curr_token.type != IDENTIFIER_T:
                return None, IllegalSyntaxError(self.curr_token.line, 
                                                self.curr_token.col,
                                                "Class Parent Name expected!")
            parent = self.curr_token
            self.next_token()
            if self.curr_token.type != RPARAM_T:
                return None, IllegalSyntaxError(self.curr_token.line, 
                                                self.curr_token.col,
                                                RPARAM_MISSING_ERROR)
            self.next_token()

        if self.curr_token.type != THEN_T:
            return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col,
                                            ":- Expected")
        self.next_token()
        if self.curr_token.type != NEWLINE_T:
            return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col,
                                            "Class definition in new line")
        
        self.next_token()
        self.indent += 1
        while True:
            tab_count = 0
            while self.curr_token.type == TAB_T:
                tab_count += 1
                self.next_token()
            if tab_count < self.indent and self.curr_token.type != NEWLINE_T:
                for _ in range(tab_count):
                    self.prev_tokens()
                self.indent -= 1
                if self.curr_token.type != EOF_T: self.prev_tokens()
                break
            elif tab_count > self.indent:
                return None, IndentationError(self.curr_token.line, self.curr_token.col,
                                              self.indent)

            if self.curr_token.type == NEWLINE_T:
                self.next_token()
                continue

            if self.curr_token.match(KEYWORD_T, FUNC_T):
                self.next_token()
                func, error = self.function_definition()
                if error: return None, error
                methods.append(func)

            elif self.curr_token.match(KEYWORD_T, INIT_T):
                init, error = self.function_definition()
                if error: return None, error


            elif self.curr_token.type == IDENTIFIER_T:
                identifier = self.curr_token
                self.next_token()
                if self.curr_token.type != EQUAL_T:
                    return None, IllegalSyntaxError(self.curr_token.line, 
                                                    self.curr_token.col,
                                                    "Equal Sign expected")
                self.next_token()
                expr, error = self.experssion()
                if error: return None, error
                attributes.append(VarAssignNode(identifier, expr))
            else:
                return None, IllegalSyntaxError(self.curr_token.line, 
                                                self.curr_token.col,
                                                "Not a var or a method")
        return ClassDefNode(class_name, parent, init, attributes, methods), None


            
        
        

            
        
    