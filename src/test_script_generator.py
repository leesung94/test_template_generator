#!/usr/bin/python
import unittest
import script_generator as sg

class ScriptGeneration(unittest.TestCase):

    def test_create_object(self):
        inst = sg.Script_Generator("hello","world")
        self.assertIsInstance(inst, sg.Script_Generator)

    def test_creation_filename(self):
        inst = sg.Script_Generator("hello","world")
        self.assertEqual(inst.filename, "TEST_world")

if __name__ == '__main__':
    unittest.main()