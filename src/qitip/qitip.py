from itertools import compress
from typing import Iterable

from numpy import dtype, int8, ndarray

from src.qitip.builders import ConstraintsBuilder, InequalityBuilder
from src.qitip.object_pools import ProverPool, SpacePool
from src.qitip.objects import Constraints, EntropicSpace, Inequality
from src.qitip.prover import Prover
from src.qitip.typings import InfoType


class from_coefficients_to_dict:
    # This function takes an object (can either be Inequality or Constraints) to
    # 1D arraylike or 2D arraylike
    @staticmethod
    def convert_inequality(obj: Inequality) -> dict[Iterable[int] | int, float]:
        non_zeros: ndarray[ndarray[bool, dtype[int8]], dtype[int8]] = (
            obj.coefficients != 0
        )

        # Ensures the sys is in the same order as the vectors
        sys_in_order: tuple[tuple[int, ...], ...] = tuple(
            tuple(k)
            for k, _ in sorted(obj.vector_entry.items(), key=lambda item: item[1])
        )

        # since each Inequality only contains one inequality
        return dict(
            zip(
                compress(sys_in_order, non_zeros[0]),
                compress(obj.coefficients[0], non_zeros[0]),
            )
        )

    @staticmethod
    def convert_constraints(obj: Constraints) -> list[dict[Iterable[int] | int, float]]:
        non_zeros: ndarray[ndarray[bool, dtype[int8]], dtype[int8]] = (
            obj.coefficients != 0
        )

        # Ensures the sys is in the same order as the vectors
        sys_in_order: tuple[tuple[int, ...], ...] = tuple(
            tuple(k)
            for k, _ in sorted(obj.vector_entry.items(), key=lambda item: item[1])
        )

        return [
            dict(
                zip(
                    compress(sys_in_order, non_zero),
                    compress(obj.coefficients[index], non_zero),
                )
            )
            for index, non_zero in enumerate(non_zeros)
        ]


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

    def embed(self, obj: InfoType) -> InfoType:
        """_summary_
        Embed the existing InfoType (can be either Inequality or Constraints) in
        higher dimensinoal space

        Args:
            obj (InfoType): Inequality or Constraints type

        Returns:
            InfoType: Type has to agree with that of the obj type
        """
        if not isinstance(obj, Inequality | Constraints):
            raise TypeError("Only Inequality and Constraints can be embedded ...")

        if len(obj.vector_entry) > len(self._space.vector_entry):
            raise ValueError("Can only embed an object to higher dimensions!")

        elif len(obj.vector_entry) == len(self._space.vector_entry):
            return obj

        # If the dim(obj) < dim(Qitip), actual embedding
        elif isinstance(obj, Inequality):
            return self.inequality.from_coefficients(
                from_coefficients_to_dict.convert_inequality(obj)
            )

        else:
            return self.constraints.from_coefficients(
                from_coefficients_to_dict.convert_constraints(obj)
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
