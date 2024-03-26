# Information inequality is studied in entropic space
# It is responsible for specifying the meaning for each axis
# Given an n-party quantum system, each axis represents an element in the superset of {1,2,...,n}
from dataclasses import dataclass, field
from itertools import combinations


@dataclass
class EntropicSpace:
    """
    Generate all possible pairs from n random variables.

    The class includes information of

    1. All the pairs

    2. The index in an entropic vector that corresponds to the given pairing
    """

    # Number of parties
    n: int
    _all_pairs: tuple[frozenset[int], ...] = field(init=False)
    _vector_entry: dict[frozenset[int], int] = field(init=False)

    def __hash__(self) -> int:
        return hash((self.n))

    def __post_init__(self):
        self._all_pairs: tuple[frozenset[int], ...] = self.generate_all_pairs(self.n)
        self._vector_entry: dict[frozenset[int], int] = {
            v: k for k, v in enumerate(self._all_pairs)
        }

    # Properties
    @property
    def vector_entry(self) -> dict[frozenset[int], int]:
        return self._vector_entry

    @staticmethod
    def generate_all_pairs(n: int) -> tuple[frozenset[int], ...]:
        labeling: set = set(range(1, n + 1))

        return tuple(
            frozenset(group)
            for size in range(1, n + 1)
            for group in combinations(labeling, r=size)
        )


class SpacePool:
    def __init__(self):
        self._created: set[EntropicSpace] = set()

    def get(self, n: int) -> EntropicSpace:
        for s in self._created:
            if s.n == n:
                return s

        new_space = EntropicSpace(n=n)
        self._created.add(new_space)
        return new_space
