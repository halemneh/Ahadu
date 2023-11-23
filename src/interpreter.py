from type import *
from constants import *
from error import *
from parser_ import ReturnNode, StatementNode, BinaryOpNode

import copy

class Context:
    def __init__(self, name, parent = None, parent_line = None):
        self.name = name
        self.parent = parent
        self.parent_line = parent_line
        self.symbol_table = None

class SymbolTable:
    def __init__(self, parent):
        self.parent = parent
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
        raise Exception(f'No visit_{type(node).__name__} method defined!')
    
    def visit_StatementNode(self, node, context):
        """
        
        """
        value = None
        for expr in node.expr_list:
            value, error = self.visit(expr, context)
            if error: return None, error
            # print(value)
        return value, None
        
    
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
        if node.op_token.type not in (SLICE_T, CALL_T, DOT_T):
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
        elif node.op_token.type == CALL_T:
            args = []
            for arg in node.right_node:
                value, error = self.visit(arg, context)
                if error: return None, error
                args.append(value)

            if isinstance(left, Class):
                object = Object(left).set_context(context).set_position(
                    node.op_token.line, node.op_token.col)
                result, error = self.object_init(object, args)
                if error: return None, error
            else:
                result, error = self.call(copy.deepcopy(left), args, context, 
                                          node.op_token.line, node.op_token.col)
            if error: return None, error
            return result, None
        elif node.op_token.type == DOT_T:
            if not isinstance(left, Object):
                return None, RTError(node.line, node.col, "Invalid Operation!!", context)
            (callee, args) = node.right_node
            if args == None:
                result, error = self.visit(callee, left.obj_context)
                if error: return None, error
            else:
                function, error = self.visit(callee, left.obj_context)
                if error: return None, error
                args_ = []
                for arg in args:
                    value, error = self.visit(arg, context)
                    if error: return None, error
                    args_.append(value)
                result, error = self.call(function, args_, left.obj_context, 
                                          node.op_token.line, node.op_token.col)

        if error:
            return None, error
        else:
            return result.set_position(node.line, node.col).set_context(
                context), None
        
    def object_init(self, object, args):
        """
        
        """
        interpreter = Interpreter()
        # TODO: change name to Amharic
        init_context = Context("init")
        init_context.symbol_table = SymbolTable(None)
        error =  object.init(args, init_context, interpreter, object.line, 
                             object.col)
        if error: return None, error
        return object, None
        
    def call(self, func, args, context, line, col):
        """
        
        """
        interpreter = Interpreter()
        func_context = Context(func.name, context, func.line)
        func_context.symbol_table = SymbolTable(context.symbol_table)
        
        result, error = func.run(args, interpreter, func_context, line, col)
        if error: return None, error
        if func.should_return: result = copy.deepcopy(result)
        return result, None
        
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
        obj_context = context
        identifier = None
        if isinstance(node.name, BinaryOpNode):
            if node.name.op_token.type != DOT_T:
                return None, RTError(node.line, node.col, "Invalid OPs", context)
            obj, error = self.visit(node.name.left_node, context)
            if error: return None, error
            if not isinstance(obj, Object):
                return None, RTError(node.line, node.col, "Invalid OPers", context)
            obj_context = obj.obj_context
            (identifier, args) = node.name.right_node
            if args != None: 
                return None, RTError(node.line, node.col, "Invalid OPers", context)
            _, error = self.visit(identifier, obj_context)
            if error: return None, error
            identifier = identifier.name.value

        else:
            identifier = node.name.value

        value, error = self.visit(node.value, context)
        if error: return None, error

        if value == None:
            return None, RTError(node.line, node.col, 
                                 "Var can't be equal to NoneType", context)
        
        elif isinstance(value, Object):
            value.set_name(identifier)
        obj_context.symbol_table.set(identifier, value)

        # print(obj_context.symbol_table.symbols)
        return value, None
    
    def visit_VarAccessNode(self, node, context):
        """
        
        """
        identifier = node.name.value
        value = context.symbol_table.get(identifier)

        if not value:
            return None, RTError(node.line, node.col, UNDEFINED_IDENTIFIER, 
                                 context, identifier)
 
        return value.set_context(context).set_position(
            node.line, node.col), None
        
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
        
        return None, None
        
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
    
    def visit_FunctionDefNode(self, node, context, add_to_sym = True):
        """
        
        """
        should_rtn  = False
        if isinstance(node.body, StatementNode):
            should_rtn = isinstance(node.body.expr_list[-1], ReturnNode)
        else:
            should_rtn = isinstance(node.body, ReturnNode)
        
        func = Function(node.name.value, node.args, node.body, should_rtn
                        ).set_context(context).set_position(node.line, node.col)
        if add_to_sym: context.symbol_table.set(node.name.value, func)
        return func, None
    
    def visit_ReturnNode(self, node, context):
        """
        
        """
        return_value, error = self.visit(node.expr, context)
        if error: return None, error
        return return_value.set_context(context).set_position(
            node.line, node.col), None    
    
    def visit_ClassDefNode(self, node, context):
        """
        
        """
        attributes = {}
        methods = {}
        if node.parent and context.object_table.get(node.parent) == None:
            return None, RTError(node.line, node.col, 
                                 "Class parent is not defined", 
                                 context)
        for attribute in node.attributes:
            value, error = self.visit(attribute.value, context)
            if error: return None, error
            attributes[attribute.name.value] = value
        
        for method in node.methods:
            value, error = self.visit_FunctionDefNode(method, context, False)
            if error: return None, error
            methods[value.name] = value

        class_symbol_table = SymbolTable(None)
        class_context = Context(node.name)
        class_context.symbol_table = class_symbol_table
        class_def =  Class(node.name, node.parent, node.init, attributes, 
                           methods, class_context).set_context(context
                            ).set_position(node.line, node.col)
        context.symbol_table.set(node.name, class_def)
        return None, None
    
    def visit_BuiltInFuncNode(self, node, context):
        """
        
        """
        args = []
        for arg in node.args:
            arg, error = self.visit(arg, context)
            if error: return None, error
            args.append(arg)

        func = getattr(self, f'built_in_{node.name}', self.unknown_func)
        return func(args, node.line, node.col, context) 
    
    def unknown_func(self, args, line, col):
        raise Exception(f'Unknoen built-in Function')
    
    def built_in_PRINT(self, args, line, col, context):
        if len(args) == 0:
            return None, None
        if len(args) > 1:
            return None, RTError(line, col, NO_OF_ARGS_PASSED, context, 
                                 ("Print", len(args)))
        try: 
            print(args[0])
            return None, None
        except:
            return None, RTError(line, col, "Print Failed", context)