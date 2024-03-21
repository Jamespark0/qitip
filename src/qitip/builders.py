from typing import Callable, Iterable, Optional

from numpy.typing import ArrayLike

from src.qitip.objects import Constraints, Inequality


def convert_iterable_int_to_set(key: Iterable[int] | int) -> frozenset[int]:
    if isinstance(key, int):
        return frozenset({key})
    elif all([isinstance(i, int) for i in key]):
        return frozenset(key)
    else:
        raise TypeError(
            f"Key, {key} can either be an integer or a sequence of integers."
        )


def create_vector_with_coefficient(
    vector_entry: dict[frozenset[int], int]
) -> Callable[[dict[Iterable[int] | int, float]], tuple[float, ...]]:
    def assign_coefficients(
        coefficients: dict[Iterable[int] | int, float]
    ) -> tuple[float, ...]:
        sys_coefficients: dict[frozenset[int], float] = {
            convert_iterable_int_to_set(k): v for k, v in coefficients.items()
        }

        # Create a tuple of coeffcients in the order of vector entry
        # If the coefficient is not assigned by the user, it is set to 0
        # Otherwise, use the user-assigned coefficient
        return tuple(
            sys_coefficients[key] if sys_coefficients.get(key, None) else 0
            for key in vector_entry.keys()
        )

    return assign_coefficients


def create_matrix_with_coefficient_list(
    vector_entry: dict[frozenset[int], int]
) -> Callable[
    [Iterable[dict[Iterable[int] | int, float]]], tuple[tuple[float, ...], ...]
]:
    def assign_coefficients(
        coefficient_list: Iterable[dict[Iterable[int] | int, float]]
    ) -> tuple[tuple[float, ...], ...]:
        return tuple(
            [
                create_vector_with_coefficient(vector_entry)(coefficients)
                for coefficients in coefficient_list
            ]
        )

    return assign_coefficients


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


class ConstraintsBuilder:
    # Constraints builder is chaacterized by the vector entry
    def __init__(self, vector_entry: dict[frozenset[int], int]) -> None:
        self._vector_entry: dict[frozenset[int], int] = vector_entry

    # When we use cb = ConstraintsBuilder(vectro_entry)
    # cb(c) should give us a new Constraints object
    def __call__(self, c: ArrayLike | None = None) -> Constraints:
        return Constraints(vector_entry=self._vector_entry, c=c)

    # As the number of coefficients increases, it is easier to
    # create an object by specifying the coefficients
    # But only one constraint can be created with this method
    def from_coefficients(
        self, c: Iterable[dict[Iterable[int] | int, float]]
    ) -> Constraints:
        return Constraints(
            vector_entry=self._vector_entry,
            c=create_matrix_with_coefficient_list(vector_entry=self._vector_entry)(c),
        )
