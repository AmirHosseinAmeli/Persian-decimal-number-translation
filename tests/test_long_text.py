import re

from thousand import Thousand


def test_long_text():
    recognizer = Thousand.get_instance()
    text = "حاصل جمع صد و ده و یکصدو بیست برابر دویست و سی می شود."
    result = [recognizer.w2n(match.group()) for match in re.finditer(recognizer.non_capturing_pats(), text)]
    assert result == [110, 120, 230]

