from itertools import combinations

import numpy as np
from numpy.typing import NDArray


class QuantumElementalInequalities:
    """
    The elemental inequalities are based on the paper by Pippenger

    1. Delta(I, J) >= 0 which are referred to as type 1
        I - J = {i} and J - I = {j} and i >= j
    2. E(I, J) >=0 which are referred to as type 2
        I ∩ J = {k} and k+1 ∈ I and I ∪ J = {1,2,...,N}
    """

    def __init__(self, vector_entry: dict[frozenset[int], int]):
        self.vector_entry: dict[frozenset[int], int] = vector_entry
        self.entire_system: frozenset[int] = max(self.vector_entry.keys())
        self.n: int = max(self.entire_system)

        if self.n < 2:
            raise ValueError(
                f"Number of quantum systems should be >= 2; {self.n} is given instead."
            )

    def _get_type_1_elemental_vector(self, i: int, j: int) -> NDArray[np.int64]:
        remaining: frozenset[int] = self.entire_system - {i, j}

        elemental_i_j: NDArray = np.empty((0, len(self.vector_entry)))

        # Combinations run from r = 0 to r = num of all remainings
        for r in range(len(remaining) + 1):
            for intersection in combinations(remaining, r):
                set_i = frozenset(intersection).union({i})
                set_j = frozenset(intersection).union({j})

                vector = np.zeros(len(self.vector_entry))
                vector[self.vector_entry[set_i]] = 1
                vector[self.vector_entry[set_j]] = 1
                vector[self.vector_entry[frozenset(set_i.union(set_j))]] = -1

                # Exclude intersections being empty
                if intersection != tuple():
                    vector[self.vector_entry[frozenset(intersection)]] = -1

                elemental_i_j = np.vstack((elemental_i_j, vector))

        return elemental_i_j

    def _get_type_2_elemental_vector(self, k: int) -> NDArray[np.int64]:
        intersection = {k}

        i_diff_j = {(k + 1) % self.n if k + 1 > self.n else k + 1}

        remaining = self.entire_system - intersection - i_diff_j

        elemental_k: NDArray[np.int64] = np.empty(
            (0, len(self.vector_entry)), dtype=np.int8
        )

        for r in range(0, len(remaining) + 1):
            for i_remaning in combinations(remaining, r):
                vec = np.zeros(len(self.vector_entry))

                i_remaning = frozenset(i_remaning)
                j_remaining = remaining.difference(i_remaning)
                set_i = (i_remaning.union(i_diff_j)).union(intersection)
                set_j = j_remaining.union(intersection)

                vec[self.vector_entry[set_i]] = 1
                vec[self.vector_entry[set_j]] = 1
                vec[self.vector_entry[set_i.difference(set_j)]] = -1
                if j_remaining != frozenset():
                    vec[self.vector_entry[set_j.difference(set_i)]] = -1

                elemental_k: NDArray[np.int64] = np.vstack((elemental_k, vec))

        return elemental_k

    def _get_all_type_1(self):
        all_type_1: NDArray = np.empty((0, len(self.vector_entry)))
        for group in self.vector_entry.keys():
            if len(group) > 2:
                break
            elif len(group) == 2:
                i, j = group
                all_type_1 = np.vstack(
                    (all_type_1, self._get_type_1_elemental_vector(i, j))
                )
        return all_type_1

    def _get_all_type_2(self):
        all_type_2 = np.empty((0, len(self.vector_entry)))
        for k in range(1, self.n + 1):
            all_type_2 = np.vstack((all_type_2, self._get_type_2_elemental_vector(k=k)))

        return all_type_2

    def get_elementals(self) -> NDArray[np.float64]:
        return np.vstack((self._get_all_type_1(), self._get_all_type_2()))
