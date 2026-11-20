import unittest
from PIL import ImageFont

from scripts.render_poster import is_closing_punctuation, wrap_by_width


class WrapTests(unittest.TestCase):
    def setUp(self):
        self.font = ImageFont.load_default()

    def test_wrap_returns_lines(self):
        lines = wrap_by_width("星星之火可以燎原", self.font, 30)
        self.assertGreaterEqual(len(lines), 1)
        self.assertEqual("".join(lines), "星星之火可以燎原")

    def test_closing_punctuation_is_detected(self):
        self.assertTrue(is_closing_punctuation("。"))
        self.assertFalse(is_closing_punctuation("星"))


if __name__ == "__main__":
    unittest.main()
