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
        self.line = op_token.line
        self.col = op_token.col

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
        self.line = value.line
        self.col = value.col

    def __repr__(self):
        return f'({str(self.name)} = {self.value})'

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
    
class StringNode:
    def __init__(self, string):
        self.string = string
        self.line = self.string.line
        self.col = self.string.col

    def __repr__(self):
        return f'"{self.string.value}"'
    
class ArrayNode:
    def __init__(self, array, line, col):
        self.array = array
        self.line = line
        self.col = col

    # def __repr__(self):
    #     return self.array

class FunctionDefNode:
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body
        self.line = self.name.line
        self.col = self.name.col

    def __repr__(self):
        return f'[{self.name.value} ({self.args}):\n ({self.body})]'
    
class ReturnNode:
    def __init__(self, expr):
        self.expr = expr
        self.line = self.expr.line
        self.col = self.expr.line

    def __repr__(self):
        return f'Return: {self.expr}'
    
class ClassDefNode:
    def __init__(self, name, parent, init, attributes, methods):
        self.name = name.value
        self.parent = parent
        self.init = init
        self.attributes = attributes
        self.methods = methods
        self.line = name.line
        self.col = name.col

    def __repr__(self):
        return f'[Class: <{self.name}>]'
    
class BuiltInFuncNode:
    def __init__(self, name, args):
        self.args = args
        self.name = name.value
        self.line = name.line
        self.col = name.col
