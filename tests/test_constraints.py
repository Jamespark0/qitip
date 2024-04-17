from qitip.objects import Constraints

vector_entry: dict[frozenset[int], int] = {
    frozenset((1,)): 0,
    frozenset((2,)): 1,
    frozenset((1, 2)): 2,
}


def test_empty_constraint_initialization():
    empty_constraint = Constraints(vector_entry=vector_entry)
    assert empty_constraint.coefficients.shape == (0, len(vector_entry))


def test_single_constraint_initialization_with_vector():
    single_constraint = Constraints(vector_entry, (1, 0, 0))
    assert single_constraint.coefficients.shape == (1, len(vector_entry))


def test_single_constraint_initialization_with_matrix():
    single_constraint = Constraints(vector_entry, ((1, 0, 0),))
    assert single_constraint.coefficients.shape == (1, len(vector_entry))


def test_multiple_constraints_initialization():
    num_constraints: int = 2
    c = [
        [(i + len(vector_entry) * _) for i in range(len(vector_entry))]
        for _ in range(num_constraints)
    ]
    multi_constraints = Constraints(vector_entry, c)
    assert multi_constraints.coefficients.shape == (num_constraints, len(vector_entry))
