from fancylists.fancylists import letter_to_number

def test_single_lowercase_letter():
    assert letter_to_number('a') == 1
    assert letter_to_number('b') == 2
    assert letter_to_number('z') == 26

def test_multiple_lowercase_letters():
    assert letter_to_number('aa') == 27
    assert letter_to_number('ab') == 28
    assert letter_to_number('az') == 52
    assert letter_to_number('ba') == 53
    assert letter_to_number('zz') == 702
