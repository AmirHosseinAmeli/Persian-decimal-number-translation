import pytest

from two_digits import TwoDigits


@pytest.mark.parametrize("word,number", [
    ("هفتاد و دو", 72), ("سی و 5", 35), ("پنجاه", 50), ("۷۶", 76), ("5۴", 54), ("95", 95),
    ("شصت و هشت", 68), ("شانزده", 16)
])
def test_two_digits(word, number):
    assert TwoDigits.get_instance().w2n(word) == number
