from typing import Iterable

import numpy as np
from qitip.objects import Constraints, Inequality
from qitip.qitip import Qitip


def test_embed_inequality_to_higher_dim() -> None:
    q2 = Qitip(n=2)
    q3 = Qitip(n=3)

    vec: dict[Iterable[int] | int, float] = {(1, 2): 1}

    inq_in_2: Inequality = q2.inequality.from_coefficients(vec)
    inq_in_3: Inequality = q3.embed(inq_in_2)

    expect_inq = q3.inequality.from_coefficients(vec)

    assert np.array_equiv(inq_in_3.coefficients, expect_inq.coefficients)


def test_embed_empty_constraints_to_higher_dim():
    q2 = Qitip(n=2)
    q3 = Qitip(n=3)

    empty_cons_in_2: Constraints = q2.constraints()
    empty_cnos_in_3: Constraints = q3.embed(empty_cons_in_2)

    assert np.array_equiv(empty_cnos_in_3.coefficients, q3.constraints().coefficients)


def test_embed_single_constraints_to_higher_dim() -> None:
    q2 = Qitip(n=2)
    q3 = Qitip(n=3)

    c: tuple[dict[Iterable[int] | int, float]] = ({(1, 2): 1, (1): -1},)

    one_constraint_in_2: Constraints = q2.constraints.from_coefficients(c)
    one_constraint_in_3: Constraints = q3.embed(one_constraint_in_2)

    assert np.array_equiv(
        one_constraint_in_3.coefficients,
        q3.constraints.from_coefficients(c).coefficients,
    )


def test_embed_multi_constraints_to_higher_dim() -> None:
    q2 = Qitip(n=2)
    q3 = Qitip(n=3)

    c: tuple[dict[Iterable[int] | int, float], ...] = (
        {(1, 2): 1, (1): -1},
        {(1,): -1, (2): 1},
    )

    multi_constraints_in_2: Constraints = q2.constraints.from_coefficients(c)
    multi_constraints_in_3: Constraints = q3.embed(multi_constraints_in_2)

    assert np.array_equiv(
        multi_constraints_in_3.coefficients,
        q3.constraints.from_coefficients(c).coefficients,
    )
