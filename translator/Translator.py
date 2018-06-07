import sys
import ast

parenthesis = 0
brackets = 0
variable_declaration = ''
setup = ''
functions = {}


class MyVisitor(ast.NodeVisitor):
    def visit_Str(self, node, depth=None):
        if depth is not None:
            self.depth_visit_Str(node, depth)
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

    def depth_visit_Str(self, node, depth):
        global function_def
        depth += 1
        for index, text in enumerate(node):
            if len(node) > index > 0:
                function_def += ', '
            if isinstance(text, ast.Call):
                self.visit_Call(text, depth)
            elif isinstance(text, ast.Num):
                self.visit_Num(text, depth)
            elif isinstance(text, ast.Name):
                self.visit_Name(text, depth)
            elif isinstance(text, ast.Str):
                function_def += text.s
                print(' Found String: "' + text.s + '"')
            elif isinstance(text, ast.BinOp):
                self.visit_BinOp(text, depth)

    def visit_Name(self, node, depth=None, is_call=False):
        if depth is not None:
            self.depth_visit_Name(node, depth, is_call)
        else:
            self.general_visit_Name(node)

    def general_visit_Name(self, node):
        global variable_declaration
        global setup
        global function_def
        if isinstance(node, list):
            for nod in node:
                self.visit_Name(nod)
        elif node.id != 'halduino':
            variable_declaration += 'int ' + node.id + ' = '
            if node.id != 'timeUS' and node.id != 'distanceUS':
                setup += 'pinMode(' + node.id + ','
            else:
                function_def += node.id + ' = '
            print('Name: ' + node.id)

    def depth_visit_Name(self, node, depth, is_call=False):
        global function_def
        depth += 1
        separator = ' ' + depth * '-'
        if isinstance(node, ast.Add):
            print(separator + ' Add: ' + str(node))
            if function_def is not None:
                function_def += ' + '
        elif isinstance(node, ast.Div):
            self.visit_Div(node)
        elif isinstance(node, ast.Num):
            self.visit_Num(node, depth)
        else:
            if is_call is False and function_def is not None:
                if node.id == 'str':
                    function_def += 'String'
                else:
                    function_def += node.id
            print(separator + ' Name: ' + node.id)

    def visit_FunctionDef(self, node):
        depth = 0
        global function_def
        global brackets
        global functions

        function_def = node.name + '('
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
        function_def += '}\n'
        try:
            function_def = str(node.returns.id) + ' ' + function_def + '\n'
            print('RETURNS -> ' + str(node.returns.id))
            # Add the function definition to a functions list
            functions[node.name] = function_def
            self.visit_Name(node.returns, depth)
        except AttributeError:
            function_def = 'void ' + function_def
            functions[node.name] = function_def

    def visit_Expr(self, node, depth=None):
        if depth is None:
            self.general_visit_Expr(node)
        else:
            self.depth_visit_Expr(node, depth)

    def general_visit_Expr(self, node):
        if isinstance(node, list):
            for nod in node:
                print(' Expression: ' + str(nod.value))
                self.visit_Call(nod.value, 1)
        elif isinstance(node.value, ast.Str):
            self.visit_Str(node.value, 1)
        else:
            print(' Expression: ' + str(node.value))
            self.visit_Call(node.value, 1)

    def depth_visit_Expr(self, node, depth):
        depth += 1
        separator = ' ' + depth * '-'
        if isinstance(node, list):
            for nod in node:
                print(separator + ' Expression: ' + str(nod.value))
                self.visit_Call(nod.value, depth)
        else:
            print(separator + ' Expression: ' + str(node.value))
            self.visit_Call(node.value, depth)

    def visit_Call(self, node, depth):
        global function_def
        global parenthesis
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Call: ' + str(node.func))
        if isinstance(node.func, ast.Attribute):
            parenthesis += 1
            self.visit_Attribute(node.func)
        else:
            function_name = node.func.id
            if function_name == 'print':
                function_name = 'Serial.' + function_name
            if function_name == 'sleep':
                function_def += 'delay('
            else:
                function_def += function_name + '('
            parenthesis += 1
            self.visit_Name(node.func, depth, True)
        # ARGUMENTS
        self.visit_Str(node.args, depth)
        parenthesis -= 1
        if parenthesis == 0:
            function_def += ');\n   '
        else:
            function_def += ')'

    def visit_Num(self, node, depth=None):
        if depth is not None:
            self.depth_visit_Num(node, depth)
        else:
            self.general_visit_Num(node)

    def general_visit_Num(self, node):
        global variable_declaration
        global setup
        variable_declaration += str(node.n) + ';\n'
        print('Num: ' + str(node.n))

    def depth_visit_Num(self, node, depth):
        global function_def
        depth += 1
        separator = ' ' + depth * '-'
        if isinstance(node, list):
            for nod in node:
                print(separator + ' Num: ' + str(nod.n))
                function_def += str(nod.n)
        elif isinstance(node, ast.UnaryOp):
            print(separator + ' UnaryOp: ')
        else:
            print(separator + ' Num: ' + str(node.n))
            function_def += str(node.n)

    def visit_arguments(self, node, depth):
        global function_def
        global brackets
        depth += 1
        separator = ' ' + depth * '-'
        for index, arg in enumerate(node.args):
            self.visit_arg(arg, depth)
            if index < len(node.args) - 1:
                function_def += ', '
        brackets += 1
        function_def += ') {\n'
        print(separator + ' arguments: ' + str(node.args))

    def visit_arg(self, node, depth):
        global function_def
        depth += 1
        separator = ' ' + depth * '-'
        self.visit_Name(node.annotation, depth)
        function_def += ' ' + node.arg
        print(separator + 'arg: ' + node.arg + ' ' + node.annotation.id)

    def visit_Return(self, node, depth):
        global function_def
        depth += 1
        separator = ' ' + depth * '-'
        function_def += '  return '
        if isinstance(node.value, ast.Call):
            self.visit_Call(node.value, depth)
        elif isinstance(node.value, ast.Name):
            self.visit_Name(node.value, depth)
        else:
            print(separator + node.value)
        function_def += ';\n'

    def visit_BinOp(self, node, depth):
        global function_def
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' BinOp')
        if isinstance(node.left, ast.BinOp):
            self.visit_BinOp(node.left, depth)
        else:
            self.visit_Name(node.left, depth)
        self.visit_Name(node.op, depth)
        self.visit_Name(node.right, depth)

    def visit_While(self, node, depth=None):
        if depth is None:
            self.general_visit_While(node)
        else:
            self.depth_visit_While(node, depth)

    def general_visit_While(self, node):
        print('While: ' + str(node.test))
        self.visit_NameConstant(node.test, 0)
        print(' While: ' + str(node.body))
        self.visit_If(node.body[0], 0)

    def depth_visit_While(self, node, depth):
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' While: ' + str(node.test))

    def visit_NameConstant(self, node, depth):
        global function_def
        if node.value is True:
            function_def += 'true'
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + 'Name Constant: ' + str(node.value))

    def visit_If(self, node, depth):
        global function_def
        global parenthesis
        global brackets
        depth += 1
        separator = ' ' + depth * '-'
        function_def += 'if ('
        parenthesis += 1
        # TEST PART OF IF
        if isinstance(node.test, ast.Compare):
            self.visit_Compare(node.test, depth)
        else:
            self.visit_NameConstant(node.test, depth)
        brackets += 1
        function_def += ') {\n  '
        parenthesis -= 1
        for body_part in node.body:
            if isinstance(body_part, ast.Expr):
                self.visit_Expr(body_part, depth)
        for or_else_part in node.orelse:
            if isinstance(or_else_part, ast.If):
                print(separator + ' ElIf')
                brackets -= 1
                function_def += '} else '
                self.visit_If(or_else_part, depth)
            elif isinstance(or_else_part, ast.Expr):
                print(separator + ' Else')
                brackets += 1
                function_def += '} else {\n   '
                self.visit_Expr(or_else_part, depth)
                brackets -= 1
                if brackets >= 0:
                    function_def += '}'
        brackets -= 1
        if brackets > 0:
            function_def += '}\n'

    def visit_Compare(self, node, depth):
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Comparision')
        # LEFT PART
        if isinstance(node.left, ast.Call):
            self.visit_Call(node.left, depth)
        elif isinstance(node.left, ast.Name):
            self.visit_Name(node.left, depth)
        # OPERATOR
        if isinstance(node.ops[0], ast.Gt):
            self.visit_Gt(depth)
        elif isinstance(node.ops[0], ast.Lt):
            self.visit_Lt(depth)
        elif isinstance(node.ops[0], ast.Eq):
            self.visit_Eq(depth)
        elif isinstance(node.ops[0], ast.LtE):
            self.visit_LtE(depth)
        # COMPARATORS
        self.visit_Num(node.comparators, depth)

    def visit_Assign(self, node, depth=None):
        if depth:
            self.depth_visit_Assign(node)
        else:
            self.general_visit_Assign(node)

    def general_visit_Assign(self, node):
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
            for val in node.value:
                print('Assign: ' + val)
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
        else:
            print('Assign: ' + node.value)
        print('Assign ' + str(node.targets) + ' ' + str(node.value))

    def depth_visit_Assign(self, node):
        print('Assign ' + str(node.targets) + ' ' + str(node.value))

    def visit_Attribute(self, node):
        print(' Attribute: ' + str(node.value) + str(node.ctx) + str(node.attr))
        global function_def
        global functions
        if isinstance(node.value, ast.Name):
            self.visit_Name(node.value)
            if node.value.id == 'halduino':
                function_def += node.attr + '('
                print('Halduino found with call to function ' + node.attr)
                halduino = open('./HALduino/halduino.ino', 'r')
                notFound = True
                notEOF = True
                line = ''
                while notFound and notEOF:
                    line = halduino.readline()
                    if len(line) > 0:
                        parts = line.split(' ')  # +|\([^\)]*\)
                        if len(parts) > 1:
                            if parts[1].split('(')[0] == node.attr:
                                notFound = False
                    else:
                        notEOF = False
                if notFound == False:
                    function = ''
                    endOfFunction = False
                    while not endOfFunction:
                        function += line
                        line = halduino.readline()
                        l = line.rstrip()
                        if not l or len(line) <= 0:
                            endOfFunction = True
                    functions[node.attr] = function
        print('Attribute: ' + str(node.value) + node.attr)

    def visit_Gt(self, depth):
        global function_def
        function_def += ' > '
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Greater than')

    def visit_Lt(self, depth):
        global function_def
        function_def += ' < '
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Lower than')

    def visit_LtE(self, depth):
        global function_def
        function_def += ' <= '
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Lower than equal')

    def visit_Eq(self, depth):
        global function_def
        function_def += ' == '
        depth += 1
        separator = ' ' + depth * '-'
        print(separator + ' Equal')

    def visit_Div(self, node):
        global function_def
        function_def += ' / '


class MyTransformer(ast.NodeTransformer):
    def visit_Str(self, node):
        return ast.Str('\"' + node.s + '\"')


input_filename = ""
output_filename = "output.ino"

print('ARGS: ' + str(len(sys.argv)))

if len(sys.argv) == 2:
    input_filename = sys.argv[1]
elif len(sys.argv) > 2:
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
else:
    print('Usage: ')
    print('python3 Translator.py [input-file] [output-file]')
    print('python3 Translator.py [input-file]')
    sys.exit(0)

print('FILENAME: ' + input_filename)
print('OUTPUT FILENAME: ' + output_filename)
output = open(output_filename, 'w+')
controller_file = open(input_filename).read()
car_controller = ast.parse(controller_file)
MyTransformer().visit(car_controller)
MyVisitor().visit(car_controller)

output.write(variable_declaration + '\n')
output.write('''void setup() {
    // put your setup code here, to run once:
''' + setup + '''
}\n''')

for key, value in functions.items():
    output.write(value)

print()
output.close()
