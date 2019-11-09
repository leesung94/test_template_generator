#!/usr/bin/python
# -*- coding: utf-8 -*- 

# Author:
#   Lee Sung

import os.path

class Contents_Extractor:
    def __init__(self, fileloc):
        self.fileloc = fileloc
        self.filename = None
        self.contents = []
        self.filehandle = None
        self.directory = None
        self.is_class = None
        self.function_names = []

    def open_file(self):
        if os.path.isfile(self.fileloc):
            self.filehandle = open(self.fileloc, "r")
            self.filename = os.path.basename(self.fileloc)
            self.directory = os.path.dirname(self.fileloc)
            return 0
        return 1

    def close_file(self):
        self.filehandle.close()

    def read_contents(self):
        self.contents = self.filehandle.readlines()

    @staticmethod
    def parse_function_name(string):
        funcname = ""
        # Want what is right of the equals sign and space
        if ("= " in string):
            funcname = string.split("= ")[1]
        # Want what is right of the equals sign
        elif ("=" in string):
            funcname = string.split("=")[1]
        # If we get here then all we want is everything right of "function "
        else:
            funcname = string.split("function ")[1]
        return funcname

    @staticmethod
    def parse_function_inputs(string):
        arg_list = []
        # Remove the right bracket
        phase_one = string.split(")")[0]
        # Check there are inputs
        if len(phase_one) > 0:
            if ("," in phase_one):
                # Split the inputs
                arg_list = phase_one.split(",")
            else:
                # Single input
                arg_list.append(phase_one)
        return arg_list

    @staticmethod
    def parse_function_outputs(string):
        output_list = []
        # Check we have outputs
        if ("=" in string):
            # Get everything to the right of "function "
            phase_one = string.split("function ")[1]
            # Get everything left of "="
            phase_two = phase_one.split("=")[0]
            if "[" in phase_two:
                phase_three = phase_two.split("[")[1]
                phase_four = phase_three.split("]")[0]
                output_list = (phase_four.split(","))
            else:
                output_list.append(phase_two)
        return output_list

    @staticmethod
    def recombine_multi_func(idx, list, line):
        # Check if the function is multilined
        if ("..." in line):
            idx += 1
            # Replace the pattern before we append the next line so that we dont 
            # endlessly loop
            line = line.replace("...", "")
            line = line.replace("\n", "")
            newline = list[idx]
            newline = newline.strip()
            # Append the next line
            line += newline
            # Repeat until we stop encountering "..."
            [line, idx] = Contents_Extractor.recombine_multi_func(idx, list, line)
        # End clause is we dont 
        return [line, idx]

    def get_function_lines(self):
        function_lines = []
        idx = 0
        while (idx < len(self.contents)):
            line = self.contents[idx]
            # If line contains "function" that are not comments or code
            if ("function" in line and "%" not in line and ";" not in line):
                [line, idx] = Contents_Extractor.recombine_multi_func(idx, self.contents, line)
                function_lines.append(line)
            idx += 1
        return function_lines

    def get_functions(self):
        self.function_names = []
        # Witchcraft TM
        # Gets all lines in the string array which contain the word "function"
        function_lines = self.get_function_lines()
        for func in function_lines:
            # Exclude comments and lines of code
            if ("%" not in func and ";" not in func):
                # Parse function name, inputs and outputs
                first_split = func.split("(")
                firstpass_left = first_split[0]
                firstpass_right = first_split[1]

                funcname = Contents_Extractor.parse_function_name(firstpass_left)
                func_args = Contents_Extractor.parse_function_inputs(firstpass_right)
                func_outs = Contents_Extractor.parse_function_outputs(firstpass_left)
                func_details = (funcname, func_args, func_outs)
                self.function_names.append(func_details)
        return self.function_names

    def match_first_item_in_contents(self, substring):
        """
        Search the contents instance variable and attempts to match an entry with
        a substring 
        """
        idx = None
        # More Witchcraft TM
        element = next((s for s in self.contents if substring in s), None)
        # If we get an element then find its index
        if element != None:
            idx = self.contents.index(element)
        return idx

    def get_script_type(self):
        """
        Work out if we are dealing with a class or function script
        """
        # Check if we found an element with classdef substring
        if self.match_first_item_in_contents("classdef") == None:
            # Check if we found an element with function substring
            if self.match_first_item_in_contents("function") != None:
                self.is_class = False
        else:
            self.is_class = True
        return self.is_class

