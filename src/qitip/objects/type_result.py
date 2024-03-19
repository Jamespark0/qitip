from dataclasses import dataclass

from numpy.typing import NDArray


@dataclass(kw_only=True)
class TypeResult:
    status: bool
    inequality_entry: tuple[NDArray, ...] | tuple[()] | None
    constraint_entry: tuple[NDArray, ...] | tuple[()] | None
    used_inequalities: NDArray
    used_constraints: NDArray | None
    messages: tuple[str, ...]
