from dataclasses import InitVar, dataclass, field
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike

from qitip.utils.converters import create_matrix_with_coefficient_list
from qitip.utils.validators import validate_matrix


def update_constraints(
    curr: np.ndarray, new: ArrayLike
) -> np.ndarray[np.float64, np.dtype[np.float64 | np.int64]]:
    # Add the new constraints into the current constraints
    # Also remove duplicate constraints

    # validate if "new" holds valid constraints
    temp = validate_matrix(m=new, dim=curr.shape[1]).reshape((-1, curr.shape[1]))

    return np.unique(np.concatenate((curr, temp)), axis=0)


@dataclass
class Constraints:
    vector_entry: dict[frozenset[int], int]
    c: InitVar[ArrayLike | None] = field(default=None)
    coefficients: np.ndarray = field(init=False)

    def __post_init__(self, c: ArrayLike | None = None):
        if (c is None) or (np.array(c) == 0).all():
            self.coefficients = np.empty((0, len(self.vector_entry)))
            return

        self.coefficients = update_constraints(
            curr=np.empty((0, len(self.vector_entry))), new=c
        )


class ConstraintsBuilder:
    # Constraints builder is chaacterized by the vector entry
    def __init__(self, vector_entry: dict[frozenset[int], int]) -> None:
        self._vector_entry: dict[frozenset[int], int] = vector_entry

    def __call__(self, c: ArrayLike | None = None) -> Constraints:
        """
        When we use cb = ConstraintsBuilder(vectro_entry)
        cb(c) should give us a new Constraints object

        Args:
            c (ArrayLike | None, optional): Constraints in the form
             of a 2D matrix. Defaults to None.
        """

        return Constraints(vector_entry=self._vector_entry, c=c)

    def from_coefficients(
        self, c: Iterable[dict[Iterable[int] | int, float]]
    ) -> Constraints:
        """
        As the number of coefficients increases, it is easier to
        create an object by specifying the coefficients

        Args:
            c (Iterable[dict[Iterable[int]  |  int, float]]):
            A collection of dictionaries where each dictionary defines
            the coefficients of marginal entropies

            format: {marginal system: coefficients}
        """
        return Constraints(
            vector_entry=self._vector_entry,
            c=create_matrix_with_coefficient_list(vector_entry=self._vector_entry)(c),
        )
