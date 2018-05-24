import ast

loop = ""

class MyVisitor(ast.NodeVisitor):
    def visit_Str(self, node, depth):
        global loop
        depth += 1
        for index, text in enumerate(node):
            if isinstance(text, ast.Call):
                self.visit_Call(text, depth)
            elif isinstance(text, ast.Num):
                self.visit_Num(text, depth)
                if index < len(node) - 1:
                    loop += ', '
            elif isinstance(text, ast.Str):
                loop += text.s
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

    def visit_Expr(self, node):
        self.general_visit_Expr(node)

    def general_visit_Expr(self, node):
        if isinstance(node, list):
            for nod in node:
                print(' Expression: ' + str(nod.value))
                self.visit_Call(nod.value, 0)
        else:
            print(' Expression: ' + str(node.value))
            self.visit_Call(node.value, 0)

    def visit_Call(self, node, depth):
        global loop
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Call: ' + str(node.func))
        loop += node.func.id + '('
        self.visit_Name(node.func, depth, True)
        self.visit_Str(node.args, depth)
        loop += ');\n   '

    def visit_Num(self, node, depth):
        global loop
        depth += 1
        separator = ' ' + depth * '-'
        if isinstance(node, list):
            for nod in node:
                print(separator + ' Num: ' + str(nod.n))
        elif isinstance(node, ast.UnaryOp):
            print(separator + ' UnaryOp: ')
        else:
            loop += str(node.n)
            print(separator + ' Num: ' + str(node.n))

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
        if isinstance(node.value, ast.BinOp):
            self.visit_BinOp(node.value, depth)
        else:
            print(separator + node.value)
        function += ';\n'

    def visit_BinOp(self, node, depth):
        global function
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' BinOp')
        self.visit_Name(node.left, depth)
        self.visit_Name(node.op, depth)
        self.visit_Name(node.right, depth)


class MyTransformer(ast.NodeTransformer):
    def visit_Str(self, node):
        return ast.Str('str: ' + node.s)


output = open('output.ino', 'w')
output.write('''void setup() {
    // put your setup code here, to run once:

}\n''')
controller_file = open('example.py').read()
car_controller = ast.parse(controller_file)
MyTransformer().visit(car_controller)
MyVisitor().visit(car_controller)


output.write('''\nvoid loop() {
    // put your main code here, to run repeatedly:
   ''' + loop +
'''\n}\n''')
print()
output.close()
