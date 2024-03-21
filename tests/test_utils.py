from typing import Iterable

from src.qitip.builders import ConstraintsBuilder, InequalityBuilder
from src.qitip.objects import Constraints, Inequality
from src.qitip.qitip import from_coefficients_to_dict

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

    assert vec == from_coefficients_to_dict.convert_inequality(inq)


def test_convert_empty_constraints_to_dict() -> None:
    vec = [
        dict(),
    ]

    builder = ConstraintsBuilder(vector_entry)

    empty_constraint: Constraints = builder.from_coefficients(vec)

    # Note that this returns an empty list rather than vec
    assert [] == from_coefficients_to_dict.convert_constraints(empty_constraint)


def test_convert_single_constraint_to_dict() -> None:
    builder = ConstraintsBuilder(vector_entry)

    c: tuple[dict[Iterable[int] | int, float]] = ({(1, 2): 1, (1,): -1},)

    single_constraints: Constraints = builder.from_coefficients(c)

    assert list(c) == from_coefficients_to_dict.convert_constraints(single_constraints)


def test_convert_multiple_constraints_to_dict() -> None:
    builder: ConstraintsBuilder = ConstraintsBuilder(vector_entry)

    c: tuple[dict[Iterable[int] | int, float], ...] = (
        {(1, 2): 1, (1,): -1},
        {(1,): -1, (2,): 1},
    )

    multi_constraints = builder.from_coefficients(c)

    assert list(c) == from_coefficients_to_dict.convert_constraints(multi_constraints)
