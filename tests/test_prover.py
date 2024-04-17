import numpy as np
from numpy.typing import NDArray
from qitip.objects import EntropicSpace
from qitip.prover import Prover

# from qitip.quantum_inequalities import QuantumElementalInequalities

"""
The prover can also be applied in the classical regime by replacing 
QuantumElementalInequalities(space).ELEMENtAL with ShannonInequality(space).ELEMMENTAL
"""


def test_quantum_strong_subadditivity() -> None:
    n: int = 3
    space = EntropicSpace(n)
    # prover = Prover(
    #     elemental=QuantumElementalInequalities(
    #         vector_entry=space.vector_entry
    #     ).get_elementals(),
    #     n=n,
    # )
    prover = Prover(space=space)
    inequality: NDArray[np.float64] = np.zeros(len(space.vector_entry))
    inequality[space.vector_entry[frozenset({1, 2, 3})]] = -1
    inequality[space.vector_entry[frozenset({3})]] = -1
    inequality[space.vector_entry[frozenset({1, 3})]] = 1
    inequality[space.vector_entry[frozenset({2, 3})]] = 1

    assert prover._check_type(
        inequality=inequality, constraints=np.empty((0, len(space.vector_entry)))
    )


def test_quantum_weak_monotonacity() -> None:
    n: int = 3
    space = EntropicSpace(n=n)
    # prover = Prover(
    #     elemental=QuantumElementalInequalities(
    #         vector_entry=space.vector_entry
    #     ).get_elementals(),
    #     n=n,
    # )
    prover = Prover(space=space)

    inequality = np.zeros(len(space.vector_entry))

    inequality[space.vector_entry[frozenset({1})]] = -1
    inequality[space.vector_entry[frozenset({2})]] = -1
    inequality[space.vector_entry[frozenset({1, 3})]] = 1
    inequality[space.vector_entry[frozenset({2, 3})]] = 1

    assert prover._check_type(
        inequality=inequality, constraints=np.empty((0, len(space.vector_entry)))
    )


def test_conditional_von_neumann_entropy() -> None:
    n: int = 2

    space = EntropicSpace(n=n)
    # prover = Prover(
    #     elemental=QuantumElementalInequalities(
    #         vector_entry=space.vector_entry
    #     ).get_elementals(),
    #     n=n,
    # )
    prover = Prover(space=space)
    inequality = np.zeros(len(space.vector_entry))

    inequality[space.vector_entry[frozenset({1, 2})]] = 1
    inequality[space.vector_entry[frozenset({2})]] = -1

    assert (
        prover._check_type(
            inequality=inequality,
            constraints=np.empty((0, len(space.vector_entry))),
        )
        is False
    )


def test_constrained_non_von_neumann_type() -> None:
    n: int = 4

    space = EntropicSpace(n=n)
    # prover = Prover(
    #     elemental=QuantumElementalInequalities(
    #         vector_entry=space.vector_entry
    #     ).get_elementals(),
    #     n=n,
    # )
    prover = Prover(space=space)

    constraints = np.zeros((3, len(space.vector_entry)))
    # I(C;A|B) = 0
    constraints[0][space.vector_entry[frozenset({2, 3})]] = 1
    constraints[0][space.vector_entry[frozenset({1, 2})]] = 1
    constraints[0][space.vector_entry[frozenset({1, 2, 3})]] = -1
    constraints[0][space.vector_entry[frozenset({2})]] = -1
    # I(B;C|A) = 0
    constraints[1][space.vector_entry[frozenset({1, 2})]] = 1
    constraints[1][space.vector_entry[frozenset({1, 3})]] = 1
    constraints[1][space.vector_entry[frozenset({1, 2, 3})]] = -1
    constraints[1][space.vector_entry[frozenset({1})]] = -1
    # I(A;B|D) = 0
    constraints[2][space.vector_entry[frozenset({1, 4})]] = 1
    constraints[2][space.vector_entry[frozenset({2, 4})]] = 1
    constraints[2][space.vector_entry[frozenset({1, 2, 4})]] = -1
    constraints[2][space.vector_entry[frozenset({4})]] = -1

    inequality = np.zeros(len(space.vector_entry))
    # I(C;D) >= I(C;AB)
    # equivalently, (S_{c} + S_{d} - S_{c,d}) - (S_{c} + S_{ab} - S_{abc}) >= 0
    inequality[space.vector_entry[frozenset({4})]] = 1
    inequality[space.vector_entry[frozenset({3, 4})]] = -1
    inequality[space.vector_entry[frozenset({1, 2})]] = -1
    inequality[space.vector_entry[frozenset({1, 2, 3})]] = 1

    assert prover._check_type(inequality=inequality, constraints=constraints) is False


def test_quantum_zhang_yeung_inequality() -> None:
    n: int = 4
    space = EntropicSpace(n)

    prover = Prover(space=space)

    inequality = np.zeros(len(space.vector_entry))
    # Zhang-Yeung Inequality in canonical form
    inequality[space.vector_entry[frozenset({1})]] = -2
    inequality[space.vector_entry[frozenset({2})]] = -2
    inequality[space.vector_entry[frozenset({3})]] = -1
    inequality[space.vector_entry[frozenset({1, 4})]] = 1
    inequality[space.vector_entry[frozenset({2, 4})]] = 1
    inequality[space.vector_entry[frozenset({3, 4})]] = -1
    inequality[space.vector_entry[frozenset({1, 2})]] = 3
    inequality[space.vector_entry[frozenset({1, 3})]] = 3
    inequality[space.vector_entry[frozenset({2, 3})]] = 3
    inequality[space.vector_entry[frozenset({1, 2, 3})]] = -4
    inequality[space.vector_entry[frozenset({1, 2, 4})]] = -1

    assert (
        prover._check_type(
            inequality, constraints=np.empty((0, len(space.vector_entry)))
        )
        is False
    )
