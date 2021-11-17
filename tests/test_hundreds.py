import pytest

from hundreds import Hundreds


@pytest.mark.parametrize("word,number", [
    ("صد و هفتاد و دو", 172), ("چهارصد و سی و 5", 435), ("پانصد", 500), ("هفتصد و 20", 720), ("هشت صد", 800),
    ("076", 76), ("67", 67)
])
def test_hundreds(word, number):
    assert Hundreds.get_instance().w2n(word) == number
