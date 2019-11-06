#!/usr/bin/python

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
        self.function_lines = []
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

    def get_function_lines(self):
        # Exclude first line incase the script is a function script
        modified_list = self.contents[self.first_line:]
        # Witchcraft TM
        # Gets all lines in the string array which contain the word "function"
        self.function_lines = [line for line in modified_list if "function" in line]
        return self.function_lines

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

    def __init__(self, lines, filename):
        self.lines = lines
        self.filename = "TEST_" + filename

    def get_filename(self):
        print "Filename is : " + self.filename



