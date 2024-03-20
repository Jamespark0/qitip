from src.qitip.builders import ConstraintsBuilder, InequalityBuilder
from src.qitip.object_pools import ProverPool, SpacePool
from src.qitip.objects import EntropicSpace
from src.qitip.prover import Prover


class Qitip:
    _space_pool: SpacePool = SpacePool()
    _prover_pool: ProverPool = ProverPool()

    def __init__(self, n: int):
        self._space: EntropicSpace = self._space_pool.get(n)
        self._prover: Prover = self._prover_pool.get(space=self._space)
        self.inequality: InequalityBuilder = InequalityBuilder(
            vector_entry=self._space.vector_entry
        )
        self.constraints: ConstraintsBuilder = ConstraintsBuilder(
            vector_entry=self._space.vector_entry
        )

    @property
    def vector_entry(self):
        return self._space.vector_entry

    @property
    def space(self):
        return self._space

    @property
    def prover(self):
        return self._prover


def init(n: int) -> Qitip:
    return Qitip(n=n)


if __name__ == "__main__":
    while True:
        try:
            n: int = int(input("Input the number of quantum systems: "))
            if n >= 2:
                break
            else:
                print("Number of quantum systems has to be greater than 2 ...")
        except ValueError:
            print("Input value should be an integer greater than 1!")
        except Exception:
            raise Exception("Unexpected errors occur ...")

    init(n)
