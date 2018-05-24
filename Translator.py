import ast

'''
    TODO 
    * Currently everything within functions is directly added to the loop function instead of consider adding it to 
    as a function itself.
    * Instead of adding just the return statement to the function as it's done now, we should add the whole function's
    content to the former.
    * The sign ";" should be added just when the final statement comes
'''

class MyVisitor(ast.NodeVisitor):
    def visit_Str(self, node, depth, isLoop=False):
        global function
        depth += 1
        for index, text in enumerate(node):
            if isinstance(text, ast.Call):
                self.visit_Call(text, depth)
            elif isinstance(text, ast.Num):
                self.visit_Num(text, depth, isLoop)
                if isLoop:
                    loop += ', '
            elif isinstance(text, ast.Str):
                function += text.s
                print(' Found String: "' + text.s + '"')

    def visit_Name(self, node, depth, isCall=False):
        global function
        depth += 1
        separator = ' ' + depth * '-'
        if isinstance(node, ast.Add):
            print(separator + ' Add: ' + str(node))
            if function is not None:
                function += ' + '
        else:
            if isCall is False and function is not None:
                function += node.id
            print(separator + ' Name: ' + node.id)

    def visit_FunctionDef(self, node):
        depth = 0
        global function
        function = node.name + '('
        print('Function Definition: ' + str(node.name))
        self.visit_arguments(node.args, depth)
        for nod in node.body:
            if isinstance(nod, ast.Expr):
                self.visit_Expr(nod)
            elif isinstance(nod, ast.Return):
                self.visit_Return(nod, depth)
            elif isinstance(nod, ast.If):
                self.visit_If(nod, depth)
            else:
                print(nod)
        function += '}\n'
        try:
            function = str(node.returns.id) + ' ' + function
            print('RETURNS -> ' + str(node.returns.id))
            output.write(function)
            self.visit_Name(node.returns, depth)
        except AttributeError:
            function = 'void ' + function
            output.write(function)

    def visit_Expr(self, node, depth=None, isLoop=False):
        if depth is None:
            self.general_visit_Expr(node, isLoop)
        else:
            self.depth_visit_Expr(node, depth, isLoop)

    def general_visit_Expr(self, node, isLoop=False):
        if isinstance(node, list):
            for nod in node:
                print(' Expression: ' + str(nod.value))
                self.visit_Call(nod.value, 0, isLoop)
        else:
            print(' Expression: ' + str(node.value))
            self.visit_Call(node.value, 0, isLoop)

    def depth_visit_Expr(self, node, depth, isLoop=False):
        depth += 1
        separator = ' ' + depth * '-'
        if isinstance(node, list):
            for nod in node:
                print(separator + ' Expression: ' + str(nod.value))
                self.visit_Call(nod.value, depth, isLoop)
        else:
            print(separator + ' Expression: ' + str(node.value))
            self.visit_Call(node.value, depth, isLoop)

    def visit_Call(self, node, depth, isLoop=False):
        global function
        global loop
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Call: ' + str(node.func))
        if isLoop is True:
            loop += node.func.id + '('
        function += node.func.id + '('
        self.visit_Name(node.func, depth, True)
        self.visit_Str(node.args, depth)
        if isLoop is True:
            loop += ');\n   '
        function += ');\n   '

    def visit_Num(self, node, depth, isLoop=False):
        global loop
        global function
        depth += 1
        separator = ' ' + depth * '-'
        if isinstance(node, list):
            for nod in node:
                print(separator + ' Num: ' + str(nod.n))
                if isLoop is True:
                    loop += str(nod.n)
                function += str(nod.n)
        elif isinstance(node, ast.UnaryOp):
            print(separator + ' UnaryOp: ')
        else:
            if isLoop != False:
                loop += str(node.n)
            print(separator + ' Num: ' + str(node.n))
            if isLoop is True:
                loop += str(node.n)
            function += str(node.n)

    def visit_arguments(self, node, depth):
        global function
        depth += 1
        separator = ' ' + depth * '-'
        for index, arg in enumerate(node.args):
            function += 'int '
            self.visit_arg(arg, depth)
            if index < len(node.args) - 1:
                function += ', '
        function += ') {\n'
        print(separator + ' arguments: ' + str(node.args))

    def visit_arg(self, node, depth):
        global function
        depth += 1
        separator = ' ' + depth * '-'
        function += node.arg
        print(separator + 'arg: ' + node.arg)

    def visit_Return(self, node, depth):
        global function
        depth += 1
        separator = ' ' + depth * '-'
        function += '  return '
        if isinstance(node.value, ast.Call):
            self.visit_Call(node.value, depth)
        else:
            print(separator + node.value)
        function += ';\n'

    def visit_BinOp(self, node, depth):
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' BinOp')
        self.visit_Name(node.left, depth)
        self.visit_Name(node.op, depth)
        self.visit_Name(node.right, depth)

    def visit_While(self, node=None, depth=None):
        if depth is None:
            self.general_visit_While(node)
        else:
            self.depth_visit_While(node, depth)

    # This is the main loop
    def general_visit_While(self, node):
        global loop
        loop = ""
        print('LOOP While: ' + str(node.test))
        self.visit_NameConstant(node.test, 0)
        print('LOOP While: ' + str(node.body))
        self.visit_If(node.body[0], 0, True)


    def depth_visit_While(self, node, depth):
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' While: ' + str(node.test))

    def visit_NameConstant(self, node, depth):
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + 'Name Constant: ' + str(node.value))

    def visit_If(self, node, depth, isLoop=False):
        global loop
        global function
        depth += 1
        separator = ' ' + depth * '-'
        if isLoop != False:
            loop += 'if('
        function += '   if ('
        self.visit_Compare(node.test, depth, isLoop)
        if isLoop != False:
            loop += ') {\n  '
        function += ') {\n  '
        for body_part in node.body:
            if isinstance(body_part, ast.Expr):
                self.visit_Expr(body_part, depth, isLoop)
        for or_else_part in node.orelse:
            if isinstance(or_else_part, ast.If):
                print(separator + ' ElIf')
                if isLoop != False:
                    loop += '} else '
                function += '} else '
                self.visit_If(or_else_part, depth, isLoop)
            elif isinstance(or_else_part, ast.Expr):
                print(separator + ' Else')
                if isLoop != False:
                    loop += '} else {'
                function += '} else {'
                self.visit_Expr(or_else_part, depth, isLoop)
                if isLoop != False:
                    loop += '}'
                function += '}'
        function += '}\n'

    def visit_Compare(self, node, depth, isLoop=False):
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Comparision')
        # LEFT PART
        if isinstance(node.left, ast.Call):
            self.visit_Call(node.left, depth, isLoop)
        elif isinstance(node.left, ast.Name):
            self.visit_Name(node.left, depth, isLoop)
        # OPERATOR
        if isinstance(node.ops[0], ast.Gt):
            self.visit_Gt(depth)
        elif isinstance(node.ops[0], ast.Lt):
            self.visit_Lt(depth, isLoop)
        elif isinstance(node.ops[0], ast.Eq):
            self.visit_Eq(depth)
        # COMPARATORS
        self.visit_Num(node.comparators, depth, isLoop)


    def visit_Gt(self, depth):
        global function
        function += ' > '
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Greater than')

    def visit_Lt(self, depth, isLoop=False):
        global function
        global loop
        if isLoop != False:
            loop += ' < '
        function += ' < '
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Lower than')

    def visit_Eq(self, depth):
        global function
        function += ' == '
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Equal')


class MyTransformer(ast.NodeTransformer):
    def visit_Str(self, node):
        return ast.Str('\"' + node.s + '\"')


output = open('output.ino', 'w')
output.write('''void setup() {
    // put your setup code here, to run once:

}\n''')
controller_file = open('StopnGo.py').read()
car_controller = ast.parse(controller_file)
MyTransformer().visit(car_controller)
MyVisitor().visit(car_controller)


output.write('''\nvoid loop() {
    // put your main code here, to run repeatedly:
   ''' + loop +
'''\n}\n''')
print()
output.close()
