import sys
import ast

parentheses = 0
brackets = 0
functions = {}


class MyVisitor(ast.NodeVisitor):
    def visit_Str(self, node, index=0, variable_declaration=False):
        global variable_def
        global function_def
        if isinstance(node, list):
            for index, text in enumerate(node):
                if len(node) > index > 0:
                    function_def += ', '
                if isinstance(text, ast.Call):
                    self.visit_Call(text)
                elif isinstance(text, ast.Num):
                    self.visit_Num(text, variable_declaration=False)
                elif isinstance(text, ast.Name):
                    self.visit_Name(text)
                elif isinstance(text, ast.Str):
                    function_def += text.s
                    print('Found String: "' + text.s + '"')
                elif isinstance(text, ast.BinOp):
                    function_def_no_parentheses = function_def
                    self.visit_BinOp(text)
                    self.addParentheses(text, function_def_no_parentheses)
                elif isinstance(text, ast.Subscript):
                    self.visit_Name(text.value)
                    function_def += '['
                    self.visit_Slice(text.slice)
                    function_def += ']'
                elif isinstance(text, ast.UnaryOp):
                    self.visit_UnaryOp(text)
                else:
                    print(text)
        elif variable_declaration:
            if index == 0 and str(type(node.s).__name__) == 'str':
                variable_def = 'String ' + variable_def
            variable_def += node.s
            print('Found String: "' + node.s + '"')
        else:
            function_def += node.s
            print('Found String: "' + node.s + '"')

    def visit_Name(self, node, is_call=False, variable_declaration=False):
        global function_def
        global variable_def
        if isinstance(node, list):
            for nod in node:
                self.visit_Name(nod, is_call=is_call, variable_declaration=variable_declaration)
        elif isinstance(node, ast.Add):
            print('Add: ' + str(node))
            self.visit_Add()
        elif isinstance(node, ast.Div):
            print('Div: ' + str(node))
            self.visit_Div()
        elif isinstance(node, ast.Sub):
            print('Sub: ' + str(node))
            self.visit_Sub()
        elif isinstance(node, ast.Mult):
            print('Mult: ' + str(node))
            self.visit_Mult()
        elif isinstance(node, ast.Mod):
            print('Mod: ' + str(node))
            self.visit_Mod()
        elif isinstance(node, ast.BinOp):
            print('BinOp: ' + str(node))
            self.visit_BinOp(node)
        elif isinstance(node, ast.Num):
            self.visit_Num(node, variable_declaration=False)
        elif isinstance(node, ast.Str):
            self.visit_Str(node)
        else:
            if variable_declaration is False:
                if is_call is False and function_def is not None and node.id != 'halduino':
                    if node.id == 'str':
                        function_def += 'String'
                    else:
                        function_def += node.id
            else:
                variable_def = node.id
            print('Name: ' + node.id)

    def visit_FunctionDef(self, node):
        global function_def
        global brackets
        global functions
        global variable_def
        variable_def = ''
        function_def = node.name + '('
        print('Function Definition: ' + str(node.name))
        self.visit_arguments(node.args)
        for nod in node.body:
            if isinstance(nod, ast.Expr):
                self.visit_Expr(nod)
            elif isinstance(nod, ast.Return):
                self.visit_Return(nod)
            elif isinstance(nod, ast.If):
                self.visit_If(nod)
            elif isinstance(nod, ast.Assign):
                self.visit_Assign(nod)
            elif isinstance(nod, ast.For):
                self.visit_For(nod)
            else:
                print('Function Def undefined node: ' + nod)
        brackets -= 1
        function_def += '}\n'
        try:
            function_def = str(node.returns.id) + ' ' + function_def + '\n'
            print('Returns -> ' + str(node.returns.id))
            # Add the function definition to a functions list
            functions[node.name] = function_def
            self.visit_Name(node.returns)
        except AttributeError:
            function_def = 'void ' + function_def
            functions[node.name] = function_def

    def visit_Expr(self, node):
        if isinstance(node, list):
            for nod in node:
                print('Expression: ' + str(nod.value))
                self.visit_Call(nod.value)
        elif isinstance(node.value, ast.Str):
            self.visit_Str(node.value)
        else:
            print('Expression: ' + str(node.value))
            self.visit_Call(node.value)

    def visit_Call(self, node):
        global function_def
        global parentheses
        print('Call: ' + str(node.func))
        if isinstance(node.func, ast.Attribute):
            parentheses += 1
            self.visit_Attribute(node.func)
        else:
            function_name = node.func.id
            print(function_name)
            if function_name == 'print':
                function_name = 'Serial.' + function_name
            elif function_name == 'sleep':
                function_name = 'delay'
            try:
                function_def += function_name + '('
            except:
                print('Code must be within a function')
                exit(1)
            parentheses += 1
            self.visit_Name(node.func, is_call=True)
        # ARGUMENTS
        self.visit_Str(node.args)
        parentheses -= 1
        if parentheses == 0:
            function_def += ');\n   '
        else:
            function_def += ')'

    def visit_Num(self, node, index=0, variable_declaration=False):
        global variable_def
        global function_def
        if variable_declaration == True:
            if index == 0:
                variable_def = str(type(node.n).__name__) + ' ' + variable_def
            variable_def += str(node.n)
            print('Num: ' + str(node.n))
        else:
            if isinstance(node, list):
                for nod in node:
                    print('Num: ' + str(nod.n))
                    function_def += str(nod.n)
            elif isinstance(node, ast.UnaryOp):
                print('UnaryOp: ')
            else:
                print('Num: ' + str(node.n))
                function_def += str(node.n)

    def visit_arguments(self, node):
        global function_def
        global brackets
        for index, arg in enumerate(node.args):
            self.visit_arg(arg)
            if index < len(node.args) - 1:
                function_def += ', '
        brackets += 1
        function_def += ') {\n'
        print('arguments: ' + str(node.args))

    def visit_arg(self, node):
        global function_def
        if node.annotation is not None:
            self.visit_Name(node.annotation)
            function_def += ' ' + node.arg
            print('arg: ' + node.arg + ' ' + node.annotation.id)
        else:
            function_def += 'int ' + node.arg
            print('arg: ' + node.arg)

    def visit_Return(self, node):
        global function_def
        function_def += '  return '
        if isinstance(node.value, ast.Call):
            self.visit_Call(node.value)
        elif isinstance(node.value, ast.Name):
            self.visit_Name(node.value)
        else:
            print(node.value)
        function_def += ';\n'

    def visit_BinOp(self, node):
        global function_def
        print('BinOp')
        if isinstance(node.left, ast.BinOp):
            self.visit_BinOp(node.left)
        else:
            self.visit_Name(node.left)
        self.visit_Name(node.op)
        self.visit_Name(node.right)

    def addParentheses(self, node, function_def_no_parentheses):
        # Add Parentheses
        global function_def
        lines = open(input_filename).readlines()
        target_line = lines[node.lineno - 1]
        transformed_line = ''
        notFound = True
        line_index = 0
        while notFound:
            if target_line[line_index] == '(':
                notFound = False
            line_index += 1
        notFound = True
        while notFound:
            if target_line[line_index] == ')' and target_line[line_index + 1] == '\n':
                notFound = False
            else:
                transformed_line += target_line[line_index]
            line_index += 1
        line_to_transform = function_def.splitlines()[len(function_def.splitlines()) - 1]
        if len(line_to_transform.split(transformed_line)) == 1:
            line_index = 0
            copy_index = 0
            new_line = ''
            while line_index < len(transformed_line):
                character = transformed_line[line_index]
                if character == '(':
                    previous_index = line_index
                    following_index = line_index
                    previous_index -= 1
                    following_index += 1
                    if previous_index > 0:
                        previous_char = transformed_line[previous_index]
                        following_char = transformed_line[following_index]
                        copy_index = 0
                        notFound = True
                        while notFound and copy_index < len(line_to_transform) - 1:
                            if line_to_transform[copy_index] == previous_char and line_to_transform[copy_index + 1] == following_char:
                                new_line += '('
                                notFound = False
                            else:
                                new_line += line_to_transform[copy_index]
                            copy_index += 1
                    else:
                        following_char = transformed_line[following_index]
                        copy_index = 0
                        notFound = True
                        while notFound and copy_index < len(line_to_transform) - 1:
                            if line_to_transform[copy_index + 1] == following_char:
                                new_line += '('
                                notFound = False
                            else:
                                new_line += line_to_transform[copy_index]
                            copy_index += 1
                        new_line += '('
                if character == ')':
                    previous_index = line_index
                    following_index = line_index
                    previous_index -= 1
                    try:
                        following_index += 1
                        following_char = transformed_line[following_index]
                    except:
                        following_char = None
                    previous_char = transformed_line[previous_index]
                    notFound = True
                    while notFound and copy_index < len(line_to_transform):
                        if following_char is not None:
                            if line_to_transform[copy_index - 1] == previous_char and line_to_transform[copy_index] == following_char:
                                new_line += ')'
                                notFound = False
                            else:
                                new_line += line_to_transform[copy_index]
                        else:
                            new_line += line_to_transform[copy_index]
                        copy_index += 1
                    if following_char is None:
                        new_line += ')'
                line_index += 1
            while copy_index < len(line_to_transform):
                new_line += line_to_transform[copy_index]
                copy_index += 1
            if new_line != '':
                function_def = function_def[:function_def.rfind('\n')] + ' \n' +  new_line

    def visit_While(self, node):
        print('While: ' + str(node.test))
        self.visit_NameConstant(node.test)
        print(' While: ' + str(node.body))
        self.visit_If(node.body[0])

    def visit_NameConstant(self, node, index=0):
        global function_def
        global variable_def
        boolean_var = ''
        if node.value is True:
            boolean_var = 'true'
        elif node.value is False:
            boolean_var = 'false'
        if variable_def != '':
            variable_def += boolean_var
            if index == 0:
                variable_def = 'boolean ' + variable_def
        else:
            function_def += boolean_var

    def visit_If(self, node):
        global function_def
        global parentheses
        global brackets
        function_def += 'if ('
        parentheses += 1
        # TEST PART OF IF
        if isinstance(node.test, ast.Compare):
            self.visit_Compare(node.test)
        else:
            self.visit_NameConstant(node.test)
        brackets += 1
        function_def += ') {\n  '
        parentheses -= 1
        for body_part in node.body:
            if isinstance(body_part, ast.Expr):
                self.visit_Expr(body_part)
        for or_else_part in node.orelse:
            if isinstance(or_else_part, ast.If):
                print('ElIf')
                brackets -= 1
                function_def += '} else '
                self.visit_If(or_else_part)
            elif isinstance(or_else_part, ast.Expr):
                print('Else')
                brackets += 1
                function_def += '} else {\n   '
                self.visit_Expr(or_else_part)
                brackets -= 1
                if brackets >= 0:
                    function_def += '}\n'
        brackets -= 1
        if brackets > 0:
            function_def += '}\n'

    def visit_Compare(self, node):
        print('Comparision')
        # LEFT PART
        if isinstance(node.left, ast.Call):
            self.visit_Call(node.left)
        elif isinstance(node.left, ast.Name):
            self.visit_Name(node.left)
        # OPERATOR
        if isinstance(node.ops[0], ast.Gt):
            self.visit_Gt()
        elif isinstance(node.ops[0], ast.Lt):
            self.visit_Lt()
        elif isinstance(node.ops[0], ast.Eq):
            self.visit_Eq()
        elif isinstance(node.ops[0], ast.LtE):
            self.visit_LtE()
        # COMPARATORS
        self.visit_Num(node.comparators, variable_declaration=False)

    def visit_Assign(self, node):
        global function_def
        global variable_def
        self.visit_Name(node.targets, variable_declaration=True)
        print('Assign: ' + str(node.value))
        if isinstance(node.value, ast.List):
            variable_def += '[] = {'
            print('List! ' + str(len(node.value.elts)))
            for index, element in enumerate(node.value.elts):
                if index >= 1:
                    variable_def += ','
                if isinstance(element, ast.Num):
                    self.visit_Num(element, index=index, variable_declaration=True)
                elif isinstance(element, ast.NameConstant):
                    self.visit_NameConstant(element, index)
                else:
                    self.visit_Str(element, index=index, variable_declaration=True)
            function_def += variable_def + '};\n'
            variable_def = ''
        elif isinstance(node.value, list):
            for val in node.value:
                print('Assign: ' + val)
        elif isinstance(node.value, ast.Call):
            self.visit_Call(node.value)
        elif isinstance(node.value, ast.Name):
            self.visit_Name(node.value)
        elif isinstance(node.value, ast.BinOp):
            self.visit_BinOp(node.value)
        elif isinstance(node.value, ast.NameConstant):
            variable_def += ' = '
            self.visit_NameConstant(node.value, 0)
            variable_def += ';\n'
            function_def += variable_def
            variable_def = ''
        elif isinstance(node.value, ast.Num):
            variable_def += ' = '
            self.visit_Num(node.value, 0, variable_declaration=True)
            variable_def += ';\n'
            function_def += variable_def
            variable_def = ''
        elif isinstance(node.value, ast.Str):
            variable_def += ' = '
            self.visit_Str(node.value, variable_declaration=True)
            variable_def += ';\n'
            function_def += variable_def
            variable_def = ''
        else:
            print('Assign: ' + str(node.value))
        print('Assign ' + str(node.targets) + ' ' + str(node.value))

    def visit_Attribute(self, node):
        print('Attribute: ' + str(node.value) + str(node.ctx) + str(node.attr))
        global function_def
        global functions
        if isinstance(node.value, ast.Name):
            self.visit_Name(node.value)
            if node.value.id == 'halduino':
                function_def += node.attr + '('
                print('Halduino found with call to function ' + node.attr)
                if len(node.attr.split('get')) > 1:
                    searched_node = node.attr.split('get')[1]
                elif len(node.attr.split('set')) > 1:
                    searched_node = node.attr.split('set')[1]
                elif len(node.attr.split('line')) > 1:
                    searched_node = node.attr.split('line')[1]
                else:
                    searched_node = node.attr.split('stop')[1]
                print(searched_node)
                halduino = open('./HALduino/halduino' + robot + '.ino', 'r')
                notFound = True
                notEOF = True
                line = ''
                declaration_name = ''
                while notEOF:
                    while notFound and notEOF:
                        line = halduino.readline()
                        if len(line) > 0:
                            if len(line.split(searched_node)) > 1:
                                parts = line.split(' ')  # +|\([^\)]*\)
                                declaration_name = parts[1].split('(')[0]
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
                        functions[declaration_name] = function
                        notFound = True
        print('Attribute: ' + str(node.value) + node.attr)

    def visit_For(self, node):
        global function_def
        print('For!')
        print('Target: ' + str(node.target))
        function_def += 'for(int '
        self.visit_Name(node.target)
        function_def += ' = 0; sizeof('
        print('Iterator: ' + str(node.iter))
        self.visit_Name(node.iter)
        function_def += '); x++) {\n'
        print('Body: ' + str(node.body))
        self.visit_Expr(node.body)
        function_def += '}\n'

    def visit_UnaryOp(self, node):
        global function_def
        if isinstance(node.op, ast.UAdd):
            function_def += '+'
        elif isinstance(node.op, ast.USub):
            function_def += '-'
        self.visit_Num(node.operand)
        print('OP: ' + str(node.op))
        print('OPERAND: ' + str(node.operand))
        '''
        'op',
        'operand',
        '''

    def visit_Slice(self, node):
        self.visit_Num(node.value)

    def visit_Gt(self):
        global function_def
        function_def += ' > '
        print('Greater than')

    def visit_Lt(self):
        global function_def
        function_def += ' < '
        print('Lower than')

    def visit_LtE(self):
        global function_def
        function_def += ' <= '
        print('Lower than equal')

    def visit_Eq(self):
        global function_def
        function_def += ' == '
        print('Equal')

    def visit_Div(self):
        global function_def
        function_def += ' / '

    def visit_Sub(self):
        global function_def
        function_def += ' - '

    def visit_Add(self):
        global function_def
        function_def += ' + '

    def visit_Mult(self):
        global function_def
        function_def += ' * '

    def visit_Mod(self):
        global function_def
        function_def += ' % '


