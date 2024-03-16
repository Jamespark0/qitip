from src.qitip.objects.entropic_space import EntropicSpace
from src.qitip.prover import Prover


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

    def get(self, space: EntropicSpace):
        for p in self.created:
            if p.n == space.n:
                return p

        new_prover = Prover(space=space)
        self.created.add(new_prover)
        return new_prover
