import pytest

from app.calculator import add,divide
@pytest.mark.smoke
def test_add():
    assert add(10,10)==20

@pytest.mark.regression
def test_divide():
    assert divide(20,4)==5

@pytest.mark.regression
def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10,0)