class MyTransformer(ast.NodeTransformer):
    def visit_Str(self, node):
        return ast.Str('\"' + node.s + '\"')

robot=''
input_filename = ''
output_filename = 'output.ino'

print('ARGS: ' + str(len(sys.argv)))

if len(sys.argv) == 3:
    input_filename = sys.argv[1]
    robot = sys.argv[2]
elif len(sys.argv) > 4:
    input_filename = sys.argv[1]
    robot = sys.argv[2]
    output_filename = sys.argv[3]
else:
    print('Usage: ')
    print('python3 Translator.py [input-file] [robot] [output-file]')
    print('python3 Translator.py [input-file] [robot]')
    sys.exit(0)

print('FILENAME: ' + input_filename)
print('ROBOT: ' + robot)
print('OUTPUT FILENAME: ' + output_filename)
output = open(output_filename, 'w+')
controller_file = open(input_filename).read()
parsed_file = ast.parse(controller_file)
MyTransformer().visit(parsed_file)
MyVisitor().visit(parsed_file)

if 'setup' not in functions:
    functions['setup'] = '''void setup() {
    }\n'''

if 'loop' not in functions:
    functions['loop'] = '''void loop() {
        }\n'''

if robot == 'Complubot':
    # Modify setup to include Robot.begin()
    setup = '\n'
    for index, line in enumerate(functions['setup'].splitlines()):
        if index == 1:
            setup += '\n   Robot.begin();\n'
        setup += line
    setup += '\n'
    functions['setup'] = setup
    output.write('#include <ArduinoRobot.h> // include the robot library\n')

for key, value in functions.items():
    output.write(value)

print()
output.close()
