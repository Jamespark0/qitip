from dataclasses import dataclass, field
from typing import Optional

from numpy import array

from qitip.objects import Constraints, Inequality
from qitip.prover import Prover
from qitip.utils.converters import CoefficientsToDict, canonical_to_expression


@dataclass
class TypeResult:
    status: Optional[bool] = field(init=False, default=None)
    message: str = field(init=False, default="")


class ResultBuilder:
    def __init__(self, prover: Prover) -> None:
        self._prover: Prover = prover
        self.reset()

    @property
    def result(self) -> TypeResult:
        return self._result

    def reset(self) -> None:
        self._result: TypeResult = TypeResult()

    def process_type(self, inequality: Inequality, constraints: Constraints) -> None:
        self._result.status = self._prover._check_type(
            inequality.coefficients, constraints.coefficients
        )

        # Abbreviation for von-Neumann type
        vn_message: str = "It's von-Neumann type inequality.\n\nIt can be proved by summing up the following:\n"
        # Abbreviation for non-Provable type
        np_message: str = (
            "Not provable by Quantum ITIP:(\n\nOne can try to disprove by using:\n"
        )
        self._result.message += vn_message if self._result.status else np_message

    def process_used_inequality_constraints(
        self, inequality: Inequality, constraints: Constraints
    ):
        if self._result.status is None:
            raise NotImplementedError(
                f"Check type before calling {self.process_used_inequality_constraints.__qualname__}"
            )

        # Mapping from elemental inequalities to vector entries of used _inequalities
        inequality_entry: dict[tuple[int, ...], int] = {
            tuple(elemental): index
            for index, elemental in enumerate(self._prover.elemental)
        }

        constraints_entry: dict[tuple[float, ...], int] = {
            tuple(constraint): index
            for index, constraint in enumerate(constraints.coefficients)
        }

        # the inequality is von-Neumann type
        if self._result.status:
            used_inequalities, used_constraints = self._prover._shortest_proof(
                inequality=inequality.coefficients, constraints=constraints.coefficients
            )

            for elemental, coefficient in CoefficientsToDict.convert_vector(
                vector_entry=inequality_entry, coefficients=used_inequalities
            ).items():
                # Notice that the keys of the inequality_entries are "tuples" !!!!!
                self._result.message += f"{coefficient} * [{canonical_to_expression(CoefficientsToDict.convert_vector(vector_entry=inequality.vector_entry, coefficients=array(elemental)))}] >= 0\n"

            for constraint, coefficient in CoefficientsToDict.convert_vector(
                vector_entry=constraints_entry, coefficients=used_constraints
            ).items():
                # The negative 1 comes from the expression of duality
                self._result.message += f"{-1*coefficient} * [{canonical_to_expression(CoefficientsToDict.convert_vector(vector_entry=constraints.vector_entry, coefficients=array(constraint)))}] = 0\n"

        # not provable by quantum ITIP
        else:
            temp_used_inequalities, temp_used_constriants = (
                self._prover._shortest_counter_proof(
                    inequality=inequality.coefficients,
                    constraints=constraints.coefficients,
                )
            )

            used_inequalities = (temp_used_inequalities != 0).astype(int)
            used_constraints = (temp_used_constriants != 0).astype(int)

            for elemental, _ in CoefficientsToDict.convert_vector(
                vector_entry=inequality_entry, coefficients=used_inequalities
            ).items():
                self._result.message += f"{canonical_to_expression(CoefficientsToDict.convert_vector(vector_entry=inequality.vector_entry, coefficients=array(elemental)))} = 0\n"

            for constraint, _ in CoefficientsToDict.convert_vector(
                vector_entry=constraints_entry, coefficients=used_constraints
            ).items():
                self._result.message += f"{canonical_to_expression(CoefficientsToDict.convert_vector(vector_entry=constraints.vector_entry, coefficients=array(constraint)))} = 0"


def result_director(
    prover: Prover, inequality: Inequality, constraints: Optional[Constraints] = None
):
    if constraints is None:
        _constraints: Constraints = Constraints(vector_entry=inequality.vector_entry)
    else:
        _constraints = constraints

    builder: ResultBuilder = ResultBuilder(prover=prover)
    builder.process_type(inequality=inequality, constraints=_constraints)
    builder.process_used_inequality_constraints(
        inequality=inequality, constraints=_constraints
    )
    return builder.result
