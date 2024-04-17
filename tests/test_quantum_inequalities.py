import numpy as np
import pytest
from qitip.objects import EntropicSpace
from qitip.quantum_inequalities import QuantumElementalInequalities


def test_one_system_all_inequalities():
    n: int = 1

    space: EntropicSpace = EntropicSpace(n=n)

    with pytest.raises(ValueError):
        QuantumElementalInequalities(vector_entry=space.vector_entry).get_elementals()


def test_two_system_type_1() -> None:
    n: int = 2
    space = EntropicSpace(n=n)

    quantum_ineqality = QuantumElementalInequalities(vector_entry=space.vector_entry)
    intended_inequalities = np.array([[1, 1, -1]])

    type_1_inequalities = quantum_ineqality._get_all_type_1()
    num_inequalities = type_1_inequalities.shape[0]

    assert num_inequalities == 1
    assert all(
        [inequality in type_1_inequalities for inequality in intended_inequalities]
    )


def test_three_system_type_1() -> None:
    n: int = 3

    space = EntropicSpace(n)

    quantum_inequality = QuantumElementalInequalities(space.vector_entry)
    intended_inequalities = np.array(
        [
            [0, 0, -1, 0, 1, 1, -1],
            [1, 1, 0, -1, 0, 0, 0],
            [0, -1, 0, 1, 0, 1, -1],
            [1, 0, 1, 0, -1, 0, 0],
            [-1, 0, 0, 1, 1, 0, -1],
            [0, 1, 1, 0, 0, -1, 0],
        ]
    )

    type_1_inequalities = quantum_inequality._get_all_type_1()
    num_inequalities: int = type_1_inequalities.shape[0]

    assert num_inequalities == 6
    assert all(
        [inequality in type_1_inequalities for inequality in intended_inequalities]
    )


def test_ten_system_type_1() -> None:
    n: int = 10

    space = EntropicSpace(n)

    quantum_inequality = QuantumElementalInequalities(space.vector_entry)
    num_inequalities = quantum_inequality._get_all_type_1().shape[0]

    assert num_inequalities == 10 * 9 * 2 ** (7)


def test_two_system_type2() -> None:
    n: int = 2

    space = EntropicSpace(n=n)

    quantum_inequality = QuantumElementalInequalities(space.vector_entry)
    intended_inequalities = np.array([[1, -1, 1], [-1, 1, 1]])

    type_2_inequalities = quantum_inequality._get_all_type_2()
    num_inequalities_t2 = type_2_inequalities.shape[0]

    assert num_inequalities_t2 == 2
    assert all(
        [inequality in type_2_inequalities for inequality in intended_inequalities]
    )


def test_three_system_type2() -> None:
    n: int = 3

    space = EntropicSpace(n)

    quantum_inequality = QuantumElementalInequalities(space.vector_entry)
    intended_inequalities = np.array(
        [
            [0, -1, -1, 1, 0, 1, 0],
            [1, 0, 0, 0, 0, -1, 1],
            [-1, 0, -1, 1, 0, 1, 0],
            [0, 1, 0, 0, -1, 0, 1],
            [-1, -1, 0, 0, 1, 1, 0],
            [0, 0, 1, -1, 0, 0, 1],
        ]
    )

    type_2_inequalities = quantum_inequality._get_all_type_2()
    num_inequality_t2 = type_2_inequalities.shape[0]

    assert num_inequality_t2 == n * 2 ** (n - 2)
    assert all(
        [inequality in type_2_inequalities for inequality in intended_inequalities]
    )


def test_ten_system_type2() -> None:
    n: int = 10

    space = EntropicSpace(n)

    quantum_inequality = QuantumElementalInequalities(space.vector_entry)
    num_inequality_t2 = quantum_inequality._get_all_type_2().shape[0]

    assert num_inequality_t2 == n * 2 ** (n - 2)
