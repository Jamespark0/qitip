import numpy as np
import pytest
from qitip.objects import Inequality

vector_entry: dict[frozenset[int], int] = {
    frozenset((1,)): 0,
    frozenset((2,)): 1,
    frozenset((1, 2)): 2,
}


def test_valid_creation():
    Inequality(vector_entry=vector_entry, v=(1, 0, 0))


def test_intended_numpy_array():
    vector = (1, 0, 0)
    inequality = Inequality(vector_entry=vector_entry, v=vector)
    assert (inequality.coefficients == np.array([vector])).all()
    assert (inequality.coefficients.shape) == (len(vector),)


def test_v_longer_than_entry_mapping():
    with pytest.raises(ValueError):
        Inequality(vector_entry=vector_entry, v=(1, 2, 3, 4))


def test_v_shorter_than_entry_mapping():
    with pytest.raises(ValueError):
        Inequality(vector_entry=vector_entry, v=(1, 2))
