from fancylists.fancylists import letter_index_to_number

def test_single_lowercase_letter():
    assert letter_index_to_number('a', 'a') == 1
    assert letter_index_to_number('b', 'a') == 2
    assert letter_index_to_number('z', 'a') == 26

def test_multiple_lowercase_letters():
    assert letter_index_to_number('aa', 'a') == 27
    assert letter_index_to_number('ab', 'a') == 28
    assert letter_index_to_number('az', 'a') == 52
    assert letter_index_to_number('ba', 'a') == 53
    assert letter_index_to_number('zz', 'a') == 702

def test_single_uppercase_letter():
    assert letter_index_to_number('A', 'A') == 1
    assert letter_index_to_number('B', 'A') == 2
    assert letter_index_to_number('Z', 'A') == 26

def test_multiple_uppercase_letters():
    assert letter_index_to_number('AA', 'A') == 27
    assert letter_index_to_number('AB', 'A') == 28
    assert letter_index_to_number('AZ', 'A') == 52
    assert letter_index_to_number('BA', 'A') == 53
    assert letter_index_to_number('ZZ', 'A') == 702
