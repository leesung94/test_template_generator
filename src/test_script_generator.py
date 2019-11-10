#!/usr/bin/python

# Author:
#   Lee Sung

# This test have been written using UNIX paths for files

# Libraries
import unittest

# User Defined
import script_generator as sg

class ContentExtractor(unittest.TestCase):

    def create_basic_inst(self, filepath):
        inst = sg.Contents_Extractor(filepath)
        inst.open_file()
        inst.read_contents()
        inst.close_file()
        return inst
    
    def test_create_object(self):
        inst = sg.Contents_Extractor("../test/class.m")
        self.assertIsInstance(inst, sg.Contents_Extractor)

    def test_open_real_file(self):
        inst = sg.Contents_Extractor("../test/class.m")
        result = inst.open_file()
        inst.close_file()
        self.assertEquals(result, 0)
        self.assertEqual(inst.filename, "class.m")
        self.assertEqual(inst.directory, "../test")

    def test_open_fake_file(self):
        inst = sg.Contents_Extractor("../notapath/")
        result = inst.open_file()
        self.assertEquals(result, 1)

    def test_exist_substring(self):
        inst = self.create_basic_inst("../test/class.m")
        result = inst.match_first_item_in_contents("classdef")
        self.assertEquals(result, 0)

    def test_nonexist_substring(self):
        inst = self.create_basic_inst("../test/class.m")
        result = inst.match_first_item_in_contents("nonexistence")
        self.assertEquals(result, None)

    def test_no_start_exist_substring(self):
        inst = self.create_basic_inst("../test/func2.m")
        result = inst.match_first_item_in_contents("function")
        self.assertEquals(result, 1)

    def test_class_get_script_type(self):
        inst = self.create_basic_inst("../test/class.m")
        result = inst.get_script_type()
        self.assertTrue(result)

    def test_func_get_script_type(self):
        inst = self.create_basic_inst("../test/func1.m")
        result = inst.get_script_type()
        self.assertFalse(result)

    def test_none_get_script_type(self):
        inst = self.create_basic_inst("../test/notscript.m")
        result = inst.get_script_type()
        self.assertEquals(result, None)

    def test_class_func_count(self):
        inst = self.create_basic_inst("../test/class.m")
        inst.get_script_type()
        result = inst.get_functions()
        self.assertEqual(len(result), 2)

    def test_func_func_count(self):
        inst = self.create_basic_inst("../test/func1.m")
        inst.get_script_type()
        result = inst.get_functions()
        self.assertEqual(len(result), 1)

class ScriptGenerator(unittest.TestCase):

    def test_create_object(self):
        inst = sg.Script_Generator("hello",".")
        self.assertIsInstance(inst, sg.Script_Generator)

    def test_creation_filename(self):
        inst = sg.Script_Generator("hello",".")
        self.assertEqual(inst.filename, "TEST_hello")

if __name__ == '__main__':
    unittest.main()