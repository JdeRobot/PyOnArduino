import sys
import ast
from subprocess import call
from os import chdir, getcwd
from shutil import move, rmtree
import platform

function_def = ''
parentheses = 0
brackets = 0
functions = {}
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
is_if = True
boolOp = ''


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
        print('NODE Str: ' + str(type(node.s)))
        str_var = '\"' + node.s + '\"'
        if is_array:
            if array_index == 0:
                str_var = '{' + str_var
            if array_index < array_length - 1:
                str_var += ','
            array_index += 1

        if is_call_parameter:
            if call_index >= 0:
                str_var += ','
            call_index += 1

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
        global is_for
        global for_index
        global is_call_parameter
        global call_index
        global is_call_parameter

        if node.id == 'print':
            function_def += 'Serial.' + node.id
        elif node.id == 'sleep':
            function_def += 'delay'
        elif node.id != 'halduino' and is_var_declaration is False:
            if is_call_parameter:
                if call_index >= 0:
                    node.id += ','
                call_index += 1
            function_def += node.id

        if is_call:
            self.check_last_comma()
            function_def += '('
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
        global call_index
        global is_call_parameter
        global boolOp
        is_call_parameter = True
        is_call = True
        call_index = 0
        parentheses += 1
        print('NODE Call: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)
        is_call = False
        is_call_parameter = False
        call_index = 0
        parentheses -= 1
        if parentheses == 0 and is_Comparision == False and not boolOp:
            self.check_last_comma()
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
        global is_call_parameter
        global call_index
        print('NODE Num: ' + str(type(node)))
        num_var = str(node.n)
        if is_array:
            if array_index == 0:
                num_var = '{' + num_var
            if array_index < array_length - 1:
                num_var += ','
            array_index += 1

        if is_call_parameter:
            if call_index >= 0:
                num_var += ','
            call_index += 1

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
        for list_index, arg in enumerate(node.args):
            self.visit_arg(arg)
            if list_index < len(node.args) - 1:
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
        function_def += '('
        print('NODE Return: ' + str(type(node.left)) + ' ' + str(type(node.op)) + ' ' + str(type(node.right)))
        ast.NodeVisitor.generic_visit(self, node)
        self.check_last_comma()
        function_def += ')'

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
        global is_if
        boolean_var = ''
        if node.value is True:
            boolean_var = 'true'
        elif node.value is False:
            boolean_var = 'false'

        if is_if:
            boolean_var += ') {\n'

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
        self.check_last_comma()
        function_def += '['
        print('NODE Index: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)
        self.check_last_comma()
        function_def += ']'

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
        print('NODE If: ' + str(type(node)) + ' ' + str(brackets) + ' ' + str(node.orelse) + ' ' + str(has_else_part))
        ast.NodeVisitor.generic_visit(self, node)
        has_else_part = False
        brackets -= 1
        is_if = False
        if global_if:
            function_def += '}\n'

    def visit_Compare(self, node):
        global function_def
        global is_Comparision
        global boolOp
        print('Comparision')
        # LEFT PART
        print('NODE Compare 1: ' + str(type(node.left)))
        if isinstance(node.left, ast.Call):
            is_Comparision = True
        print('NODE Compare 2: ' + str(type(node.ops[0])))
        print('NODE Compare 3: ' + str(type(node.comparators)))
        function_def += '('
        ast.NodeVisitor.generic_visit(self, node)
        function_def += ')'
        if boolOp:
            function_def += boolOp
            boolOp = ''
        else:
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
        if node.value.id == 'halduino':
            self.add_halduino_function(node)
        print('NODE Atribute 1: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def add_halduino_function(self, node):
        global function_def
        function_def += node.attr
        print('Halduino found with call to function ' + node.attr)
        halduino = open('./HALduino/halduino' + robot + '.ino', 'r')
        print('NODE: ' + node.attr)
        self.search_for_function(halduino, True, '', '', node.attr)

    def search_for_function(self, halduino, not_found, function_line, declaration_name, searched_node):
        global functions
        not_eof = True
        while not_eof:
            while not_found and not_eof:
                function_line = halduino.readline()
                if len(function_line) > 0:
                    if len(function_line.split(searched_node)) > 1:
                        parts = function_line.split(' ')  # +|\([^\)]*\)
                        declaration_name = parts[1].split('(')[0]
                        not_found = False
                        not_eof = False
                else:
                    not_eof = False

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
                not_found = True

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
        self.check_last_comma()
        function_def += ' / '

    def visit_Sub(self, node):
        global function_def
        self.check_last_comma()
        function_def += ' - '

    def visit_Add(self, node):
        global function_def
        self.check_last_comma()
        function_def += ' + '

    def visit_Mult(self, node):
        global function_def
        self.check_last_comma()
        function_def += ' * '

    def visit_Mod(self, node):
        global function_def
        self.check_last_comma()
        function_def += ' % '

    def visit_And(self, node):
        global boolOp
        boolOp = ' && '
        print('NODE And: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Or(self, node):
        global boolOp
        boolOp = ' || '
        print('NODE Or: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_BoolOp(self, node):
        global function_def
        print('NODE BoolOp: ' + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)


    def check_last_comma(self):
        global function_def
        if function_def[-1:] == ',':
            function_def = function_def[:-1]

if __name__ == "__main__":
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
        print('python3 translator/Translator.py [input-file] [robot] [output-file]')
        print('python3 translator/Translator.py [input-file] [robot]')
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

    if robot == 'Complubot' or robot == 'CompluBot':
        # Modify setup to include Robot.begin()
        setup = '\n'
        for index, line in enumerate(functions['setup'].splitlines()):
            if index == 1:
                if 'setSpeedEngines' in functions or 'getIR1' in functions or 'getIR2' in functions or 'getIR3' in functions or 'getIR4' in functions or 'getIR5' in functions:
                    setup += '\n   RobotMotor.begin();\n'
                else:
                    setup += '\n   Robot.begin();\n'
                if 'playBeep' in functions or 'playMelody' in functions:
                    setup += '\n   Robot.beginSpeaker();\n'
                if 'clearIt' in functions or 'setScreenText' in functions:
                    setup += '\n   Robot.beginTFT();\n'
            setup += line

        setup += '\n'''
        functions['setup'] = setup
        if 'setSpeedEngines' in functions or 'getIR1' in functions or 'getIR2' in functions or 'getIR3' in functions or 'getIR4' in functions or 'getIR5' in functions:
            output.write('#include <ArduinoRobotMotorBoard.h> // include the robot library\n')
        else:
            output.write('#include <ArduinoRobot.h> // include the robot library\n')

    for key, value in functions.items():
        output.write(value)

    print()
    output.close()
    operating_system = platform.system()
    if operating_system == 'Darwin':
        arduino_dir = '/Applications/Arduino.app/Contents/Java'
        print('macOS')
    elif operating_system == 'Windows':
        arduino_dir = 'C:/Arduino'
        print('Windows')
    else:
        arduino_dir = '/home/sudar/apps/arduino-1.0.5'
        print('Linux')

    arduino_libs =''
    if robot == 'Complubot'  or robot == 'CompluBot':
        board = 'robotControl'
        arduino_libs = 'Robot_Control Wire SPI'
    else:
        board = 'uno'

    file_directory = getcwd()+'/'
    try:
        rmtree('output')
    except FileNotFoundError:
        print('Folder doesn\'t exists')

    call(['mkdir', 'output'])
    chdir('output/')
    move(file_directory+output_filename, getcwd() + '/' + output_filename)
    makefile = open(getcwd() + '/' + 'Makefile', 'w+')
    makefile.write('ARDUINO_DIR   = ' + arduino_dir + '\n')
    if arduino_libs:
        makefile.write('ARDUINO_LIBS= '+arduino_libs+'\n')
    makefile.write('MONITOR_PORT  = /dev/cu.usbmodem*\n')
    makefile.write('BOARD_TAG = ' + board + '\n')
    makefile.write('include /usr/local/opt/arduino-mk/Arduino.mk')
    makefile.close()
    call(['make'])
    call(['make', 'upload'])