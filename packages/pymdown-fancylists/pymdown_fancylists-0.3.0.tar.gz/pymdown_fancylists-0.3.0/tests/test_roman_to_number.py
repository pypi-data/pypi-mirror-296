from fancylists.fancylists import roman_to_number

def test_roman_values():
    assert roman_to_number('i') == 1
    assert roman_to_number('v') == 5
    assert roman_to_number('x') == 10
    assert roman_to_number('l') == 50
    assert roman_to_number('c') == 100
    assert roman_to_number('d') == 500
    assert roman_to_number('m') == 1000


def test_non_roman_values():
    assert roman_to_number('a') == None
    assert roman_to_number('b') == None
    assert roman_to_number('e') == None
    assert roman_to_number('z') == None


def test_roman_additions():
    assert roman_to_number('ii') == 2
    assert roman_to_number('iii') == 3
    assert roman_to_number('vi') == 6
    assert roman_to_number('vii') == 7
    assert roman_to_number('xi') == 11
    assert roman_to_number('xv') == 15
    assert roman_to_number('xvi') == 16
    assert roman_to_number('xx') == 20
    assert roman_to_number('xxi') == 21
    assert roman_to_number('xxv') == 25
    assert roman_to_number('xxvi') == 26
    assert roman_to_number('lx') == 60


def test_roman_subtractions():
    assert roman_to_number('iv') == 4
    assert roman_to_number('ix') == 9
    assert roman_to_number('xl') == 40
    assert roman_to_number('xc') == 90
    assert roman_to_number('cd') == 400
    assert roman_to_number('cm') == 900


# def test_roman_invalid_subtractions():
#     assert roman_to_number('il') == None
#     assert roman_to_number('ic') == None


def test_roman_combinations():
    assert roman_to_number('xiv') == 14
    assert roman_to_number('xix') == 19
    assert roman_to_number('xliv') == 44
