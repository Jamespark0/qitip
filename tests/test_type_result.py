from qitip.objects import (
    Constraints,
    ConstraintsBuilder,
    EntropicSpace,
    Inequality,
    InequalityBuilder,
    result_director,
)
from qitip.prover import Prover


def test_winter_linden_inequality() -> None:
    space = EntropicSpace(n=4)
    constraints: Constraints = ConstraintsBuilder(space.vector_entry).from_coefficients(
        [
            {(2, 3): 1, (1, 2): 1, (1, 2, 3): -1, (2): -1},
            {(1, 2): 1, (1, 3): 1, (1, 2, 3): -1, (1): -1},
            {(1, 4): 1, (2, 4): 1, (1, 2, 4): -1, (4): -1},
        ]
    )
    inequality: Inequality = InequalityBuilder(space.vector_entry).from_coefficients(
        {(4): 1, (3, 4): -1, (1, 2): -1, (1, 2, 3): 1}
    )

    prover: Prover = Prover(space)

    assert result_director(prover, inequality, constraints).status is False
