# Inequality is responsible for storing the information of
# 1. the information inequality given by the user in the "canoncial form"
# 2. the mapping between entries in the vector and the marginal entropy

from dataclasses import InitVar, dataclass, field

import numpy as np
from numpy.typing import ArrayLike

from src.qitip.objects import EntropicSpace
from src.qitip.validators import validate_vector


@dataclass
class Inequality:
    vector_entry: dict[frozenset[int], int]
    v: InitVar[ArrayLike]
    vector: np.ndarray = field(init=False)

    def __post_init__(self, v):
        self.vector = validate_vector(v=v, dim=len(self.vector_entry)).reshape((1, -1))

    def embed(self, space: EntropicSpace):
        raise NotImplementedError("To be implemented ...")
