import sys
import ast

parentheses = 0
brackets = 0
functions = {}
has_else_part = False
direction = ''
is_call = False
is_Comparision = False
is_var_declaration = False
is_array = False
array_index = 0
array_length = 0
variable_def = ''


class MyVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        print('NODE generic: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Str(self, node):
        global variable_def
        global function_def
        global is_array
        global array_index
        global array_length
        print('NODE Str: ' + str(type(node.s)))
        str_var = '\"' + node.s + '\"'
        if is_array:
            if array_index == 0:
                str_var = '{' + str_var
            if array_index < array_length - 1:
                str_var += ','
            array_index += 1

        if variable_def != '':
            if is_array:
                variable_def = 'String ' + variable_def + str_var
            else:
                variable_def = 'String ' + variable_def + ' = ' + str_var
            function_def += variable_def
        else:
            function_def += str_var
        variable_def = ''

    def visit_Name(self, node):
        global function_def
        global variable_def
        global is_call
        global is_var_declaration
        global is_array
        if node.id == 'print':
            function_def += 'Serial.' + node.id
        elif node.id == 'sleep':
            function_def += 'delay'
        elif node.id != 'halduino' and is_var_declaration == False:
            function_def += node.id

        if is_call:
            function_def += '('
            is_call = False
        elif is_var_declaration:
            variable_def += node.id
            is_var_declaration = False

        print('NODE Name: ' + str(type(node)) + ' ' + node.id)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        global function_def
        global brackets
        global functions
        global variable_def
        variable_def = ''
        function_def = node.name + '('
        print('Function Definition: ' + str(node.name))
        print('NODE arguments: ' + str(type(node.args)))
        ast.NodeVisitor.generic_visit(self, node)
        brackets -= 1
        function_def += '}\n'
        try:
            function_def = str(node.returns.id) + ' ' + function_def + '\n'
            print('Returns -> ' + str(node.returns.id))
            # Add the function definition to a functions list
            functions[node.name] = function_def
            print('NODE function_def: ' + str(type(node.returns)))
        except AttributeError:
            function_def = 'void ' + function_def
            functions[node.name] = function_def

    def visit_Expr(self, node):
        global direction
        global function_def
        if node == direction:
            function_def += '} else {\n'
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node):
        global function_def
        global parentheses
        global is_call
        global is_Comparision
        is_call = True
        parentheses += 1
        print('NODE Call: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)
        is_call = False
        parentheses -= 1
        if parentheses == 0 and is_Comparision == False:
            print('PARENTHESES ' + str(parentheses))
            function_def += ');\n   '
        else:
            print('PARENTHESES ' + str(parentheses))
            function_def += ')'
            is_Comparision = False

    def visit_Num(self, node):
        global variable_def
        global function_def
        global is_array
        global array_index
        global array_length
        print('NODE Num: ' + str(type(node)))
        num_var = str(node.n)
        if is_array:
            if array_index == 0:
                num_var = '{' + num_var
            if array_index < array_length - 1:
                num_var += ','
            array_index += 1

        if variable_def != '':
            if is_array:
                variable_def = type(node.n).__name__ + ' ' + variable_def + num_var
            else:
                variable_def = type(node.n).__name__ + ' ' + variable_def + ' = ' + num_var
            function_def += variable_def
        else:
            function_def += num_var
        variable_def = ''
        ast.NodeVisitor.generic_visit(self, node)

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
            print('NODE Return: ' + str(type(node.annotation)))
            ast.NodeVisitor.generic_visit(self, node.annotation)
            var_type = node.annotation.id
            if node.annotation.id == 'str':
                var_type = 'String'
            function_def += var_type + ' ' + node.arg
            print('arg 1: ' + node.arg + ' ' + node.annotation.id)
        else:
            function_def += 'int ' + node.arg
            print('arg 2: ' + node.arg)

    def visit_Return(self, node):
        global function_def
        function_def += '  return '
        print(node.value)
        function_def += ';\n'
        print('NODE Return: ' + str(type(node.value)))
        ast.NodeVisitor.generic_visit(self, node.value)

    def visit_BinOp(self, node):
        global function_def
        print('BinOp')
        print('NODE Return: ' + str(type(node.left)) + ' ' + str(type(node.op)) + ' ' + str(type(node.right)))
        ast.NodeVisitor.generic_visit(self, node)

    def addParentheses(self, node):
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
                            if line_to_transform[copy_index] == previous_char and line_to_transform[
                                        copy_index + 1] == following_char:
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
                            if line_to_transform[copy_index - 1] == previous_char and line_to_transform[
                                copy_index] == following_char:
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
                function_def = function_def[:function_def.rfind('\n')] + ' \n' + new_line

    def visit_While(self, node):
        print('NODE While 1: ' + str(type(node.test)))
        ast.NodeVisitor.generic_visit(self, node.test)
        for body_part in node.body:
            print('NODE While 2: ' + str(type(body_part)))
            ast.NodeVisitor.generic_visit(self, body_part)

    def visit_List(self, node):
        global function_def
        global is_array
        global array_index
        global array_length
        global is_var_declaration
        global variable_def
        print('NODE List: ' + str(type(node)) + ' ' + str(type(node.elts)) + ' ' + str(type(node.ctx)) + ' ')
        is_array = True
        array_index = 0
        array_length = len(node.elts)
        variable_def += '[] = '
        ast.NodeVisitor.generic_visit(self, node)
        array_index = 0
        is_array = False
        variable_def += '}'

    def visit_NameConstant(self, node):
        global function_def
        global variable_def
        global is_array
        global array_index
        global array_length
        boolean_var = ''
        if node.value is True:
            boolean_var = 'true'
        elif node.value is False:
            boolean_var = 'false'

        if is_array:
            if array_index == 0:
                boolean_var = '{' + boolean_var
                variable_def = 'boolean ' + variable_def
            if array_index < array_length - 1:
                boolean_var += ','
            array_index += 1

        if variable_def != '':
            if is_array:
                variable_def += boolean_var
            else:
                variable_def += ' = ' + boolean_var
                variable_def = 'boolean ' + variable_def
        else:
            function_def += boolean_var
        print('NODE NameConstant: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Index(self, node):
        global function_def
        function_def += '['
        print('NODE Index: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)
        function_def += ']'

    def visit_If(self, node):
        global function_def
        global parentheses
        global brackets
        global has_else_part
        global direction
        global_if = True
        if has_else_part:
            global_if = False
            function_def += '} else '
        function_def += 'if ('
        brackets += 1
        if len(node.orelse) > 0:
            has_else_part = True
            direction = node.orelse[0]
        else:
            has_else_part = False
        print('NODE If: ' + str(type(node)) + ' ' + str(brackets) + ' ' + str(node.orelse) + ' ' + str(has_else_part))
        ast.NodeVisitor.generic_visit(self, node)
        has_else_part = False
        brackets -= 1
        if global_if:
            function_def += '}\n'

    def visit_Compare(self, node):
        global function_def
        global is_Comparision
        print('Comparision')
        # LEFT PART
        print('NODE Compare 1: ' + str(type(node.left)))
        if isinstance(node.left, ast.Call):
            is_Comparision = True
        print('NODE Compare 2: ' + str(type(node.ops[0])))
        print('NODE Compare 3: ' + str(type(node.comparators)))
        ast.NodeVisitor.generic_visit(self, node)
        function_def += ') {\n'

    def visit_Assign(self, node):
        global function_def
        global variable_def
        global is_var_declaration
        print('Assign ' + str(node.targets) + ' ' + str(node.value))
        is_var_declaration = True
        ast.NodeVisitor.generic_visit(self, node)
        variable_def += ';\n'
        function_def += variable_def
        variable_def = ''

    def visit_Attribute(self, node):
        print('Attribute: ' + str(node.value) + str(node.ctx) + str(node.attr))
        global function_def
        global functions
        global parentheses

        if node.value.id == 'halduino':
            function_def += node.attr
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

        print('NODE Atribute 1: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_For(self, node):
        global function_def
        print('For!')
        print('Target: ' + str(node.target))
        function_def += 'for(int '
        print('NODE For : ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)
        function_def += ' = 0; sizeof('
        function_def += '); x++) {\n'
        function_def += '}\n'

    def visit_UnaryOp(self, node):
        global function_def
        print('NODE Unary 1: ' + str(type(node.op)))
        ast.NodeVisitor.generic_visit(self, node.op)
        print('NODE Unray 2: ' + str(type(node.operand)))
        ast.NodeVisitor.generic_visit(self, node.operand)
        print('OP: ' + str(node.op))
        print('OPERAND: ' + str(node.operand))

    def visit_Slice(self, node):
        print('NODE Unray 2: ' + str(type(node.value)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Gt(self):
        global function_def
        function_def += ' > '
        print('Greater than')

    def visit_Lt(self, node):
        global function_def
        function_def += ' < '
        print('Lower than')

    def visit_LtE(self, node):
        global function_def
        function_def += ' <= '
        print('Lower than equal')

    def visit_Eq(self, node):
        global function_def
        function_def += ' == '
        print('Equal')

    def visit_Div(self, node):
        global function_def
        function_def += ' / '

    def visit_Sub(self, node):
        global function_def
        function_def += ' - '

    def visit_Add(self, node):
        global function_def
        function_def += ' + '

    def visit_Mult(self, node):
        global function_def
        function_def += ' * '

    def visit_Mod(self, node):
        global function_def
        function_def += ' % '


robot = ''
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
