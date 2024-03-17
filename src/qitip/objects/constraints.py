from dataclasses import InitVar, dataclass, field

import numpy as np
from numpy.typing import ArrayLike

from src.qitip.validators import validate_matrix


def update_constraints(
    curr: np.ndarray, new: ArrayLike
) -> np.ndarray[np.float64, np.dtype[np.float64 | np.int64]]:
    # Add the new constraints into the current constraints
    # Also remove duplicate constraints

    # validate if "new" holds valid constraints
    temp = validate_matrix(m=new, dim=curr.shape[1]).reshape((-1, curr.shape[1]))

    return np.unique(np.vstack((curr, temp)), axis=0)


@dataclass
class Constraints:
    vector_entry: dict[frozenset[int], int]
    c: InitVar[ArrayLike | None] = field(default=None)
    constraints: np.ndarray = field(init=False)

    def __post_init__(self, c: ArrayLike | None = None):
        if c is None:
            self.constraints = np.empty((0, len(self.vector_entry)))
            return

        self.constraints = update_constraints(
            curr=np.empty((0, len(self.vector_entry))), new=c
        )

    # TODO: classmethod to create constraints based on coefficients
    @classmethod
    def from_coefficients(cls, **kwargs): ...
