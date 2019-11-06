#!/usr/bin/python
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

    def get_first_line(self):
        return self.contents[0]

    def get_function_lines(self):
        # Exclude first line incase the script is a function script
        modified_list = self.contents[1:]
        # Witchcraft TM
        # Gets all lines in the string array which contain the word "function"
        self.function_lines = [line for line in modified_list if "function" in line]
        return self.function_lines

    def get_script_type(self):
        """
        Work out if we are dealing with a class or function script
        """
        first_line = self.get_first_line()
        if "function" in first_line:
            self.is_class = False
        else if "classdef" in first_line:
            self.is_class = True
        return self.is_class

class Script_Generator:

    def __init__(self, lines, filename):
        self.lines = lines
        self.filename = "TEST_" + filename

    def get_filename(self):
        print "Filename is : " + self.filename



