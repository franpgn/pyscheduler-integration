# tests/test_vts.py
import sys
import os
import unittest
from apps.src.vts import VTS  # Importa a função VTS do módulo src.vts

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)


class TestVTS(unittest.TestCase):
    def test_anagram(self):
        self.assertTrue(VTS("listen", "silent"))
        self.assertTrue(VTS("triangle", "integral"))

    def test_not_anagram(self):
        self.assertFalse(VTS("hello", "world"))
        self.assertFalse(VTS("python", "java"))

    def test_different_lengths(self):
        self.assertFalse(VTS("short", "longer"))

    def test_case_sensitivity(self):
        self.assertFalse(VTS("Listen", "silent"))
        self.assertTrue(VTS("Dormitory", "dirtyroom"))

    def test_empty_strings(self):
        self.assertTrue(VTS("", ""))
        self.assertFalse(VTS("nonempty", ""))

    def test_single_character(self):
        self.assertTrue(VTS("a", "a"))
        self.assertFalse(VTS("a", "b"))

    def test_with_spaces(self):
        self.assertTrue(VTS("a b c", "c a b"))
        self.assertFalse(VTS("a b c", "a b c "))


if __name__ == "__main__":
    unittest.main()
