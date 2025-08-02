from calculator import add
from calculator import minus 

def test_main():

    result = add.add(2,2)
    assert result == 4


    result = add.add(0,0)
    assert result == 0

    result = minus.minus(0,0)
    assert result == 0

    result = minus.minus(10,2)
    assert result == 8

