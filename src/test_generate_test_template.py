#!/usr/bin/python
import unittest
import generate_test_template

class TemplateGeneration(unittest.TestCase):

    def test_get_class_script_type(self):
        line = "classdef BasicClass"
        is_class = generate_test_template.get_script_type(line)
        self.assertTrue(is_class)

if __name__ == '__main__':
    unittest.main()