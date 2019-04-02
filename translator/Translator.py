import sys
import ast
from subprocess import call
from os import chdir, getcwd, makedirs
from shutil import move, rmtree
import platform
import re

try:
    sys.path.append(".")
    import translator.TranslatorVariables as vars
    import translator.strings.TranslatorStrings as strings
except ModuleNotFoundError:
    print('Absolute import failed')


class TranslatorVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        print(strings.GENERIC_NODE + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Str(self, node):
        print(strings.STR_NODE + str(type(node.s)))
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
        vars.function_def += self.dyn_variable_creation(var_name, var_type, str(node.s))
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
        print(strings.NAME_NODE + str(type(node)) + ' ' + node.id)
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

        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        vars.variable_def = ''
        vars.function_def = node.name + '('
        print(strings.FUNCTION_DEF + str(node.name))
        print(strings.NODE_ARGS + str(type(node.args)))
        vars.scope_variables = []
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
        print(strings.NODE_EXPR + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node):
        vars.is_call = True
        vars.call_index = 0
        vars.parentheses += 1
        print(strings.NODE_CALL + str(type(node)))
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
            print(strings.PARENTHESES + str(vars.parentheses))
            vars.function_def += ');\n   '
        else:
            print(strings.PARENTHESES + str(vars.parentheses))
            vars.function_def += ')'
            vars.is_comparision = False
        if vars.bin_op:
            vars.bin_op = False

    def visit_Num(self, node):
        print(strings.NODE_NUM + str(type(node)))
        vars.num_var = str(node.n)
        if vars.is_array:
            if vars.array_index == 0:
                vars.num_var = '{' + vars.num_var
            if vars.array_index < vars.array_length - 1:
                vars.num_var += ','
            vars.array_index += 1

        if vars.is_call_parameter:
            if not vars.is_built_in_func:
                vars.function_def += self.dyn_variable_creation('var' + str(vars.variables_counter),
                                                                str(type(node.n).__name__).upper(),
                                                                vars.var_sign + str(node.n))
                vars.var_sign = ''
            vars.variables_counter += 1

        if vars.variable_def != '':
            if vars.is_array:
                vars.variable_def = type(node.n).__name__ + ' ' + vars.variable_def + vars.num_var
            else:
                var_name = vars.variable_def
                vars.variable_def = self.dyn_variable_creation(var_name, str(type(node.n).__name__).upper(),
                                                               vars.var_sign + str(node.n))
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
        print(strings.NODE_ARGS + str(node.args))

    def visit_arg(self, node):
        vars.function_def += 'DynType ' + node.arg
        print(strings.NODE_ARG + str(type(node.annotation)))

    def visit_Return(self, node):
        vars.function_def += '  return '
        print(node.value)
        print(strings.NODE_RETURN + str(type(node.value)))
        ast.NodeVisitor.visit(self, node.value)
        vars.function_def += ';\n'

    def visit_BinOp(self, node):
        vars.bin_op = True
        if vars.call_def != '':
            vars.call_def += '('
        else:
            vars.function_def += '('
        print(strings.NODE_BINOP + str(type(node.left)) + ' ' + str(type(node.op)) + ' ' + str(type(node.right)))
        ast.NodeVisitor.generic_visit(self, node)
        self.check_last_comma()
        if vars.call_def != '':
            vars.call_def += ')'
        else:
            vars.function_def += ')'

    def visit_While(self, node):
        vars.function_def += 'while('
        print(strings.NODE_WHILE + str(type(node.test)))
        vars.is_while = True
        ast.NodeVisitor.generic_visit(self, node.test)
        vars.function_def += ') {'
        for body_part in node.body:
            print(strings.NODE_WHILE_BODY + str(type(body_part)))
            ast.NodeVisitor.generic_visit(self, body_part)
        vars.function_def += '}\n'
        vars.is_while = False

    def visit_List(self, node):
        print(strings.NODE_LIST + str(type(node)) + ' ' + str(type(node.elts)) + ' ' + str(type(node.ctx)) + ' ')
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
                vars.variable_def = self.dyn_variable_creation('var' + str(vars.variables_counter), 'BOOL',
                                                               vars.var_sign + boolean_var)
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
        print(strings.NODE_NAME_CONSTANT + str(type(node)))
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
        print(strings.NODE_INDEX + str(type(node)))
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
        vars.function_def += 'if ('
        vars.is_if = True # visit_Call inserts a ';' if NOT set to True.
        self.visit (node.test)
        vars.is_if = False
        vars.function_def += ') {\n'
        for statement in node.body:
            self.visit (statement)
        vars.function_def += '} '
        if (len (node.orelse) > 0):
            for i in range (0, len (node.orelse)):
                statement = node.orelse[i]
                if (type(statement) == ast.If):
                    vars.function_def += 'else '
                    self.visit (statement)
                    if (i == len(node.orelse) - 1):
                        vars.function_def += '\n'
                    
                else:
                    vars.function_def += 'else {\n'
                    self.visit (statement)
                    vars.function_def += '}\n'
        print(strings.NODE_IF + str(type(node)) + ' ' + str(vars.brackets) + ' ' + str(node.orelse) + ' ' + str(
            vars.has_else_part) + ' ' + str(node.body))

    def visit_Compare(self, node):
        print(strings.NODE_COMPARE + str(type(node.left)) + ' ' + str(type(node.ops[0])) + ' ' + str(
            type(node.comparators)))
        if isinstance(node.left, ast.Call):
            vars.is_comparision = True
        else:
            vars.is_variable = True
        vars.function_def += '('
        ast.NodeVisitor.generic_visit(self, node)
        vars.function_def += ')'
        if len(vars.bool_op) > 0:
            vars.function_def += vars.bool_op[len(vars.bool_op) - 1]
            vars.bool_op = vars.bool_op[:-1]

    def visit_Assign(self, node):
        print(strings.NODE_ASSIGN + str(node.targets) + ' ' + str(node.value))
        vars.is_var_declaration = True
        ast.NodeVisitor.generic_visit(self, node)
        vars.function_def += vars.variable_def
        vars.variable_def = ''

    def visit_Attribute(self, node):
        print(strings.NODE_ATTRIBUTE + str(node.value) + str(node.ctx) + str(node.attr))
        vars.node_attr = node.attr
        ast.NodeVisitor.generic_visit(self, node)

    def add_halduino_function(self, node):
        vars.call_def += vars.node_attr
        print('Halduino found with call to function ' + vars.node_attr)
        self.search_for_function(vars.halduino_directory + robot, vars.node_attr)

    def search_for_function(self, directory, searched_node, is_first_search=True):
        halduino = open(directory + '.ino', 'r')
        function_line = ''
        not_found = True
        not_eof = True
        is_first_non_empty_line = True
        function_start_line = 0
        function_variables_line = 0
        if searched_node not in vars.functions:
            while not_found and not_eof:
                if re.search('#include', function_line):
                    vars.libraries[function_line] = function_line
                function_line = halduino.readline()
                function_start_line += 1
                if function_line.strip():
                    if is_first_non_empty_line:
                        function_variables_line = function_start_line
                        is_first_non_empty_line = False
                    if re.search('\w+ ' + searched_node + '\(.*\) {', function_line):
                        not_found = False
                        not_eof = False
                else:
                    not_eof = function_line != ''
                    function_variables_line = function_start_line
                    is_first_non_empty_line = True
            if not_found is False:
                self.add_function(function_line, searched_node, function_variables_line, function_start_line,
                                  is_first_search, halduino)
            else:
                if is_first_search and not searched_node == strings.SETUP:
                    print('Function not found for this robot! ' + searched_node)
                    halduino.close()
                    exit()
        halduino.close()

    def add_function(self, function_line, searched_node, function_variables_line, function_start_line, is_first_search,
                     halduino):
        function_string = ''
        end_of_function = False
        while not end_of_function:
            function_string += function_line
            function_line = halduino.readline()
            if re.search(strings.REGEX_IS_FUNCTION, function_line) and not re.search(strings.REGEX_HAS_DOT,
                                                                                     function_line):
                function_name = re.search(strings.REGEX_FUNCTION_NAME, function_line).group(0)[:-1]
                if function_name not in vars.functions:
                    self.search_for_function(vars.halduino_directory + robot, function_name, is_first_search=False)
            l = function_line.rstrip()
            end_of_function = not l or len(function_line) <= 0
        vars.functions[searched_node] = function_string
        if function_variables_line < function_start_line:
            halduino.seek(0)
            for i, line in enumerate(halduino):
                if function_variables_line - 1 <= i < function_start_line - 1:
                    if re.search(strings.REGEX_SETUP_STATEMENT, line) and not re.search(strings.REGEX_VARIABLE, line):
                        vars.setup_statements[line] = line
                    else:
                        vars.global_variables[line] = self.search_architecture(line)
        if is_first_search:
            halduino.close()

    def search_architecture(self, line):
        if robot_architecture:
            architecture_variable = re.search(strings.REGEX_ARCHITECTURE_VARIABLE, line)
            if architecture_variable:
                match = re.search(strings.REGEX_ARCHITECTURE_VARIABLE_2, architecture_variable.group(0))
                for architecture_line in open(robot_architecture, 'r'):
                    if (re.search(match.group(0), architecture_line)):
                        value = re.search(strings.REGEX_VARIABLE_VALUE, architecture_line)
                        new_line = ''
                        for letter in line:
                            if letter != '(' and letter != '=':
                                new_line += letter
                            else:
                                if letter == '(':
                                    new_line += '(' + value.group(0)[1:] + ');\n'
                                else:
                                    new_line += '= ' + value.group(0)[1:] + ';\n'
                                break
                        line = new_line
        return line

    def visit_For(self, node):
        print('For statements are not supported yet')
        exit(0)

    def visit_UnaryOp(self, node):
        print(strings.NODE_UNARYOP + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Slice(self, node):
        print(strings.NODE_SLICE + str(type(node.value)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Gt(self, node):
        if vars.call_def != '':
            vars.call_def += ' > '
        else:
            vars.function_def += ' > '

    def visit_Lt(self, node):
        if vars.call_def != '':
            vars.call_def += ' < '
        else:
            vars.function_def += ' < '

    def visit_LtE(self, node):
        if vars.call_def != '':
            vars.call_def += ' <= '
        else:
            vars.function_def += ' <= '

    def visit_Eq(self, node):
        vars.call_index = 0
        if vars.call_def != '':
            vars.call_def += ' == '
        else:
            vars.function_def += ' == '

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
        print(strings.NODE_AND + str(type(node)) + str(len(vars.bool_op)))
        vars.bool_op.append(' && ')
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Or(self, node):
        print(strings.NODE_OR + str(type(node)) + str(len(vars.bool_op)))
        vars.bool_op.append(' || ')
        ast.NodeVisitor.generic_visit(self, node)

    def visit_BoolOp(self, node):
        print(strings.NODE_BOOLOP + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Load(self, node):
        print(strings.NODE_LOAD + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_USub(self, node):
        print(strings.NODE_USUB + str(type(node)))
        vars.var_sign += '-'
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Is(self, node):
        print(strings.NODE_IS + str(type(node)))
        vars.function_def += ' == '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_IsNot(self, node):
        print(strings.NODE_IS_NOT + str(type(node)))
        vars.function_def += ' != '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Pass(self, node):
        print(strings.NODE_PASS + str(type(node)))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Set(self, node):
        print('Arrays are not supported yet')
        exit(0)

    def visit_Tuple(self, node):
        print('Tuples are not supported yet')
        exit(0)

    def dyn_variable_creation(self, var_name, var_type, value):
        if var_name in vars.scope_variables:
            definition = ''
        else:
            vars.scope_variables.append(var_name)
            definition = 'DynType ' + var_name + ';'
        definition += var_name + '.tvar = ' + var_type + ';'
        definition += 'String har' + str(vars.variables_counter) + ' = "' + value + '";'
        definition += 'har' + str(vars.variables_counter) + '.toCharArray(' + var_name + '.data, MinTypeSz);\n'
        return definition

    def check_last_comma(self, text=None):
        if text is not None:
            if text[-1:] == ',':
                return text[:-1]
            return text
        else:
            if vars.function_def[-1:] == ',':
                vars.function_def = vars.function_def[:-1]


def create_output():
    output = open('output.ino', 'w+')
    for key, value in vars.libraries.items():
        output.write(value)
    output.write('\n')
    for key, value in vars.global_variables.items():
        output.write(value)
    output.write(variables_manager)
    for key, value in vars.functions.items():
        output.write(value)
        output.write('\n')
    output.close()
    file_directory = getcwd() + '/'
    try:
        rmtree(strings.OUTPUT)
    except FileNotFoundError:
        print('Folder doesn\'t exists')

    makedirs(strings.OUTPUT)
    chdir(strings.OUTPUT)
    move(file_directory + output_filename, getcwd() + '/' + output_filename)


def create_makefile(robot):
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

    makefile = open(getcwd() + '/' + 'Makefile', 'w+')
    for line in open('../makefiles/' + robot + 'Makefile', 'r'):
        makefile.write(line)
    makefile.write('ARDUINO_DIR   = ' + arduino_dir + '\n')
    for parameter in makefile_parameters:
        makefile.write(parameter)
    makefile.close()


if __name__ == "__main__":
    output_filename = 'output.ino'

    print('ARGS: ' + str(len(sys.argv)))

    if len(sys.argv) == 3:
        input_filename = sys.argv[1]
        robot = sys.argv[2]
        robot_architecture = ''
    elif len(sys.argv) == 4:
        input_filename = sys.argv[1]
        robot = sys.argv[2]
        robot_architecture = sys.argv[3]
    else:
        print('Usage: ')
        print('python3 translator/Translator.py [input-file] [robot]')
        sys.exit(0)

    print('FILENAME: ' + input_filename)
    print('ROBOT: ' + robot)
    controller_file = open(input_filename).read()
    parsed_file = ast.parse(controller_file)
    vars.Variables()
    TranslatorVisitor().visit(parsed_file)

    # Architectural stop declaration
    TranslatorVisitor().search_for_function(vars.halduino_directory + robot, strings.ARCHITECTURAL_STOP)
    TranslatorVisitor().search_for_function(vars.halduino_directory + robot, strings.SETUP)

    if strings.SETUP not in vars.functions:
        vars.functions[strings.SETUP] = 'void setup() {\n'
        for key, value in vars.setup_statements.items():
            vars.functions[strings.SETUP] += value
        vars.functions[strings.SETUP] += '}\n'
    elif vars.setup_statements:
        setup = vars.functions[strings.SETUP]
        counter = 0
        setup = setup.split("\n")
        new_setup = ''
        while setup[counter] != '}':
            new_setup += setup[counter] + '\n'
            counter += 1
        for key, value in vars.setup_statements.items():
            new_setup += value + '\n'
        new_setup += '}\n'
        vars.functions[strings.SETUP] = new_setup

    if strings.LOOP not in vars.functions:
        vars.functions[strings.LOOP] = '''void loop() {
}\n'''

    variables_manager = ''
    for line in open('HALduino/variablesManager.ino', 'r'):
        if re.search('#include', line):
            vars.libraries[line] = line
        else:
            variables_manager += line

    create_output()
    create_makefile(robot)
    call(['make'])
    call(['make', 'upload'])
