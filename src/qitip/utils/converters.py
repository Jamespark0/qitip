from itertools import compress
from typing import Any

from numpy import dtype, float64, int8, ndarray


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
