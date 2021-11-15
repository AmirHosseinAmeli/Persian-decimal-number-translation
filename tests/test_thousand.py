import pytest

from thousand import Thousand


@pytest.mark.parametrize("word,number", [
    ("یک هزار و صد و هفتاد و دو", 1172), ("هزار و صد و هفتاد و دو", 1172), ("100 هزار و 172", 100172),
    ("ده هزار و پنج", 10005), ("ده هزار و سیصد و ده", 10310), ("چهارصد و ۵۷ هزار و هشتاد و نه", 457089)
])
def test_thousand(word, number):
    assert Thousand.get_instance().w2n(word) == number
