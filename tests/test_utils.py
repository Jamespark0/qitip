from typing import Iterable

from qitip.objects import (
    Constraints,
    ConstraintsBuilder,
    Inequality,
    InequalityBuilder,
)
from qitip.utils.converters import CoefficientsToDict

# Test with bipartite system for simplicity
vector_entry: dict[frozenset[int], int] = {
    frozenset({1}): 0,
    frozenset({2}): 1,
    frozenset({1, 2}): 2,
}


def test_convert_inequality_coefficients_to_dict() -> None:
    vec: dict[Iterable[int] | int, float] = {(1, 2): 1, (1,): -1}

    builder = InequalityBuilder(vector_entry)
    inq: Inequality = builder.from_coefficients(vec)

    assert vec == CoefficientsToDict.convert_vector(inq.vector_entry, inq.coefficients)


def test_convert_empty_constraints_to_dict() -> None:
    vec = [
        dict(),
    ]

    builder = ConstraintsBuilder(vector_entry)

    empty_constraint: Constraints = builder.from_coefficients(vec)

    # Note that this returns an empty list rather than vec
    assert [] == CoefficientsToDict.convert_matrix(
        empty_constraint.vector_entry, empty_constraint.coefficients
    )


def test_convert_single_constraint_to_dict() -> None:
    builder = ConstraintsBuilder(vector_entry)

    c: tuple[dict[Iterable[int] | int, float]] = ({(1, 2): 1, (1,): -1},)

    single_constraints: Constraints = builder.from_coefficients(c)

    assert list(c) == CoefficientsToDict.convert_matrix(
        single_constraints.vector_entry, single_constraints.coefficients
    )


def test_convert_multiple_constraints_to_dict() -> None:
    builder: ConstraintsBuilder = ConstraintsBuilder(vector_entry)

    c: tuple[dict[Iterable[int] | int, float], ...] = (
        {(1, 2): 1, (1,): -1},
        {(1,): -1, (2,): 1},
    )

    multi_constraints = builder.from_coefficients(c)

    assert list(c) == CoefficientsToDict.convert_matrix(
        multi_constraints.vector_entry, multi_constraints.coefficients
    )
