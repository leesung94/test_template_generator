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
        self.first_line = None

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

    def get_function_names(self):
        # Exclude first line incase the script is a function script
        modified_list = self.contents[self.first_line:]
        # Witchcraft TM
        # Gets all lines in the string array which contain the word "function"
        function_lines = [line for line in modified_list if "function" in line]
        for func in function_lines:
            # Want everything left of the bracket
            firstpass = func.split("(")[0]
            secondpass = ""
            # Want what is left of the equals sign and space
            if ("= " in firstpass):
                secondpass = firstpass.split("= ")[1]
            elif ("=" in firstpass):
                secondpass = firstpass.split("=")[1]
            else:
                secondpass = firstpass.split("function ")[1]
            self.function_names.append(secondpass)

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
        self.first_line = self.match_first_item_in_contents("classdef")
        # Check if we found an element with classdef substring
        if self.first_line == None:
            self.first_line = self.match_first_item_in_contents("function")
            # Check if we found an element with function substring
            if self.first_line != None:
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

    def generate_file_head(self):
        self.file_contents = ("classdef (TestTags = {''}) " + self.classname + " < matlab.unittest.TestCase\n\n")
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

    def generate_function_block(self, function_name):
        self.file_contents += ("        function test_" + function_name + "(testCase)\n\n")
        self.file_contents += ("        % Test Objective:\n")
        self.file_contents += ("        % -------------------------------------------------------------\n\n")
        self.file_contents += ("        % Pass Criteria:\n")
        self.file_contents += ("        % -------------------------------------------------------------\n\n")
        self.file_contents += ("        % Test Input Data:\n")
        self.file_contents += ("        % -------------------------------------------------------------\n\n")
        self.file_contents += ("        % Execute Unit Under Test:\n")
        self.file_contents += ("        % -------------------------------------------------------------\n\n")
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
            print "Test Template already exists in: " + self.fileloc
        else:
            file_handle = open(self.fileloc, "w+") 
            file_handle.write(self.file_contents)
            file_handle.close()


    