class Script_Generator:

    def __init__(self, filename, parent_dir):
        self.filename = "TEST_" + filename
        self.classname = os.path.splitext(filename)[0]
        self.file_contents = None
        self.parent_dir = os.path.join(parent_dir, '')
        self.fileloc = self.parent_dir + self.filename

    @staticmethod
    def form_function_content(function_details):
        funcname = function_details[0]
        input_list = function_details[1]
        outputs_list = function_details[2]
        # Create the string for inputs appends a "," between inputs if multiple exist
        str_inputs = ','.join(str(ele) for ele in input_list)
        # Create the string for output
        str_outputs = ""
        if isinstance(outputs_list, str) == False and len(outputs_list) > 0:
            str_outputs = "["
            str_outputs += ','.join(str(ele) for ele in outputs_list)
            str_outputs += "]"
        elif isinstance(outputs_list, str) and len(outputs_list) > 0:
            str_outputs = str(outputs_list)
        return [funcname, str_inputs, str_outputs, input_list]

    def generate_file_head(self):
        self.file_contents = ("classdef (TestTags = {''}) TEST_" + self.classname + " < matlab.unittest.TestCase\n\n")
        self.file_contents += ("    properties\n\n")
        self.file_contents += ("    end\n\n")
        self.file_contents += ("    methods (TestClassSetup)\n\n")
        self.file_contents += ("        function setup(testCase)\n\n")
        self.file_contents += ("        end\n\n")
        self.file_contents += ("    end\n\n")
        self.file_contents += ("    methods (TestClassTeardown)\n\n")
        self.file_contents += ("        function teardown(testCase)\n\n")
        self.file_contents += ("        end\n\n")
        self.file_contents += ("    end\n\n")
        self.file_contents += ("    methods (TestMethodTeardown)\n\n")
        self.file_contents += ("    end\n\n")
        self.file_contents += ("    methods (Test)\n\n")

    def generate_function_block(self, function_details):
        [funcname, str_inputs, str_outputs, input_list] = Script_Generator.form_function_content(function_details)

        self.file_contents += ("        function test_" + funcname + "(testCase)\n\n")
        self.file_contents += ("        % Test Objective:\n")
        self.file_contents += ("        % -------------------------------------------------------------\n\n")

        self.file_contents += ("        % Pass Criteria:\n")
        self.file_contents += ("        % -------------------------------------------------------------\n\n")

        # Generate input declaration
        self.file_contents += ("        % Test Input Data:\n")
        self.file_contents += ("        % -------------------------------------------------------------\n\n")
        for ele in input_list:
            self.file_contents += ("        " + ele.strip() + ";\n")

        # Generate UUT call
        self.file_contents += ("\n        % Execute Unit Under Test:\n")
        self.file_contents += ("        % -------------------------------------------------------------\n\n")

        # If we expect output then generate the assignment from function call
        if len(str_outputs) > 0:
            self.file_contents += ("        " + str_outputs + "= " + funcname + "(")
        else:
            self.file_contents += ("        " + funcname + "(")
        self.file_contents += (str_inputs + ");\n\n")
        self.file_contents += ("        % Verification:\n")
        self.file_contents += ("        % -------------------------------------------------------------\n\n")

        self.file_contents += ("        end\n\n")

    def generate_file_tail(self):
        self.file_contents += ("    end\n\n")
        self.file_contents += ("    methods\n\n")
        self.file_contents += ("    end\n\n")
        self.file_contents += ("end\n\n")

    def write_file(self):
        if os.path.isfile(self.fileloc):
            print("Error: Test Template already exists in: " + self.fileloc)
        else:
            file_handle = open(self.fileloc, "w+") 
            file_handle.write(self.file_contents)
            file_handle.close()
