import ast

parenthesis = 0
brackets = 0
variable_declaration = ''
setup = ''
functions = []


class MyVisitor(ast.NodeVisitor):
    def visit_Str(self, node, depth=None, is_loop=False):
        if depth is not None:
            self.depth_visit_Str(node, depth, is_loop)
        else:
            self.general_visit_Str(node)

    def general_visit_Str(self, node):
        global variable_declaration
        global setup
        parts = node.s.split('"')
        if parts[1] != 'INPUT' and parts[1] != 'OUTPUT':
            variable_declaration += parts[1] + ';\n'
        else:
            setup += parts[1] + ');\n'
        print('Found String: "' + node.s + '"')

    def depth_visit_Str(self, node, depth, is_loop=False):
        global loop
        global function
        depth += 1
        for index, text in enumerate(node):
            if len(node) > index > 0:
                function += ', '
            if isinstance(text, ast.Call):
                self.visit_Call(text, depth)
            elif isinstance(text, ast.Num):
                self.visit_Num(text, depth, is_loop)
            elif isinstance(text, ast.Name):
                self.visit_Name(text, depth, is_loop)
            elif isinstance(text, ast.Str):
                function += text.s
                print(' Found String: "' + text.s + '"')

    def visit_Name(self, node, depth=None, isCall=False):
        if depth is not None:
            self.depth_visit_Name(node, depth, isCall)
        else:
            self.general_visit_Name(node)

    def general_visit_Name(self, node):
        global variable_declaration
        global setup
        if isinstance(node, list):
            for nod in node:
                self.visit_Name(nod)
        else:
            variable_declaration += 'int ' + node.id + ' = '
            if node.id != 'timeUS' and node.id != 'distanceUS':
                setup += 'pinMode(' + node.id + ','
            print('Name: ' + node.id)

    def depth_visit_Name(self, node, depth, isCall=False):
        global function
        depth += 1
        separator = ' ' + depth * '-'
        if isinstance(node, ast.Add):
            print(separator + ' Add: ' + str(node))
            if function is not None:
                function += ' + '
        elif isinstance(node, ast.Div):
            self.visit_Div(node, depth)
        elif isinstance(node, ast.Num):
            self.visit_Num(node, depth)
        else:
            if isCall is False and function is not None:
                function += node.id
            print(separator + ' Name: ' + node.id)

    def visit_FunctionDef(self, node):
        depth = 0
        global function
        global brackets
        global functions
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
            elif isinstance(nod, ast.Assign):
                self.visit_Assign(nod, depth)
            else:
                print(nod)
        brackets -= 1
        function += '}\n'
        try:
            function = str(node.returns.id) + ' ' + function
            print('RETURNS -> ' + str(node.returns.id))
            # Add the function string to a list
            functions.append(function)
            self.visit_Name(node.returns, depth)
        except AttributeError:
            function = 'void ' + function
            functions.append(function)

    def visit_Expr(self, node, depth=None, is_loop=False):
        if depth is None:
            self.general_visit_Expr(node, is_loop)
        else:
            self.depth_visit_Expr(node, depth, is_loop)

    def general_visit_Expr(self, node, is_loop=False):
        if isinstance(node, list):
            for nod in node:
                print(' Expression: ' + str(nod.value))
                self.visit_Call(nod.value, 1, is_loop)
        elif isinstance(node.value, ast.Str):
            self.visit_Str(node.value, 1, is_loop)
        else:
            print(' Expression: ' + str(node.value))
            self.visit_Call(node.value, 1, is_loop)

    def depth_visit_Expr(self, node, depth, is_loop=False):
        depth += 1
        separator = ' ' + depth * '-'
        if isinstance(node, list):
            for nod in node:
                print(separator + ' Expression: ' + str(nod.value))
                self.visit_Call(nod.value, depth, is_loop)
        else:
            print(separator + ' Expression: ' + str(node.value))
            self.visit_Call(node.value, depth, is_loop)

    def visit_Call(self, node, depth, is_loop=False):
        global function
        global loop
        global parenthesis
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Call: ' + str(node.func))
        function_name = node.func.id
        if function_name == 'print':
            function_name = 'Serial.' + function_name
        if is_loop is True:
            loop += function_name + '('
        function += function_name + '('
        parenthesis += 1
        self.visit_Name(node.func, depth, True)
        self.visit_Str(node.args, depth, is_loop)
        parenthesis -= 1
        if is_loop:
            if parenthesis == 0:
                loop += ');\n   '
            else:
                loop += ')'
        if parenthesis == 0:
            function += ');\n   '
        else:
            function += ')'

    def visit_Num(self, node, depth=None, is_loop=False):
        if depth != None:
            self.depth_visit_Num(node, depth, is_loop)
        else:
            self.general_visit_Num(node)

    def general_visit_Num(self, node):
        global variable_declaration
        global setup
        variable_declaration += str(node.n) + ';\n'
        print('Num: ' + str(node.n))

    def depth_visit_Num(self, node, depth, is_loop=False):
        global loop
        global function
        depth += 1
        separator = ' ' + depth * '-'
        if isinstance(node, list):
            for nod in node:
                print(separator + ' Num: ' + str(nod.n))
                if is_loop:
                    loop += str(nod.n)
                function += str(nod.n)
        elif isinstance(node, ast.UnaryOp):
            print(separator + ' UnaryOp: ')
        else:
            print(separator + ' Num: ' + str(node.n))
            if is_loop:
                loop += str(node.n)
            function += str(node.n)

    def visit_arguments(self, node, depth):
        global function
        global brackets
        depth += 1
        separator = ' ' + depth * '-'
        for index, arg in enumerate(node.args):
            function += 'int '
            self.visit_arg(arg, depth)
            if index < len(node.args) - 1:
                function += ', '
        brackets += 1
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
        elif isinstance(node.value, ast.Name):
            self.visit_Name(node.value, depth)
        else:
            print(separator + node.value)

    def visit_BinOp(self, node, depth):
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' BinOp')
        self.visit_Name(node.left, depth)
        self.visit_Name(node.op, depth)
        self.visit_Name(node.right, depth)

    def visit_While(self, node, depth=None):
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

    def visit_If(self, node, depth, is_loop=False):
        global loop
        global function
        global parenthesis
        global brackets
        depth += 1
        separator = ' ' + depth * '-'
        if is_loop != False:
            loop += 'if ('
        function += 'if ('
        parenthesis += 1
        self.visit_Compare(node.test, depth, is_loop)
        brackets += 1
        if is_loop != False:
            loop += ') {\n  '
        function += ') {\n  '
        parenthesis -= 1
        for body_part in node.body:
            if isinstance(body_part, ast.Expr):
                self.visit_Expr(body_part, depth, is_loop)
        for or_else_part in node.orelse:
            if isinstance(or_else_part, ast.If):
                print(separator + ' ElIf')
                brackets -= 1
                if is_loop:
                    loop += '} else '
                function += '} else '
                self.visit_If(or_else_part, depth, is_loop)
            elif isinstance(or_else_part, ast.Expr):
                print(separator + ' Else')
                brackets += 1
                if is_loop:
                    loop += '} else {\n   '
                function += '} else {\n   '
                self.visit_Expr(or_else_part, depth, is_loop)
                brackets -= 1
                if is_loop:
                    if brackets >= 0:
                        loop += '}'
                if brackets >= 0:
                    function += '}'
        brackets -= 1
        if brackets > 0:
            function += '}\n'

    def visit_Compare(self, node, depth, is_loop=False):
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Comparision')
        # LEFT PART
        if isinstance(node.left, ast.Call):
            self.visit_Call(node.left, depth, is_loop)
        elif isinstance(node.left, ast.Name):
            self.visit_Name(node.left, depth, is_loop)
        # OPERATOR
        if isinstance(node.ops[0], ast.Gt):
            self.visit_Gt(depth)
        elif isinstance(node.ops[0], ast.Lt):
            self.visit_Lt(depth, is_loop)
        elif isinstance(node.ops[0], ast.Eq):
            self.visit_Eq(depth)
        # COMPARATORS
        self.visit_Num(node.comparators, depth, is_loop)

    def visit_Assign(self, node, depth=None, inFunction=False):
        if depth:
            self.depth_visit_Assign(node, depth, inFunction)
        else:
            self.general_visit_Assign(node, inFunction)

    def general_visit_Assign(self, node, inFunction=False):
        global variable_declaration
        self.visit_Name(node.targets)
        print('Assign: ' + str(node.value))
        if isinstance(node.value, ast.List):
            if isinstance(node.value.elts[0], ast.Num):
                self.visit_Num(node.value.elts[0])
            else:
                self.visit_Str(node.value.elts[0])
            self.visit_Str(node.value.elts[1])
        elif isinstance(node.value, list):
            for value in node.value:
                print('Assign: ' + value)
        elif isinstance(node.value, ast.Call):
            variable_declaration += '0;\n'
            self.visit_Call(node.value, 0)
        elif isinstance(node.value, ast.Name):
            self.visit_Call(node.value, 0)
        elif isinstance(node.value, ast.BinOp):
            variable_declaration += '0;\n'
            self.visit_BinOp(node.value, 0)
            print()
        elif isinstance(node.value, ast.Num):
            variable_declaration += str(node.value) + ';\n'
        print('Assign ' + str(node.targets) + ' ' + str(node.value))

    def depth_visit_Assign(self, node, depth, inFunction=False):
        print('Assign ' + str(node.targets) + ' ' + str(node.value))

    def visit_Gt(self, depth):
        global function
        function += ' > '
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Greater than')

    def visit_Lt(self, depth, is_loop=False):
        global function
        global loop
        if is_loop:
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

    def visit_Div(self, node, depth):
        global function
        function += ' / '


class MyTransformer(ast.NodeTransformer):
    def visit_Str(self, node):
        return ast.Str('\"' + node.s + '\"')


output = open('output.ino', 'w')
controller_file = open('StopnGo.py').read()
car_controller = ast.parse(controller_file)
MyTransformer().visit(car_controller)
MyVisitor().visit(car_controller)

output.write(variable_declaration + '\n')
output.write('''void setup() {
    // put your setup code here, to run once:
''' + setup + '''
}\n''')

for function in functions:
    output.write(function)

output.write('''\nvoid loop() {
    // put your main code here, to run repeatedly:
   ''' + loop +
             '''\n}\n''')
print()
output.close()
