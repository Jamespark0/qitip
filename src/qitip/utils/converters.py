from itertools import compress
from typing import Any, Callable, Iterable

from numpy import dtype, float64, int8, ndarray


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


def vector_entry_to_ordered_sys(
    vector_entry: dict[frozenset[int], int]
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(k) for k, _ in sorted(vector_entry.items(), key=lambda item: item[1])
    )


def frozenset_to_marginal_entropy(parties: frozenset[int]) -> str:
    return f"S({', '.join(tuple(str(party) for party in parties))})"


def canonical_to_expression(party_coefficient: dict[frozenset[int], float]) -> str:
    exp: str = " ".join(
        [
            (
                f"+ {coefficient} * {frozenset_to_marginal_entropy(party)}"
                if coefficient >= 0
                else f"- {abs(coefficient)} * {frozenset_to_marginal_entropy(party)}"
            )
            for party, coefficient in party_coefficient.items()
        ]
    )

    return exp if exp[0] == "-" else exp[2:]


class CoefficientsToDict:
    # This function takes an object (can either be Inequality or Constraints) to
    # 1D arraylike or 2D arraylike
    @staticmethod
    def convert_vector(
        vector_entry: dict[Any, int],
        coefficients: ndarray[float64, dtype[float64]],
    ) -> dict[Any, float]:
        non_zeros: ndarray[ndarray[bool, dtype[int8]], dtype[int8]] = coefficients != 0

        # Ensures the sys is in the same order as the vectors
        sys_in_order: tuple[tuple[int, ...], ...] = vector_entry_to_ordered_sys(
            vector_entry
        )

        # since each Inequality only contains one inequality
        return dict(
            zip(
                compress(sys_in_order, non_zeros),
                compress(coefficients, non_zeros),
            )
        )

    @staticmethod
    def convert_matrix(
        vector_entry: dict[Any, int],
        coefficients: ndarray[float64, dtype[float64]],
    ) -> list[dict[Any, float]]:
        non_zeros: ndarray[ndarray[bool, dtype[int8]], dtype[int8]] = coefficients != 0

        # Ensures the sys is in the same order as the vectors
        sys_in_order: tuple[tuple[int, ...], ...] = vector_entry_to_ordered_sys(
            vector_entry
        )

        return [
            dict(
                zip(
                    compress(sys_in_order, non_zero),
                    compress(coefficients[index], non_zero),
                )
            )
            for index, non_zero in enumerate(non_zeros)
        ]
