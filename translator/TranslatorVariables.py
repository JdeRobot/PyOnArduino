# TranslatorVariables.py

class Variables:
    def __init__(self):
        global array_index
        global array_length
        global bin_op
        global brackets
        global bool_op
        global call_def
        global call_index
        global direction
        global functions
        global function_def
        global function_start_line
        global function_variables_line
        global global_variables
        global halduino_directory
        global has_else_part
        global is_call
        global is_comparision
        global is_call_parameter
        global is_var_declaration
        global is_array
        global is_built_in_func
        global is_if
        global is_variable
        global is_while
        global libraries
        global parentheses
        global scope_variables
        global setup_statements
        global variable_def
        global variables_counter
        global var_sign

        array_index = 0
        array_length = 0
        bin_op = False
        brackets = 0
        bool_op = []
        call_def = ''
        call_index = 0
        direction = ''
        functions = {}
        function_def = ''
        function_start_line = 0
        function_variables_line = 0
        global_variables = {}
        halduino_directory = './HALduino/halduino'
        has_else_part = False
        is_call = False
        is_call_parameter = False
        is_comparision = False
        is_var_declaration = False
        is_array = False
        is_built_in_func = False
        is_if = False
        is_variable = False
        is_while = False
        libraries = {}
        parentheses = 0
        scope_variables = []
        setup_statements = {}
        variable_def = ''
        variables_counter = 0
        var_sign = ''