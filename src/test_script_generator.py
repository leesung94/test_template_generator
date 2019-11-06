#!/usr/bin/python
import unittest
import script_generator as sg

class ContentExtractor(unittest.TestCase):
    
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

class ScriptGenerator(unittest.TestCase):

    def test_create_object(self):
        inst = sg.Script_Generator("hello","world")
        self.assertIsInstance(inst, sg.Script_Generator)

    def test_creation_filename(self):
        inst = sg.Script_Generator("hello","world")
        self.assertEqual(inst.filename, "TEST_world")

if __name__ == '__main__':
    unittest.main()