from dataclasses import dataclass


@dataclass
class TypeResult:
    status: bool
    vector_entry: dict[frozenset[int], int]
    used_inequalities: tuple[tuple[float]]
    used_constraints: tuple[tuple[float]] | None
    messages: tuple[str]
