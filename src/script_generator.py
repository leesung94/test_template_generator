#!/usr/bin/python

class Script_Generator:

    def __init__(self, lines, filename):
        self.lines = lines
        self.filename = "TEST_" + filename

    def get_filename(self):
        print "Filename is : " + self.filename



