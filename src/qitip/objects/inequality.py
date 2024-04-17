# Inequality is responsible for storing the information of
# 1. the information inequality given by the user in the "canoncial form"
# 2. the mapping between entries in the vector and the marginal entropy

from dataclasses import InitVar, dataclass, field
from typing import Iterable, Optional

import numpy as np
from numpy.typing import ArrayLike

from qitip.utils.converters import create_vector_with_coefficient
from qitip.utils.validators import validate_vector


@dataclass
class Inequality:
    vector_entry: dict[frozenset[int], int]
    v: InitVar[ArrayLike]
    coefficients: np.ndarray = field(init=False)

    def __post_init__(self, v):
        self.coefficients = validate_vector(v=v, dim=len(self.vector_entry)).reshape(
            (-1,)
        )


class InequalityBuilder:
    # Inequality builder is chaacterized by the vector entry
    def __init__(self, vector_entry: dict[frozenset[int], int]):
        self._vector_entry: dict[frozenset[int], int] = vector_entry

    # When we use ib = InequalityBuilder(vectro_entry)
    # ib(v) should give us a new Inequality object
    def __call__(self, v: Optional[ArrayLike] = None) -> Inequality:
        if v is None:
            raise TypeError(
                f"Qitip(n).inequality(v) missing 1 required positional argument: 'v' which has the dimension of '{len(self._vector_entry)}'"
            )
        return Inequality(vector_entry=self._vector_entry, v=v)

    # As the number of coefficients increases, it is easier to
    # create an object by specifying the coefficients
    def from_coefficients(self, v: dict[Iterable[int] | int, float]) -> Inequality:
        return Inequality(
            vector_entry=self._vector_entry,
            v=create_vector_with_coefficient(vector_entry=self._vector_entry)(v),
        )
