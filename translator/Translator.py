import sys
import ast
from subprocess import call
from os import chdir, getcwd, makedirs
from shutil import move, rmtree
import platform
import re

try:
    import TranslatorVariables as vars
except ModuleNotFoundError:
    print('Absolute import failed')

class MyVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        print('NODE generic: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Str(self, node):
        print('NODE Str: ' + str(type(node.s)))
        var_type = 'STR'
        if len(node.s) == 1:
            var_type = 'CHAR'
            var_name = 'var' + str(vars.variables_counter)
        else:
            if vars.variable_def != '':
                var_name = vars.variable_def
            else:
                var_name = 'var' + str(vars.variables_counter)

        str_var = '(char*)' + var_name + '.data'
        vars.function_def += 'DynType ' + var_name + ';'
        vars.function_def += var_name + '.tvar = ' + var_type + ';'
        vars.function_def += 'String har' + str(vars.variables_counter) + ' = "' + str(node.s) + '";'
        vars.function_def += 'har' + str(vars.variables_counter) + '.toCharArray(' + var_name + '.data, MinTypeSz);\n'
        vars.variables_counter += 1

        if vars.is_array:
            if vars.array_index == 0:
                str_var = '{' + str_var
            if vars.array_index < vars.array_length - 1:
                str_var += ','
            vars.array_index += 1

        if vars.is_call_parameter:
            if vars.call_index > 0:
                vars.call_def += ','
            vars.call_index += 1
            print('CALL_INDEX_STR ' + str(vars.call_index))

        if vars.variable_def != '':
            if vars.is_array:
                vars.variable_def = var_type + vars.variable_def + str_var
                vars.function_def += vars.variable_def
        else:
            if vars.bin_op:
                vars.function_def += node.s
            else:
                if vars.is_call_parameter:
                    if vars.is_built_in_func:
                        vars.call_def += var_name + '.data'
                    else:
                        vars.call_def += var_name
                else:
                    vars.function_def += str_var
        vars.variable_def = ''

    def visit_Name(self, node):
        print('NODE Name: ' + str(type(node)) + ' ' + node.id)
        if node.id == 'print':
            vars.call_def += 'Serial.' + node.id
            vars.is_built_in_func = True
        elif node.id == 'sleep':
            vars.call_def += 'delay'
            vars.is_built_in_func = True
        elif node.id != 'halduino' and vars.is_var_declaration is False:
            if vars.is_call_parameter:
                if vars.call_index > 0:
                    vars.call_def += ','
                vars.call_index += 1
                print('CALL_INDEX_NAME ' + str(vars.call_index))
            if vars.is_variable:
                vars.function_def += 'atoi(' + node.id + '.data)'
                vars.is_variable = False
            elif vars.is_call or vars.is_call_parameter:
                vars.call_def += node.id
            else:
                vars.function_def += node.id
        if node.id == 'halduino':
            self.add_halduino_function(node)

        if vars.is_call:
            if vars.call_def != '':
                vars.call_def = self.check_last_comma(text=vars.call_def)
            vars.call_def += '('
            vars.is_call = False
            vars.is_call_parameter = True
        elif vars.is_var_declaration:
            vars.variable_def += node.id
            vars.is_var_declaration = False
        elif vars.is_for:
            if vars.for_index == 0:
                vars.function_def += ' = 0; sizeof('
            elif vars.for_index == 1:
                vars.function_def += '); x++) {\n'
            vars.for_index += 1

        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        vars.variable_def = ''
        vars.function_def = node.name + '('
        print('Function Definition: ' + str(node.name))
        print('NODE arguments: ' + str(type(node.args)))
        ast.NodeVisitor.generic_visit(self, node)
        vars.brackets -= 1
        vars.function_def += '}\n'
        try:
            vars.function_def = str(node.returns.id) + ' ' + vars.function_def + '\n'
            print('Returns -> ' + str(node.returns.id))
            # Add the function definition to a functions list
            vars.functions[node.name] = vars.function_def
            print('NODE function_def: ' + str(type(node.returns)))
        except AttributeError:
            vars.function_def = 'void ' + vars.function_def
            vars.functions[node.name] = vars.function_def

    def visit_Expr(self, node):
        if node == vars.direction:
            vars.function_def += '} else {\n'
        if vars.is_if:
            vars.function_def += ') {\n'
            vars.is_if = False
        print('NODE Expr: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node):
        vars.is_call = True
        vars.call_index = 0
        vars.parentheses += 1
        print('NODE Call: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)
        vars.function_def += vars.call_def
        vars.call_def = ''
        vars.is_call = False
        vars.is_call_parameter = False
        vars.is_built_in_func = False
        vars.call_index = 0
        vars.parentheses -= 1
        if vars.parentheses == 0 and vars.is_comparision == False and not vars.bool_op and vars.is_if == False and vars.is_while == False:
            self.check_last_comma()
            print('PARENTHESES ' + str(vars.parentheses))
            vars.function_def += ');\n   '
        else:
            print('PARENTHESES ' + str(vars.parentheses))
            vars.function_def += ')'
            vars.is_comparision = False
        if vars.bin_op:
            vars.bin_op = False

    def visit_Num(self, node):
        print('NODE Num: ' + str(type(node)))
        vars.num_var = str(node.n)
        if vars.is_array:
            if vars.array_index == 0:
                vars.num_var = '{' + vars.num_var
            if vars.array_index < vars.array_length - 1:
                vars.num_var += ','
            vars.array_index += 1

        if vars.is_call_parameter:
            if not vars.is_built_in_func:
                vars.function_def += 'DynType var' + str(vars.variables_counter) + ';'
                vars.function_def += 'var' + str(vars.variables_counter) + '.tvar = ' + str(
                    type(node.n).__name__).upper() + ';'
                vars.function_def += 'String har' + str(vars.variables_counter) + ' = "' + vars.var_sign + str(
                    node.n) + '";'
                vars.function_def += 'har' + str(vars.variables_counter) + '.toCharArray(var' + str(
                    vars.variables_counter) + '.data, MinTypeSz);\n'
                vars.var_sign = ''
            vars.variables_counter += 1

        if vars.variable_def != '':
            if vars.is_array:
                vars.variable_def = type(node.n).__name__ + ' ' + vars.variable_def + vars.num_var
            else:
                var_name = vars.variable_def
                vars.variable_def = 'DynType ' + var_name + ';'
                vars.variable_def += var_name + '.tvar = ' + str(type(node.n).__name__).upper() + ';'
                vars.variable_def += 'String har' + str(vars.variables_counter) + ' = "' + vars.var_sign + str(
                    node.n) + '";'
                vars.variable_def += 'har' + str(
                    vars.variables_counter) + '.toCharArray(' + var_name + '.data, MinTypeSz);\n'
                vars.variables_counter += 1
            vars.function_def += vars.variable_def
        else:
            if vars.is_call_parameter:
                if not vars.is_built_in_func:
                    if vars.call_index > 0:
                        vars.call_def += ','
                    vars.call_index += 1
                    print('CALL_INDEX_NUM ' + str(vars.call_index))
                    vars.call_def += 'var' + str(vars.variables_counter - 1)
                else:
                    vars.call_def += vars.num_var
            else:
                vars.function_def += vars.num_var
        vars.variable_def = ''
        ast.NodeVisitor.generic_visit(self, node)

    def visit_arguments(self, node):
        for list_index, arg in enumerate(node.args):
            self.visit_arg(arg)
            if list_index < len(node.args) - 1:
                vars.function_def += ', '
        vars.brackets += 1
        vars.function_def += ') {\n'
        print('arguments: ' + str(node.args))

    def visit_arg(self, node):
        vars.function_def += 'DynType ' + node.arg
        print('NODE ARG: ' + str(type(node.annotation)))

    def visit_Return(self, node):
        vars.function_def += '  return '
        print(node.value)
        vars.function_def += ';\n'
        print('NODE Return: ' + str(type(node.value)))
        ast.NodeVisitor.generic_visit(self, node.value)

    def visit_BinOp(self, node):
        print('BinOp')
        vars.bin_op = True
        if vars.call_def != '':
            vars.call_def += '('
        else:
            vars.function_def += '('
        print('NODE BinOp: ' + str(type(node.left)) + ' ' + str(type(node.op)) + ' ' + str(type(node.right)))
        ast.NodeVisitor.generic_visit(self, node)
        self.check_last_comma()
        if vars.call_def != '':
            vars.call_def += ')'
        else:
            vars.function_def += ')'

    def visit_While(self, node):
        vars.function_def += 'while('
        print('NODE While 1: ' + str(type(node.test)))
        vars.is_while = True
        ast.NodeVisitor.generic_visit(self, node.test)
        vars.function_def += ') {'
        for body_part in node.body:
            print('NODE While 2: ' + str(type(body_part)))
            ast.NodeVisitor.generic_visit(self, body_part)
        vars.function_def += '}\n'
        vars.is_while = False

    def visit_List(self, node):
        print('NODE List: ' + str(type(node)) + ' ' + str(type(node.elts)) + ' ' + str(type(node.ctx)) + ' ')
        vars.is_array = True
        vars.array_index = 0
        vars.array_length = len(node.elts)
        vars.variable_def += '[] = '
        ast.NodeVisitor.generic_visit(self, node)
        vars.array_index = 0
        vars.is_array = False
        vars.variable_def += '};\n'

    def visit_NameConstant(self, node):
        boolean_var = ''
        if node.value is True:
            boolean_var = 'true'
        elif node.value is False:
            boolean_var = 'false'

        if vars.is_array:
            if vars.array_index == 0:
                boolean_var = '{' + boolean_var
                vars.variable_def = 'boolean ' + vars.variable_def
            if vars.array_index < vars.array_length - 1:
                boolean_var += ','
            vars.array_index += 1

        if vars.variable_def != '':
            if vars.is_array:
                vars.variable_def += boolean_var
            else:
                vars.variable_def = 'DynType var' + str(vars.variables_counter) + ';'
                vars.variable_def += 'var' + str(vars.variables_counter) + '.tvar = BOOL;'
                vars.variable_def += 'String har' + str(
                    vars.variables_counter) + ' = "' + vars.var_sign + boolean_var + '";'
                vars.variable_def += 'har' + str(vars.variables_counter) + '.toCharArray(var' + str(
                    vars.variables_counter) + '.data, MinTypeSz);\n'
                vars.variables_counter += 1
            vars.function_def += vars.variable_def
        else:
            if vars.is_call_parameter:
                if not vars.is_built_in_func:
                    if vars.call_index > 0:
                        vars.call_def += ','
                    vars.call_index += 1
                    print('CALL_INDEX_NAME_CONSTANT ' + vars.call_index)
                    vars.call_def += 'var' + str(vars.variables_counter - 1)
                else:
                    vars.call_def += boolean_var
            else:
                vars.function_def += boolean_var
        vars.variable_def = ''
        print('NODE NameConstant: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)
        if len(vars.bool_op) > 0:
            vars.function_def += vars.bool_op[len(vars.bool_op) - 1]
            vars.bool_op = vars.bool_op[:-1]

    def visit_Index(self, node):
        self.check_last_comma()
        if vars.call_def != '':
            vars.call_def += '['
        else:
            vars.function_def += '['
        print('NODE Index: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)
        self.check_last_comma()
        if vars.call_def != '':
            vars.call_def += ']'
        else:
            vars.function_def += ']'
        if len(vars.bool_op) > 0:
            vars.function_def += vars.bool_op[len(vars.bool_op) - 1]
            vars.bool_op = vars.bool_op[:-1]

    def visit_If(self, node):
        vars.is_if = True
        global_if = True
        if vars.has_else_part:
            global_if = False
            vars.function_def += '} else '
        vars.function_def += 'if ('
        vars.brackets += 1
        if len(node.orelse) > 0:
            vars.has_else_part = True
            vars.direction = node.orelse[0]
        else:
            vars.has_else_part = False
        print('NODE If: ' + str(type(node)) + ' ' + str(vars.brackets) + ' ' + str(node.orelse) + ' ' + str(
            vars.has_else_part) + ' ' + str(node.body))
        ast.NodeVisitor.generic_visit(self, node)
        vars.has_else_part = False
        vars.brackets -= 1
        vars.is_if = False
        if global_if:
            vars.function_def += '}\n'

    def visit_Compare(self, node):
        print('Comparision')
        # LEFT PART
        print('NODE Compare 1: ' + str(type(node.left)))
        if isinstance(node.left, ast.Call):
            vars.is_comparision = True
        else:
            vars.is_variable = True
        print('NODE Compare 2: ' + str(type(node.ops[0])))
        print('NODE Compare 3: ' + str(type(node.comparators)))
        vars.function_def += '('
        ast.NodeVisitor.generic_visit(self, node)
        vars.function_def += ')'
        if len(vars.bool_op) > 0:
            vars.function_def += vars.bool_op[len(vars.bool_op) - 1]
            vars.bool_op = vars.bool_op[:-1]

    def visit_Assign(self, node):
        print('Assign ' + str(node.targets) + ' ' + str(node.value))
        vars.is_var_declaration = True
        ast.NodeVisitor.generic_visit(self, node)
        vars.function_def += vars.variable_def
        vars.variable_def = ''

    def visit_Attribute(self, node):
        print('Attribute: ' + str(node.value) + str(node.ctx) + str(node.attr))
        vars.node_attr = node.attr
        print('NODE Atribute 1: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def add_halduino_function(self, node):
        vars.call_def += vars.node_attr
        print('Halduino found with call to function ' + vars.node_attr)
        halduino = open(vars.halduino_directory + robot + '.ino', 'r')
        print('NODE: ' + vars.node_attr)
        self.search_for_function(halduino, vars.node_attr)

    def search_for_function(self, halduino, searched_node, is_first_search=True):
        function_line = ''
        not_found = True
        not_eof = True
        is_first_non_empty_line = True
        function_start_line = 0
        function_variables_line = 0
        if searched_node not in vars.functions:
            while not_found and not_eof:
                function_line = halduino.readline()
                function_start_line += 1
                if function_line.strip():
                    if is_first_non_empty_line:
                        function_variables_line = function_start_line
                        is_first_non_empty_line = False
                    if re.search('\w+ '+searched_node+'\(.*\) {', function_line):
                        not_found = False
                        not_eof = False
                else:
                    if function_line == '':
                        not_eof = False
                    function_variables_line = function_start_line
                    is_first_non_empty_line = True
            if not_found is False:
                self.add_function(function_line, searched_node, function_variables_line, function_start_line, is_first_search, halduino)
            else:
                if is_first_search:
                    print('Function not found for this robot! ' + searched_node)
                    halduino.close()
                    exit()

    def add_function(self, function_line, searched_node, function_variables_line, function_start_line, is_first_search, halduino):
        function_string = ''
        end_of_function = False
        while not end_of_function:
            function_string += function_line
            function_line = halduino.readline()
            if re.search('\w+\(((\w+, )*\w+)*\)', function_line) and not re.search('\.', function_line):
                function_name = re.search('\w+\(', function_line)
                function_name = re.search('\w+', function_name.group(0))
                if function_name.group(0) not in vars.functions:
                    new_halduino = open(vars.halduino_directory + robot + '.ino', 'r')
                    self.search_for_function(new_halduino, function_name.group(0), is_first_search=False)
            l = function_line.rstrip()
            if not l or len(function_line) <= 0:
                end_of_function = True
        vars.functions[searched_node] = function_string
        if function_variables_line < function_start_line:
            halduino.seek(0)
            for i, line in enumerate(halduino):
                if function_variables_line - 1 <= i < function_start_line - 1:
                    if re.search('[^ ]\w+\(', line) and not re.search('\w+ \w+\(', line):
                        if 'setup' in vars.functions:
                            setup = vars.functions['setup']
                            setup += line
                            vars.functions['setup'] = setup
                        else:
                            setup = 'void setup() {\n'
                            setup += line
                            vars.functions['setup'] = setup
                    else:
                        vars.global_variables[line] = line
        if is_first_search:
            halduino.close()

    def visit_For(self, node):
        print('For!')
        print('Target: ' + str(node.target))
        vars.function_def += 'for(int '
        vars.is_for = True
        vars.for_index = 0
        print('NODE For : ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)
        vars.function_def += '}\n'
        vars.for_index = 0
        vars.is_for = False

    def visit_UnaryOp(self, node):
        print('NODE UnaryOp: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Slice(self, node):
        print('NODE Slice: ' + str(type(node.value)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Gt(self, node):
        if vars.call_def != '':
            vars.call_def += ' > '
        else:
            vars.function_def += ' > '
        print('Greater than')

    def visit_Lt(self, node):
        if vars.call_def != '':
            vars.call_def += ' < '
        else:
            vars.function_def += ' < '
        print('Lower than')

    def visit_LtE(self, node):
        if vars.call_def != '':
            vars.call_def += ' <= '
        else:
            vars.function_def += ' <= '
        print('Lower than equal')

    def visit_Eq(self, node):
        vars.call_index = 0
        if vars.call_def != '':
            vars.call_def += ' == '
        else:
            vars.function_def += ' == '
        print('Equal')

    def visit_Div(self, node):
        vars.call_index = 0
        self.check_last_comma()
        if vars.call_def != '':
            vars.call_def += ' / '
        else:
            vars.function_def += ' / '

    def visit_Sub(self, node):
        vars.call_index = 0
        self.check_last_comma()
        if vars.call_def != '':
            vars.call_def += ' - '
        else:
            vars.function_def += ' - '

    def visit_Add(self, node):
        vars.call_index = 0
        self.check_last_comma()
        if vars.call_def != '':
            vars.call_def += ' + '
        else:
            vars.function_def += ' + '

    def visit_Mult(self, node):
        vars.call_index = 0
        self.check_last_comma()
        if vars.call_def != '':
            vars.call_def += ' * '
        else:
            vars.function_def += ' * '

    def visit_Mod(self, node):
        vars.call_index = 0
        self.check_last_comma()
        if vars.call_def != '':
            vars.call_def += ' % '
        else:
            vars.function_def += ' % '

    def visit_And(self, node):
        vars.bool_op.append(' && ')
        print('NODE And: ' + str(type(node)) + str(len(vars.bool_op)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Or(self, node):
        vars.bool_op.append(' || ')
        print('NODE Or: ' + str(type(node)) + str(len(vars.bool_op)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_BoolOp(self, node):
        print('NODE boolOp: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Load(self, node):
        print('NODE Load: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_USub(self, node):
        vars.var_sign += '-'
        print('NODE USub: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Is(self, node):
        vars.function_def += ' == '
        print('NODE Is: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_IsNot(self, node):
        vars.function_def += ' != '
        print('NODE IsNot: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Pass(self, node):
        print('NODE Pass: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def check_last_comma(self, text=None):
        if text is not None:
            if text[-1:] == ',':
                return text[:-1]
            return text
        else:
            if vars.function_def[-1:] == ',':
                vars.function_def = vars.function_def[:-1]

if __name__ == "__main__":
    robot = ''
    input_filename = ''
    output_filename = 'output.ino'

    print('ARGS: ' + str(len(sys.argv)))

    if len(sys.argv) == 3:
        input_filename = sys.argv[1]
        robot = sys.argv[2]
    else:
        print('Usage: ')
        print('python3 translator/Translator.py [input-file] [robot]')
        sys.exit(0)

    print('FILENAME: ' + input_filename)
    print('ROBOT: ' + robot)
    output = open('output.ino', 'w+')
    controller_file = open(input_filename).read()
    parsed_file = ast.parse(controller_file)
    vars.Variables()
    MyVisitor().visit(parsed_file)

    if robot == 'ComplubotMotor' or robot == 'CompluBotMotor':
        vars.libraries['ArduinoRobotMotorBoard'] = '#include <ArduinoRobotMotorBoard.h>\n'
    elif robot == 'ComplubotControl' or robot == 'CompluBotControl':
        vars.libraries['ArduinoRobot'] = '#include <ArduinoRobot.h>\n'
    elif robot == 'MBot' or robot == 'mBot':
        vars.libraries['MeMCore'] = '#include <MeMCore.h>\n'

    # Architectural stop declaration
    halduino = open(vars.halduino_directory + robot + '.ino', 'r')
    MyVisitor().search_for_function(halduino, 'architecturalStop')

    if 'setup' not in vars.functions:
        vars.functions['setup'] = '''void setup() {
}\n'''
    else:
        vars.functions['setup'] += '}\n'

    if 'loop' not in vars.functions:
        vars.functions['loop'] = '''void loop() {
}\n'''

    variables_manager = ''
    for line in open('Halduino/variables_manager.ino', 'r'):
        if re.search('#include', line):
            vars.libraries[line] = line
        else:
            variables_manager += line
    vars.functions['variables_manager'] = variables_manager

    for key, value in vars.libraries.items():
        output.write(value)
    output.write('\n')
    for key, value in vars.global_variables.items():
        output.write(value)
    output.write('\n')
    output.write(vars.functions['variables_manager'])
    for key, value in vars.functions.items():
        if key != 'variables_manager':
            output.write(value)
        output.write('\n')

    print()
    output.close()
    operating_system = platform.system()
    makefile_parameters = []
    if operating_system == 'Darwin':
        arduino_dir = '/Applications/Arduino.app/Contents/Java'
        makefile_parameters.append('include /usr/local/opt/arduino-mk/Arduino.mk\n')
        print('macOS')
    elif operating_system == 'Windows':
        arduino_dir = 'C:/Arduino'
        makefile_parameters.append('ARDMK_DIR = ../Makefile/Arduino.mk\n')
        print('Windows')
    else:
        arduino_dir = '/usr/share/arduino'
        makefile_parameters.append('ARDMK_DIR =  /usr/share/arduino\n')
        makefile_parameters.append('AVR_TOOLS_DIR =  /usr/\n')
        makefile_parameters.append('include $(ARDMK_DIR)/Arduino.mk\n')
        print('Linux')

    arduino_libs = ''
    if robot == 'ComplubotMotor' or robot == 'CompluBotMotor':
        board = 'robotMotor'
        arduino_libs = 'Robot_Motor Wire SPI'
    elif robot == 'ComplubotControl' or robot == 'CompluBotControl':
        board = 'robotControl'
        arduino_libs = 'Robot_Control Wire SPI'
    elif robot == 'MBot' or robot == 'mBot':
        board = 'uno'
        arduino_libs = 'Makeblock-Libraries-master Wire SPI'
    else:
        board = 'uno'

    file_directory = getcwd() + '/'
    try:
        rmtree('output')
    except FileNotFoundError:
        print('Folder doesn\'t exists')

    makedirs('output')
    chdir('output')
    move(file_directory + output_filename, getcwd() + '/' + output_filename)
    makefile = open(getcwd() + '/' + 'Makefile', 'w+')
    makefile.write('ARDUINO_DIR   = ' + arduino_dir + '\n')
    if arduino_libs:
        makefile.write('ARDUINO_LIBS= ' + arduino_libs + '\n')
    if robot == 'MBot' or robot == 'mBot':
        makefile.write('MONITOR_PORT  = /dev/cu.wchusbserial1420\n')
    else:
        makefile.write('MONITOR_PORT  = /dev/tty.usbmodem*\n')
    makefile.write('BOARD_TAG = ' + board + '\n')
    for parameter in makefile_parameters:
        makefile.write(parameter)
    makefile.close()
    call(['make'])
    call(['make', 'upload'])
