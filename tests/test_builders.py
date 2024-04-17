from typing import Iterable, Sequence

import numpy as np
from qitip.objects import (
    Constraints,
    ConstraintsBuilder,
    Inequality,
    InequalityBuilder,
)

# Test with bipartite system for simplicity
vector_entry = {frozenset({1}): 0, frozenset({2}): 1, frozenset({1, 2}): 2}


def test_call_inequality_builder() -> None:
    builder: InequalityBuilder = InequalityBuilder(vector_entry=vector_entry)

    vec: Sequence[float] = (0, 0, 1)
    inequality: Inequality = builder((0, 0, 1))

    assert inequality.coefficients.shape == (len(vector_entry),)
    assert (inequality.coefficients == np.array(vec)).all()


def test_inequality_built_from_coefficients() -> None:
    builder: InequalityBuilder = InequalityBuilder(vector_entry)

    vec: dict[Iterable[int] | int, float] = {(1, 2): 1, (1): -1}

    inequality: Inequality = builder.from_coefficients(vec)

    assert inequality.coefficients.shape == (len(vector_entry),)
    assert (inequality.coefficients == np.array((-1, 0, 1))).all()


def test_constraint_built_from_none_input() -> None:
    builder: ConstraintsBuilder = ConstraintsBuilder(vector_entry)

    constraints: Constraints = builder()

    assert constraints.coefficients.size == 0
    assert constraints.coefficients.shape == (0, len(vector_entry))


def test_constraint_built_from_single_vec() -> None:
    builder: ConstraintsBuilder = ConstraintsBuilder(vector_entry)

    constraints: Constraints = builder((1, 1, -1))

    assert constraints.coefficients.shape == (1, len(vector_entry))
    assert (constraints.coefficients == np.array([[1, 1, -1]])).all()


def test_constraints_built_from_calling_with_multiple_vecs() -> None:
    builder: ConstraintsBuilder = ConstraintsBuilder(vector_entry)

    c = ((1, -1, 0), (-1, 0, 1))

    constraints: Constraints = builder(c)

    assert constraints.coefficients.shape == (len(c), len(vector_entry))
    assert np.array_equiv(
        np.sort(constraints.coefficients, axis=0), np.sort(np.array(c), axis=0)
    )


def test_constraints_built_from_single_coefficients() -> None:
    builder: ConstraintsBuilder = ConstraintsBuilder(vector_entry)

    c: tuple[dict[Iterable[int] | int, float]] = ({(1, 2): 1, (1): -1},)

    constraints: Constraints = builder.from_coefficients(c)

    assert constraints.coefficients.shape == (1, len(vector_entry))
    assert np.array_equiv(constraints.coefficients, np.array([[-1, 0, 1]]))


def test_constraints_built_from_multiple_coefficients() -> None:
    builder: ConstraintsBuilder = ConstraintsBuilder(vector_entry)

    c: tuple[dict[Iterable[int] | int, float], ...] = (
        {(1, 2): 1, (1): -1},
        {(1,): -1, (2): 1},
    )

    constraints = builder.from_coefficients(c)

    assert constraints.coefficients.shape == (len(c), len(vector_entry))
    assert np.array_equiv(
        np.sort(constraints.coefficients, axis=0),
        np.sort(np.array([[-1, 0, 1], [-1, 1, 0]]), axis=0),
    )


def test_constraints_built_from_empty_coefficients() -> None:
    builder: ConstraintsBuilder = ConstraintsBuilder(vector_entry)
    c = (dict(),)

    constraints = builder.from_coefficients(c)

    assert constraints.coefficients.size == 0


def test_constraints_built_from_nothing():
    builder = ConstraintsBuilder(vector_entry)

    empty_constraints: Constraints = builder.from_coefficients([])

    assert empty_constraints.coefficients.size == 0
