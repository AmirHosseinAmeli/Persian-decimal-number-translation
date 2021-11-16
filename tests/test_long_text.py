import re

import pytest

from thousand import Thousand


@pytest.mark.parametrize("text,num_list", [
    ("حاصل جمع صد و ده و یکصدو بیست برابر دویست و سی می شود.", [110, 120, 230]),
    ("صد و بیست و 2 انسان", [122]),
])
def test_long_text(text, num_list):
    recognizer = Thousand.get_instance()
    result = [recognizer.w2n(match.group()) for match in re.finditer(recognizer.non_capturing_pats(), text)]
    assert result == num_list
