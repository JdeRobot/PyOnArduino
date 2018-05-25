import ast

parenthesis = 0
brackets = 0
variable_declaration = ''
setup = ''

class MyVisitor(ast.NodeVisitor):
    def visit_Str(self, node, depth=None, isLoop=False):
        if depth != None:
            self.depth_visit_Str(node, depth, isLoop)
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

    def depth_visit_Str(self, node, depth, isLoop=False):
        global loop
        global function
        depth += 1
        for index, text in enumerate(node):
            if isinstance(text, ast.Call):
                self.visit_Call(text, depth)
            elif isinstance(text, ast.Num):
                self.visit_Num(text, depth, isLoop)
            elif isinstance(text, ast.Str):
                function += text.s
                print(' Found String: "' + text.s + '"')

    def visit_Name(self, node, depth=None, isCall=False):
        if depth != None:
            self.depth_visit_Name(node, depth, isCall)
        else:
            self.general_visit_Name(node)

   # This is used on the top variable declaration
    def general_visit_Name(self, node):
        global variable_declaration
        global setup
        variable_declaration += 'int ' + node.id + ' = '
        setup += 'pinMode('+node.id+','
        print('Name: ' + node.id)

    def depth_visit_Name(self, node, depth, isCall=False):
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
        global brackets
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
        brackets -= 1
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
        global parenthesis
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Call: ' + str(node.func))
        function_name = node.func.id
        if function_name == 'print':
            function_name = 'Serial.' + function_name
        if isLoop is True:
            loop += function_name + '('
        function += function_name + '('
        parenthesis += 1
        self.visit_Name(node.func, depth, True)
        self.visit_Str(node.args, depth, isLoop)
        parenthesis -= 1
        if isLoop is True:
            if parenthesis == 0:
                loop += ');\n   '
            else:
                loop += ')'
        if parenthesis == 0:
            function += ');\n   '
        else:
            function += ')'

    def visit_Num(self, node, depth=None, isLoop=False):
        if depth != None:
            self.depth_visit_Num(node, depth, isLoop)
        else:
            self.general_visit_Num(node)

    def general_visit_Num(self, node):
        global variable_declaration
        global setup
        variable_declaration += str(node.n) + ';\n'
        print('Num: ' + str(node.n))

    def depth_visit_Num(self, node, depth, isLoop=False):
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
            print(separator + ' Num: ' + str(node.n))
            if isLoop is True:
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
        else:
            print(separator + node.value)
        # function += ';\n'

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

    def visit_If(self, node, depth, isLoop=False):
        global loop
        global function
        global parenthesis
        global brackets
        depth += 1
        separator = ' ' + depth * '-'
        if isLoop != False:
            loop += 'if ('
        function += 'if ('
        parenthesis += 1
        self.visit_Compare(node.test, depth, isLoop)
        brackets += 1
        if isLoop != False:
            loop += ') {\n  '
        function += ') {\n  '
        parenthesis -= 1
        for body_part in node.body:
            if isinstance(body_part, ast.Expr):
                self.visit_Expr(body_part, depth, isLoop)
        for or_else_part in node.orelse:
            if isinstance(or_else_part, ast.If):
                print(separator + ' ElIf')
                brackets -= 1
                if isLoop != False:
                    loop += '} else '
                function += '} else '
                self.visit_If(or_else_part, depth, isLoop)
            elif isinstance(or_else_part, ast.Expr):
                print(separator + ' Else')
                brackets += 1
                if isLoop != False:
                    loop += '} else {\n   '
                function += '} else {\n   '
                self.visit_Expr(or_else_part, depth, isLoop)
                brackets -= 1
                if isLoop != False:
                    if brackets >= 0:
                        loop += '}'
                if brackets >= 0:
                    function += '}'
        brackets -= 1
        if brackets > 0:
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
controller_file = open('StopnGo.py').read()
car_controller = ast.parse(controller_file)
MyTransformer().visit(car_controller)
MyVisitor().visit(car_controller)

output.write(variable_declaration + '\n')
output.write('''void setup() {
    // put your setup code here, to run once:
''' + setup + '''
}\n''')
output.write('''\nvoid loop() {
    // put your main code here, to run repeatedly:
   ''' + loop +
'''\n}\n''')
print()
output.close()
