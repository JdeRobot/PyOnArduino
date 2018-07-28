import sys
import ast
from subprocess import call
from os import chdir, getcwd, makedirs
from shutil import move, rmtree
import platform

function_def = ''
parentheses = 0
brackets = 0
functions = {}
global_variables = {}
libraries = {}
has_else_part = False
direction = ''
is_call = False
is_call_parameter = False
call_index = 0
is_Comparision = False
is_var_declaration = False
is_array = False
array_index = 0
array_length = 0
variable_def = ''
is_for = False
for_index = 0
is_if = False
bool_op = []
bin_op = False
halduino_directory = './HALduino/halduino'
is_variable = False
call_def = ''
variables_counter = 0
is_built_in_func = False
var_sign = ''
function_start_line = 0
function_variables_line = 0
is_while = False


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
        global call_index
        global is_call_parameter
        global bin_op
        global call_def
        print('NODE Str: ' + str(type(node.s)))
        var_type = 'String '
        if len(node.s) == 1:
            str_var = '\'' + node.s + '\''
            var_type = 'char '
        else:
            str_var = '\"' + node.s + '\"'
        if is_array:
            if array_index == 0:
                str_var = '{' + str_var
            if array_index < array_length - 1:
                str_var += ','
            array_index += 1

        if is_call_parameter:
            if call_index > 0:
                call_def += ','
            call_index += 1
            print('CALL_INDEX_STR ' + str(call_index))

        if variable_def != '':
            if is_array:
                variable_def = var_type + variable_def + str_var
            else:
                variable_def = var_type + variable_def + ' = ' + str_var
            function_def += variable_def
        else:
            if bin_op:
                function_def += node.s
            else:
                if is_call_parameter:
                    call_def += str_var
                else:
                    function_def += str_var
        variable_def = ''

    def visit_Name(self, node):
        global function_def
        global variable_def
        global is_call
        global is_var_declaration
        global is_array
        global is_for
        global for_index
        global is_call_parameter
        global call_index
        global is_variable
        global call_def
        global is_built_in_func
        print('NODE Name: ' + str(type(node)) + ' ' + node.id)
        if node.id == 'print':
            call_def += 'Serial.' + node.id
            is_built_in_func = True
        elif node.id == 'sleep':
            call_def += 'delay'
            is_built_in_func = True
        elif node.id != 'halduino' and is_var_declaration is False:
            if is_call_parameter:
                if call_index > 0:
                    call_def += ','
                call_index += 1
                print('CALL_INDEX_NAME ' + str(call_index))
            if is_variable:
                function_def += 'atoi(' + node.id + '.data)'
                is_variable = False
            elif is_call or is_call_parameter:
                call_def += node.id
            else:
                function_def += node.id
        if node.id == 'halduino':
            self.add_halduino_function(node)

        if is_call:
            if call_def != '':
                call_def = self.check_last_comma(text=call_def)
            call_def += '('
            is_call = False
            is_call_parameter = True
        elif is_var_declaration:
            variable_def += node.id
            is_var_declaration = False
        elif is_for:
            if for_index == 0:
                function_def += ' = 0; sizeof('
            elif for_index == 1:
                function_def += '); x++) {\n'
            for_index += 1

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
        global is_if
        if node == direction:
            function_def += '} else {\n'
        if is_if:
            function_def += ') {\n'
            is_if = False
        print('NODE Expr: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node):
        global function_def
        global parentheses
        global is_call
        global is_Comparision
        global call_index
        global is_call_parameter
        global bool_op
        global bin_op
        global call_def
        global is_built_in_func
        global is_if
        global is_while
        is_call = True
        call_index = 0
        parentheses += 1
        print('NODE Call: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)
        function_def += call_def
        call_def = ''
        is_call = False
        is_call_parameter = False
        is_built_in_func = False
        call_index = 0
        parentheses -= 1
        if parentheses == 0 and is_Comparision == False and not bool_op and is_if == False and is_while == False:
            self.check_last_comma()
            print('PARENTHESES ' + str(parentheses))
            function_def += ');\n   '
        else:
            print('PARENTHESES ' + str(parentheses))
            function_def += ')'
            is_Comparision = False
        if bin_op:
            bin_op = False

    def visit_Num(self, node):
        global variable_def
        global function_def
        global is_array
        global array_index
        global array_length
        global is_call_parameter
        global call_index
        global call_def
        global is_call
        global variables_counter
        global is_built_in_func
        global var_sign
        print('NODE Num: ' + str(type(node)))
        num_var = str(node.n)
        if is_array:
            if array_index == 0:
                num_var = '{' + num_var
            if array_index < array_length - 1:
                num_var += ','
            array_index += 1

        if is_call_parameter:
            if not is_built_in_func:
                function_def += 'DynType var' + str(variables_counter) + ';'
                function_def += 'var' + str(variables_counter) + '.tvar = ' + str(type(node.n).__name__).upper() + ';'
                function_def += 'String har' + str(variables_counter) + ' = "' + var_sign + str(node.n) + '";'
                function_def += 'har' + str(variables_counter) + '.toCharArray(var' + str(
                    variables_counter) + '.data, MinTypeSz);\n'
                var_sign = ''
            variables_counter += 1

        if variable_def != '':
            if is_array:
                variable_def = type(node.n).__name__ + ' ' + variable_def + num_var
            else:
                var_name = variable_def
                variable_def = 'DynType ' + var_name + ';'
                variable_def += var_name + '.tvar = ' + str(type(node.n).__name__).upper() + ';'
                variable_def += 'String har' + str(variables_counter) + ' = "' + var_sign + str(node.n) + '";'
                variable_def += 'har' + str(variables_counter) + '.toCharArray(' + var_name + '.data, MinTypeSz)'
                variables_counter += 1
            function_def += variable_def
        else:
            if is_call_parameter:
                if not is_built_in_func:
                    if call_index > 0:
                        call_def += ','
                    call_index += 1
                    print('CALL_INDEX_NUM ' + str(call_index))
                    call_def += 'var' + str(variables_counter - 1)
                else:
                    call_def += num_var
            else:
                function_def += num_var
        variable_def = ''
        ast.NodeVisitor.generic_visit(self, node)

    def visit_arguments(self, node):
        global function_def
        global brackets
        for list_index, arg in enumerate(node.args):
            self.visit_arg(arg)
            if list_index < len(node.args) - 1:
                function_def += ', '
        brackets += 1
        function_def += ') {\n'
        print('arguments: ' + str(node.args))

    def visit_arg(self, node):
        global function_def
        function_def += 'DynType ' + node.arg
        print('NODE ARG: ' + str(type(node.annotation)))

    def visit_Return(self, node):
        global function_def
        function_def += '  return '
        print(node.value)
        function_def += ';\n'
        print('NODE Return: ' + str(type(node.value)))
        ast.NodeVisitor.generic_visit(self, node.value)

    def visit_BinOp(self, node):
        global function_def
        global variable_def
        global bin_op
        global call_def
        print('BinOp')
        bin_op = True
        if call_def != '':
            call_def += '('
        else:
            function_def += '('
        print('NODE BinOp: ' + str(type(node.left)) + ' ' + str(type(node.op)) + ' ' + str(type(node.right)))
        ast.NodeVisitor.generic_visit(self, node)
        self.check_last_comma()
        if call_def != '':
            call_def += ')'
        else:
            function_def += ')'

    def visit_While(self, node):
        global function_def
        global is_while
        function_def += 'while('
        print('NODE While 1: ' + str(type(node.test)))
        is_while = True
        ast.NodeVisitor.generic_visit(self, node.test)
        function_def += ') {'
        for body_part in node.body:
            print('NODE While 2: ' + str(type(body_part)))
            ast.NodeVisitor.generic_visit(self, body_part)
        function_def += '}\n'
        is_while = False

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
        global is_if
        global bool_op
        global variables_counter
        global call_index
        global call_def
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
                variable_def = 'DynType var' + str(variables_counter) + ';'
                variable_def += 'var' + str(variables_counter) + '.tvar = BOOL;'
                variable_def += 'String har' + str(variables_counter) + ' = "' + var_sign + boolean_var + '";'
                variable_def += 'har' + str(variables_counter) + '.toCharArray(var' + str(
                    variables_counter) + '.data, MinTypeSz)'
                variables_counter += 1
            function_def += variable_def
        else:
            if is_call_parameter:
                if not is_built_in_func:
                    if call_index > 0:
                        call_def += ','
                    call_index += 1
                    print('CALL_INDEX_NAME_CONSTANT ' + call_index)
                    call_def += 'var' + str(variables_counter - 1)
                else:
                    call_def += boolean_var
            else:
                function_def += boolean_var
        variable_def = ''
        print('NODE NameConstant: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)
        if len(bool_op) > 0:
            function_def += bool_op[len(bool_op) - 1]
            bool_op = bool_op[:-1]

    def visit_Index(self, node):
        global function_def
        global bool_op
        global call_def
        self.check_last_comma()
        if call_def != '':
            call_def += '['
        else:
            function_def += '['
        print('NODE Index: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)
        self.check_last_comma()
        if call_def != '':
            call_def += ']'
        else:
            function_def += ']'
        if len(bool_op) > 0:
            function_def += bool_op[len(bool_op) - 1]
            bool_op = bool_op[:-1]

    def visit_If(self, node):
        global function_def
        global brackets
        global has_else_part
        global direction
        global is_if
        is_if = True
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
        print('NODE If: ' + str(type(node)) + ' ' + str(brackets) + ' ' + str(node.orelse) + ' ' + str(
            has_else_part) + ' ' + str(node.body))
        ast.NodeVisitor.generic_visit(self, node)
        has_else_part = False
        brackets -= 1
        is_if = False
        if global_if:
            function_def += '}\n'

    def visit_Compare(self, node):
        global function_def
        global is_Comparision
        global bool_op
        global is_variable
        print('Comparision')
        # LEFT PART
        print('NODE Compare 1: ' + str(type(node.left)))
        if isinstance(node.left, ast.Call):
            is_Comparision = True
        else:
            is_variable = True
        print('NODE Compare 2: ' + str(type(node.ops[0])))
        print('NODE Compare 3: ' + str(type(node.comparators)))
        function_def += '('
        ast.NodeVisitor.generic_visit(self, node)
        function_def += ')'
        if len(bool_op) > 0:
            function_def += bool_op[len(bool_op) - 1]
            bool_op = bool_op[:-1]

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
        global node_attr
        print('Attribute: ' + str(node.value) + str(node.ctx) + str(node.attr))
        node_attr = node.attr
        print('NODE Atribute 1: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def add_halduino_function(self, node):
        global function_def
        global call_def
        global node_attr
        call_def += node_attr
        print('Halduino found with call to function ' + node_attr)
        halduino = open(halduino_directory + robot + '.ino', 'r')
        print('NODE: ' + node_attr)
        self.search_for_function(halduino, node_attr)

    def search_for_function(self, halduino, searched_node):
        global functions
        global function_variables_line
        global function_start_line
        global global_variables
        function_line = ''
        declaration_name = ''
        not_found = True
        not_eof = True
        is_first_non_empty_line = True
        while not_found and not_eof:
            function_line = halduino.readline()
            function_start_line += 1
            if function_line.strip():
                if is_first_non_empty_line:
                    function_variables_line = function_start_line
                    is_first_non_empty_line = False
                if len(function_line.split(searched_node)) > 1 and function_line.split(searched_node)[len(
                        function_line.split(searched_node)) - 1][-2:] == "{\n":
                    parts = function_line.split(' ')  # +|\([^\)]*\)
                    declaration_name = parts[1].split('(')[0]
                    not_found = False
                    not_eof = False
            else:
                if function_line == '':
                    not_eof = False
                function_variables_line = function_start_line
                is_first_non_empty_line = True
        if not_found is False:
            function_string = ''
            end_of_function = False
            while not end_of_function:
                function_string += function_line
                function_line = halduino.readline()
                l = function_line.rstrip()
                if not l or len(function_line) <= 0:
                    end_of_function = True
            functions[declaration_name] = function_string
        else:
            print('Function not found for this robot! ' + searched_node)
            exit()

        if function_variables_line < function_start_line:
            halduino.seek(0)
            for i, line in enumerate(halduino):
                if i >= function_variables_line - 1 and i < function_start_line - 1:
                    global_variables[line] = line
        function_variables_line = 0
        function_start_line = 0
        halduino.close()

    def visit_For(self, node):
        global function_def
        global is_for
        global for_index
        print('For!')
        print('Target: ' + str(node.target))
        function_def += 'for(int '
        is_for = True
        for_index = 0
        print('NODE For : ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)
        function_def += '}\n'
        for_index = 0
        is_for = False

    def visit_UnaryOp(self, node):
        global function_def
        print('NODE UnaryOp: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Slice(self, node):
        print('NODE Unray 2: ' + str(type(node.value)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Gt(self, node):
        global function_def
        global call_def
        if call_def != '':
            call_def += ' > '
        else:
            function_def += ' > '
        print('Greater than')

    def visit_Lt(self, node):
        global function_def
        global call_def
        if call_def != '':
            call_def += ' < '
        else:
            function_def += ' < '
        print('Lower than')

    def visit_LtE(self, node):
        global function_def
        global call_def
        if call_def != '':
            call_def += ' <= '
        else:
            function_def += ' <= '
        print('Lower than equal')

    def visit_Eq(self, node):
        global function_def
        global call_def
        global call_index
        call_index = 0
        if call_def != '':
            call_def += ' == '
        else:
            function_def += ' == '
        print('Equal')

    def visit_Div(self, node):
        global function_def
        global call_def
        global call_index
        call_index = 0
        self.check_last_comma()
        if call_def != '':
            call_def += ' / '
        else:
            function_def += ' / '

    def visit_Sub(self, node):
        global function_def
        global call_def
        global call_index
        call_index = 0
        self.check_last_comma()
        if call_def != '':
            call_def += ' - '
        else:
            function_def += ' - '

    def visit_Add(self, node):
        global function_def
        global call_def
        global call_index
        call_index = 0
        self.check_last_comma()
        if call_def != '':
            call_def += ' + '
        else:
            function_def += ' + '

    def visit_Mult(self, node):
        global function_def
        global call_def
        global call_index
        call_index = 0
        self.check_last_comma()
        if call_def != '':
            call_def += ' * '
        else:
            function_def += ' * '

    def visit_Mod(self, node):
        global function_def
        global call_def
        global call_index
        call_index = 0
        self.check_last_comma()
        if call_def != '':
            call_def += ' % '
        else:
            function_def += ' % '

    def visit_And(self, node):
        global bool_op
        bool_op.append(' && ')
        print('NODE And: ' + str(type(node)) + str(len(bool_op)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Or(self, node):
        global bool_op
        bool_op.append(' || ')
        print('NODE Or: ' + str(type(node)) + str(len(bool_op)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_BoolOp(self, node):
        print('NODE boolOp: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Load(self, node):
        print('NODE Load: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_USub(self, node):
        global var_sign
        var_sign += '-'
        print('NODE USub: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Is(self, node):
        global function_def
        function_def += ' == '
        print('NODE Is: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_IsNot(self, node):
        global function_def
        function_def += ' != '
        print('NODE IsNot: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Pass(self, node):
        print('NODE Pass: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def check_last_comma(self, text=None):
        global function_def
        if text is not None:
            if text[-1:] == ',':
                return text[:-1]
            return text
        else:
            if function_def[-1:] == ',':
                function_def = function_def[:-1]


def has_motor_functions():
    return 'setSpeedEnginesMotor' in functions or 'getIR1' in functions or 'getIR2' in functions or 'getIR3' in functions or 'getIR4' in functions or 'getIR5' in functions


def uses_speaker():
    return 'playBeep' in functions or 'playMelody' in functions


def uses_screen():
    return 'clearIt' in functions or 'setScreenText' in functions


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
    MyVisitor().visit(parsed_file)

    if 'setup' not in functions:
        functions['setup'] = '''void setup() {
}\n'''

    if 'loop' not in functions:
        functions['loop'] = '''void loop() {
}\n'''

    if robot == 'Complubot' or robot == 'CompluBot':
        halduino = open(halduino_directory + robot + '.ino', 'r')
        MyVisitor().search_for_function(halduino, 'setScreenText')
        setup = '\n'
        for index, line in enumerate(functions['setup'].splitlines()):
            if index == 1:
                if has_motor_functions():
                    setup += '\n   RobotMotor.begin();\n'
                else:
                    setup += '\n   Robot.begin();\n'

                if uses_speaker():
                    setup += '\n   Robot.beginSpeaker();\n'

                if uses_screen():
                    setup += '\n   Robot.beginTFT();\n'
            setup += line
        setup += '\n'
        functions['setup'] = setup
        if has_motor_functions():
            libraries['ArduinoRobotMotorBoard'] = '#include <ArduinoRobotMotorBoard.h>\n'
        else:
            libraries['ArduinoRobot'] = '#include <ArduinoRobot.h>\n'
    elif robot == 'MBot' or robot == 'mBot':
        halduino = open(halduino_directory + robot + '.ino', 'r')
        MyVisitor().search_for_function(halduino, 'setLeds')
        halduino = open(halduino_directory + robot + '.ino', 'r')
        MyVisitor().search_for_function(halduino, 'playBuzzer')
        libraries['MeMCore'] = '#include <MeMCore.h>\n'

    variables_manager = ''
    for line in open('Halduino/variables_manager.ino', 'r'):
        if len(line.split('#include')) > 1:
            libraries[line] = line
        else:
            variables_manager += line
    functions['variables_manager'] = variables_manager

    for key, value in libraries.items():
        output.write(value)
    output.write('\n')
    for key, value in global_variables.items():
        output.write(value)
    output.write('\n')
    output.write(functions['variables_manager'])
    for key, value in functions.items():
        if key != 'variables_manager':
            output.write(value)
        output.write('\n')

    # Architectural stop declaration
    halduino = open(halduino_directory + robot + '.ino', 'r')
    MyVisitor().search_for_function(halduino, 'architecturalStop')
    output.write(functions['architecturalStop'])
    halduino = open(halduino_directory + robot + '.ino', 'r')
    MyVisitor().search_for_function(halduino, 'stopMachine')
    output.write(functions['stopMachine'])

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
    if robot == 'Complubot' or robot == 'CompluBot':
        if has_motor_functions():
            board = 'robotMotor'
            arduino_libs = 'Robot_Motor Wire SPI'
        else:
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
