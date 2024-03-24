from typing import Any

import numpy as np
from numpy.typing import ArrayLike


def validate_vector(
    v: ArrayLike, dim: int
) -> np.ndarray[np.float64, np.dtype[np.float64 | np.int64]]:
    vec: np.ndarray[Any, np.dtype[Any]] = np.array(v)

    vec_shape: tuple = vec.shape

    # check if the shape is that of a vector
    if len(vec_shape) > 1:
        raise ValueError(f"Incorrect shape, {vec_shape}, for a vector, (n, )")
    # check if the vector matches the dimensionality
    elif vec_shape[0] != dim:
        raise ValueError(
            f"Vector dimension, {vec_shape[0]}, inconsistent with the dimension of the system, {dim}"
        )
    # check if all the entries are scalars
    elif vec.dtype != np.float64 and vec.dtype != np.int64:
        raise TypeError("The entries can only be scalars.")
    else:
        return vec


def validate_matrix(
    m: ArrayLike, dim: int
) -> np.ndarray[np.float64, np.dtype[np.float64 | np.int64]]:
    matr: np.ndarray[Any, np.dtype[Any]] = np.array(m)
    matr_shape = matr.shape

    if len(matr_shape) > 2:
        raise ValueError(
            f"Input data is at most converted to a 2D matrix. Data dimension: {len(matr_shape)}"
        )

    elif len(matr_shape) == 1:
        return validate_vector(v=m, dim=dim)

    elif matr.dtype != np.float64 and matr.dtype != np.int64:
        raise TypeError("The entries can only be scalars.")

    else:
        return matr
