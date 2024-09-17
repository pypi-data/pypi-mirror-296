# tests/test_main.py

import unittest
from wrm3_term_colors.main import cs, cp
from wrm3_term_colors.pallette import pallette

class TestMainFunctions(unittest.TestCase):

    def test_color_string(self):
        """Test if color_string returns a string."""
        colored = cs('Test', 'red')
        self.assertIsInstance(colored, str)
        self.assertIn('\033[', colored)  # Check for ANSI escape sequence

    def test_invert_hex(self):
        """Test the invert_hex function."""
        from wrm3_term_colors.cls import CLR
        clr = CLR()
        self.assertEqual(clr.invert_hex('#000000'), '#FFFFFF')
        self.assertEqual(clr.invert_hex('#FFFFFF'), '#000000')
        self.assertEqual(clr.invert_hex('#123456'), '#EDCBA9')

    def test_luminance_inverse_hex(self):
        """Test the luminance_inverse_hex function."""
        from wrm3_term_colors.cls import CLR
        clr = CLR()
        self.assertEqual(clr.luminance_inverse_hex('#FFFFFF'), pallette.get('black'))
        self.assertEqual(clr.luminance_inverse_hex('#000000'), pallette.get('white'))
        self.assertEqual(clr.luminance_inverse_hex('#FF0000'), pallette.get('black'))

    def test_print_colored_text(self):
        """Test the cp function prints without errors."""
        try:
            cp('Hello, Test!', 'green')
        except Exception as e:
            self.fail(f"cp raised an exception {e}")

if __name__ == '__main__':
    unittest.main()