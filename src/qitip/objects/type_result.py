from dataclasses import dataclass
from typing import Optional

from numpy.typing import NDArray


class ResultBuilder:
    def __init__(self) -> None:
        self.message: str = ""
        self.status: Optional[bool] = None

    def check_type(self, status: bool):
        self.status = status

        # Abbreviation for von-Neumann type
        vn_message: str = "It's von-Neumann type inequality.\nIt can be proved by:\n"
        # Abbreviation for non-Provable type
        np_message: str = (
            "Not provable by Quantum ITIP:(\nOne can try to disprove by using:\n"
        )
        self.message += vn_message if status else np_message


@dataclass
class TypeResult:
    status: bool
    inequality_entry: tuple[NDArray, ...] | tuple[()] | None
    constraint_entry: tuple[NDArray, ...] | tuple[()] | None
    used_inequalities: NDArray
    used_constraints: NDArray | None
    messages: tuple[str, ...]
