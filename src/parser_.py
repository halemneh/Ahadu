from src.lexer import Token
from resources.constants import *
from resources.error import IllegalSyntaxError, IndentationError
from resources.nodes import *

# =======================================================================================
# =======================================================================================
class Parser:
    """
    The parser converts the list of token passed to it from the lexer to an AST
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.indent = 0
        self.next_token()

    def next_token(self):
        """
        Returns the next token in self.tokens after assigning it to self.curr_token and 
        advancing self.index by one.
        """
        self.index += 1
        if self.index < len(self.tokens):
            self.curr_token = self.tokens[self.index]
        return self.curr_token
    
    def prev_tokens(self):
        """
        Returns the prevous token in self.tokens after assigning it to self.curr_token 
        and reversing self.index by one.
        """
        self.index -= 1
        if self.index >= 0:
            self.curr_token = self.tokens[self.index]
        return self.curr_token
    
    def parse(self):
        """
        Returns an node object and an error if there is any after parsing self.tokens
        """
        nodes, error = self.program()
        if error: return None, error
        
        if not error and self.curr_token.type != EOF_T:
            print(self.curr_token)
            print(nodes)
            return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col, 
                                            'Incomplete expression#')
        return nodes, None
    
    def program(self):
        """
        Returns a list of statements after parsing a block of the program. 
        
        Note: A block program is a list of consecutive statements that have the same 
        indentation level. Blocks of program can be nested within another block in which 
        case the nested prgeam will have one more indentation than the outer block.
        A statement can be an expression, an if statement, a while statement, a function 
        definition, or a class definition each separated by a new line. 
        """
        program = []
        expr = None
        done = False

        # Skip newlines until the first non-newline token
        while self.curr_token.type == NEWLINE_T:
            self.next_token()

        tab_count = 0
        while self.curr_token.type == TAB_T:
            tab_count += 1
            self.next_token()

        """ 
        If the number of tabs at the start of the newline is less than the previous 
        statements then that block of program is done. And if there are more indentation
        tokens than expected we return an Indentation error.
        """
        if tab_count < self.indent:
            for _ in range(tab_count):
                self.prev_tokens()
            done = True
        elif tab_count > self.indent:
            return None, IndentationError(self.curr_token.line, self.curr_token.col, 
                                          self.indent)

        if self.curr_token.match(KEYWORD_T, CLASS_T):
            """ Looks for a class defintions. """
            self.next_token()
            obj, error = self.class_definition()
            if error: return None, error
            program.append(obj)
        else:
            """ Parse an expression as a statement. """
            expr, error = self.experssion()
            if error: return None, error
            program.append(expr)
            if isinstance(expr, ReturnNode):
                """ A return node marks an end of a block of statements."""
                while self.curr_token.type == NEWLINE_T:
                    self.next_token()
                return ProgramNode(program), None

        while True:
            line_count = 0
            while self.curr_token.type == NEWLINE_T:
                line_count += 1
                self.next_token()

            if line_count == 0: done = True

            if done:
                """
                The only case in which an expression is not followed by a newline is if 
                we are at the end of the program, we have an incomplete expression or if
                it is an if or while statemets since if and while statements begin with
                the if/whie condition as an expression. This if statements checks for 
                that.
                """
                if self.curr_token.match(KEYWORD_T, IF_T):
                    self.next_token()
                    if_condition = program.pop()
                    if_statment, error = self.if_statement(if_condition)
                    if error: return None, error
                    program.append(if_statment)
                    done = False
                elif self.curr_token.match(KEYWORD_T, WHILE_T):
                    self.next_token()
                    while_condition = program.pop()
                    if_statment, error = self.while_statement(while_condition)
                    if error: return None, error
                    program.append(if_statment)
                    done = False
                elif isinstance(expr, FunctionDefNode):
                    done = False

            if done or self.curr_token.type == EOF_T: 
                """ 
                We break out of the loop if there are no newlines or if the next token 
                is EOF.
                """
                break
            if self.curr_token.type == NEWLINE_T: continue
        
            """ Removes tab tokens and checks the indentations rules are followed. """
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
                """ Checks for class defintion. """
                self.next_token()
                obj, error = self.class_definition()
                if error: return None, error
                program.append(obj)
            else:
                """ Parse an expression as a statement. """
                expr, error = self.experssion()
                if error: return None, error
                program.append(expr)
                if isinstance(expr, ReturnNode): 
                    """ A return node marks an end of a block of statements."""
                    while self.curr_token.type == NEWLINE_T:
                        self.next_token()
                    return ProgramNode(program), None
        return ProgramNode(program), None
    
    def experssion(self):
        """
        Parses an expression.
        An expression can be a BinaryNode, UnaryNode, a number, string, or array nodes, 
        a variable assign or access node or a return statement.
        """     
        if self.curr_token.type == IDENTIFIER_T:
            """ 
            Looks for a variable assignment. The variable can be an attribute of an 
            object hence why the check for a dot token which is a way of accessing an 
            attribute or method of an object. If there is no equals token after the 
            variable, we back track to the start of the identifier token and look for a 
            comparison and/or arthimetic experssion.
            """
            start_index = self.index
            identifier = self.curr_token
            self.next_token()
            if self.curr_token.type == DOT_T:
                self.prev_tokens()
                call, error = self.unit()
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
            """ 
            If the first token in the experssion is a keyword of value RETURN we return a 
            ReturnNode.
            """
            self.next_token()
            return_expr = None
            if self.curr_token.type != NEWLINE_T:
                return_expr, error = self.experssion()
                if error: return None, error
            return ReturnNode(return_expr), None
        return self.binary_operation(self.comparison_expression, ((KEYWORD_T, AND_T),
                                                                  (KEYWORD_T, OR_T)))
    
    def binary_operation(self, func_for_left, ops, func_for_right=None):
        """
        Parses two or more expressions, factor, or units joined by the operation listed 
        in in the paremeter ops. The method returns only the left side of the possible
        binary operation if it not followed by the operations listed in ops.
        
        Note: func_for_left is the method to parse the left most node of the binary 
        operation while func_for_right is method tyo parse the subsequent nodes attached 
        to the left node.
        """
        if func_for_right == None:
            func_for_right = func_for_left

        left, error = func_for_left()
        if error: return None, error

        while self.curr_token.type in ops or (
                self.curr_token.type, self.curr_token.value) in ops:
            op_tok = self.curr_token
            self.next_token()
            right, err = func_for_right()
            if err: return None, err
            left = BinaryOpNode(left, op_tok, right)
        return left, None

    def comparison_expression(self):
        """
        Parses comparison expressions which are an arithmetic experssion or more joined 
        by '<', '<=', '>', '>=', '==', or '!='. It also parses negations at the begining 
        of other experssions.
        """
        token = self.curr_token
        if token.match(KEYWORD_T, NOT_T):
            self.next_token()
            expr, error = self.comparison_expression()
            if error: return None, error
            return UnaryOpNode(token, expr), None
        return self.binary_operation(self.arithmetic_expression, (EQ_T, LT_T, LTE_T, GTE_T, 
                                                           GT_T, GTE_T, NEQ_T))
    
    def arithmetic_expression(self):
        """
        Parses arithmetic experssions which are one or more terms that are joined by '+' 
        or '-' tokens.
        """
        return self.binary_operation(self.term, (PLUS_T, MINUS_T))
    
    def term(self):
        """
        Parses terms which are one or more factor joined by multiplication or division.
        """
        return self.binary_operation(self.factor, (MULT_T, DIVIDE_T))
    
    def factor(self):
        """
        Parses factors which can be number, string or array literals. They can also be an
        exponential experssion (a^b), variable accesses, functions calls or object 
        defintions.
        """
        token = self.curr_token
        if token.type in (PLUS_T, MINUS_T):
            self.next_token()
            number, error = self.factor()
            if error: return None, error
            return UnaryOpNode(token, number), None
        return self.exponential_expression()
    
    def exponential_expression(self):
        """
        Parses exponential expressions is they exist or calls unit() if they don't. 
        Exponential expressions have a unit bases and an factor exponents.
        """
        return self.binary_operation(self.unit, (POWER_T, ), self.factor)

    def unit(self):
        """
        Parses units. Units are the bases of expressions. They can be numbers, string or 
        array literals, identifiers (variable accesses), function definitions, function 
        calls, object defintions.
        """
        token = self.curr_token
        if token.type == INT_T:
            """ Parses numbers. """
            self.next_token()
            return NumberNode(token), None
        
        elif token.type == STRING_T:
            """ Parses string literals. """
            self.next_token()
            return StringNode(token), None
        
        elif token.type == LBRACKET_T:
            """ Parses array literals. """
            self.next_token()
            array, error = self.list_literal()
            if error: return None, error
            if self.curr_token.type == RBRACKET_T:
                self.next_token()
                return ArrayNode(array, token.line, token.col), None
            self.prev_tokens()
            return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col,
                                            RBRACKET_MISSING_ERROR)
        
        elif token.type == IDENTIFIER_T:
            """ 
            Parses variable accesses. These can be just identifiers and attributes or 
            with indexing or slicing information for arrays and strings, with arguments
            for function functions and methods calls.
            """
            self.next_token()

            if self.curr_token.type == LBRACKET_T:
                """ Parse identifiers followed by slicing or indexing information. """
                self.next_token()
                index, op, error = self.index_or_slice()
                if error: return None, error
                if self.curr_token.type == RBRACKET_T:
                    self.next_token()
                    return BinaryOpNode(VarAccessNode(token), op, index), None
                self.prev_tokens()
                return None, IllegalSyntaxError(self.curr_token.line, 
                                                self.curr_token.col, 
                                                RBRACKET_MISSING_ERROR)
            
            elif self.curr_token.type == LPARAM_T:
                """ Parse function calls. """
                self.next_token()
                args, error = self.list_literal(True)
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
                """ Parses calls to attributes and methods of objects. """
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
                    args, error = self.list_literal(True)
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
            """ 
            Parses function definition by calling the function_definiton() which 
            returns a FunctionDefintionNode.
            """
            self.next_token()
            func, error = self.function_definition()
            if error: return None, error
            return func, None
        
        elif token.type == LPARAM_T:
            """ Parses expressions within parenthesises. """
            self.next_token()
            experssion, error = self.experssion()
            if error: return None, error
            if self.curr_token.type == RPARAM_T:
                self.next_token()
                return experssion, None
            self.prev_tokens()
            return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col,
                                            RPARAM_MISSING_ERROR)
        
        elif token.type == KEYWORD_T and token.value in BUILT_IN_FUNCS:
            """ Parses calls to built-in functions. """
            self.next_token()
            if self.curr_token.type != LPARAM_T:
                return None, IllegalSyntaxError(self.curr_token.line, 
                                                self.curr_token.col,
                                                "'(' expected")
            self.next_token()
            args, error = self.list_literal(True)
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
    
    def list_literal(self, PARAN = False):
        """
        Parses and returns a list of expressions that are separated by a comma token and
        are bounded by brackets '[]' or parenthesises '()' if PARAM is set to true.
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
    
    def index_or_slice(self):
        """
        Parses an index or a range of index information that are specified by pussing a 
        colon between two indicies.
        """
        op = Token(SLICE_T, self.curr_token.line, self.curr_token.col)
        if self.curr_token.type == COLON_T:
            self.next_token()
            if self.curr_token.type == RBRACKET_T:
                return (None, None), op, None
            end, error = self.arithmetic_expression()
            if error: return None, None, error
            return (None, end), op, None
        elif self.curr_token.type == RBRACKET_T:
            return None, None, IllegalSyntaxError(self.curr_token.line, 
                                                  self.curr_token.col, "Index Missing")
        else:
            start, error = self.arithmetic_expression()
            if error: return None, None, error
            if self.curr_token.type == COLON_T:
                self.next_token()
                if self.curr_token.type == RBRACKET_T:
                    return (start, None), op, None
                end, error = self.arithmetic_expression()
                if error: return None, None, error
                return (start, end), op, None
            else:
                op = Token(AT_T, self.curr_token.line, self.curr_token.col)
                return start, op, None



    def if_statement(self, if_condition):
        """
        Parses an if statement with the condition for the if statement alreay parsed and 
        passed to it by the called. An if statement can be just an if case or include 
        several else if cases and an else case. 
       
        Note: Inline if statements are allowed. In a block if statement structure the 
        statments for each case are parsed as blocks of program with one more indentation 
        at the start of each line than the lines with the condition expressions. But it 
        is possible to have some of the else if cases and the else case be an inline
        expression within a block if statement. 
        """
        cases = []
        else_case = None

        if self.curr_token.type != THEN_T and (self.curr_token == NEWLINE_T):
            return None, IllegalSyntaxError(self.curr_token.line, self.curr_token.col, 
                                            "Expected ':-' ")
        if self.curr_token.type == THEN_T:
            self.next_token()
        
        if self.curr_token.type == NEWLINE_T:
            """ A block if statement structure. """
            self.indent += 1
            if_statement, error = self.program()
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
                """ Parses the else if cases if they exist. """
                self.next_token()
                elif_condition, error = self.experssion()
                if error: return None, error

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
                    self.indent += 1
                    elif_statement, error = self.program()
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
                """ Parses the else case if it exists. """
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
                    else_case, error = self.program()
                    if error: return None, error
                    self.indent -= 1

                else:
                    self.next_token()
                    else_case, error = self.experssion()
                    if error: return None, error
        else:
            """ An inline is statement. """
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
    
    def while_statement(self, while_condition):
        """
        Parses and returns a WhileNode for while statements with the while condition 
        already parsed and passed to it by the caller.
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
            return WhileNode(while_condition, expr), None
        self.indent += 1
        statement, error = self.program()
        if error: return None, error
        self.indent -= 1
        return WhileNode(while_condition, statement), None

    def function_definition(self):
        """
        Parses and returns a FunctionDefNode for a function defintion. The method assumes
        the called has found the FUNC_T token which marks the start of a function 
        defintion. So, the methods starts by looking for the name, identifier, of the
        function.
        """
        if self.curr_token.type != IDENTIFIER_T and not self.curr_token.match(KEYWORD_T, 
                                                                              INIT_T):
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
            """ Parses the parameters of the function. """
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

        """ A block function defintion. """
        if self.curr_token.type == NEWLINE_T:
            self.next_token()
            self.indent += 1
            body, error = self.program()
            if error: return None, error
            self.indent -= 1

            return FunctionDefNode(func_name, args, body), None
        
        """ An inline function defintion. """
        body, error = self.experssion()
        if error: return None, error
        return FunctionDefNode(func_name, args, body), None
    
    def class_definition(self):
        """
        Parses and returns a ClassDefNode for a class defintion. 
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

        """ Checks if the class inherits from a parent class. """
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
            """ 
            The methods and attributes need to start with one more indentation than 
            the program. 
            """
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
                """ Class methods. """
                self.next_token()
                func, error = self.function_definition()
                if error: return None, error
                methods.append(func)

            elif self.curr_token.match(KEYWORD_T, INIT_T):
                """ Class init function. """
                init, error = self.function_definition()
                if error: return None, error

            elif self.curr_token.type == IDENTIFIER_T:
                """ Class attributes. """
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
    
# =======================================================================================
# =======================================================================================