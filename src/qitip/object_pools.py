from qitip.prover import Prover
from src.qitip.objects import EntropicSpace


class SpacePool:
    def __init__(self):
        self.created: set[EntropicSpace] = set()

    def get(self, n: int) -> EntropicSpace:
        for s in self.created:
            if s.n == n:
                return s

        new_space = EntropicSpace(n=n)
        self.created.add(new_space)
        return new_space


class ProverPool:
    def __init__(self) -> None:
        self.created: set[Prover] = set()
