from numpy.typing import ArrayLike

from src.qitip.object_pools import ProverPool, SpacePool
from src.qitip.objects import Constraints, EntropicSpace, Inequality
from src.qitip.prover import Prover


class Qitip:
    _space_pool: SpacePool = SpacePool()
    _prover_pool: ProverPool = ProverPool()

    def __init__(self, n: int):
        self._space: EntropicSpace = self._space_pool.get(n)
        self.prover: Prover = self._prover_pool.get(space=self._space)

    def inequality(self, v: ArrayLike) -> Inequality:
        return Inequality(vector_entry=self._space.vector_entry, v=v)

    def constraints(self, c: ArrayLike | None = None) -> Constraints:
        return Constraints(vector_entry=self._space.vector_entry, c=c)
