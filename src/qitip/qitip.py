from typing import Optional

from src.qitip.builders import ConstraintsBuilder, InequalityBuilder
from src.qitip.object_pools import ProverPool, SpacePool
from src.qitip.objects import Constraints, EntropicSpace, Inequality, TypeResult
from src.qitip.objects.type_result import result_director
from src.qitip.prover import Prover
from src.qitip.typings import InfoType
from src.qitip.utils.converters import CoefficientsToDict


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
                CoefficientsToDict.convert_vector(obj.vector_entry, obj.coefficients)
            )

        else:
            return self.constraints.from_coefficients(
                CoefficientsToDict.convert_matrix(obj.vector_entry, obj.coefficients)
            )

    def is_vn_type(
        self, inequality: Inequality, constraints: Optional[Constraints] = None
    ) -> TypeResult:
        return result_director(
            prover=self._prover, inequality=inequality, constraints=constraints
        )

    @property
    def vector_entry(self):
        return self._space.vector_entry

    @property
    def space(self):
        return self._space
