import numpy as np
from scipy.optimize import OptimizeResult, linprog

from src.qitip.objects.entropic_space import EntropicSpace

# Prover is created with Quantum Elemental Inequalities
# In principle, it can also be created with classical elemental inequalities
from src.qitip.quantum_inequalities import QuantumElementalInequalities


class Prover:
    def __init__(self, space: EntropicSpace):
        self.n: int = max(max(space.vector_entry))
        self.elemental = QuantumElementalInequalities(
            space.vector_entry
        ).get_elementals()

    def __hash__(self) -> int:
        return hash((self.n))

    def calculate(
        self, inequality: np.ndarray, constraints: np.ndarray
    ) -> OptimizeResult:
        # Negative sign in 'c' arises from the fact that scipy.linprog calculates minimal value
        return linprog(
            c=-np.zeros(self.elemental.shape[0] + constraints.shape[0]),
            A_eq=np.vstack((self.elemental, -constraints)).transpose(),
            b_eq=inequality,
            bounds=tuple(
                [(0, None)] * self.elemental.shape[0]
                + [(None, None)] * constraints.shape[0]
            ),
        )

    def check_type(self, result: OptimizeResult) -> bool:
        max_value: int = 0
        return (result.success) and (result.fun == max_value)

    def shortest_proof_generator(
        self, inequality: np.ndarray, constraints: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray] | tuple[None, None]:
        """
        This method is called only when the given inequality is von-Neumann-type/Shannon-type

        Following from the paper, "Proving and Disproving Information Inequalities"
        """
        # For -z <= mu <= z
        A_ub = np.zeros(
            (
                # self.elemental.shape[0] + 2 * constraints.shape[0],
                2 * constraints.shape[0],
                self.elemental.shape[0] + 2 * constraints.shape[0],
            )
        )
        # Ensure -z <= mu <= z
        for row in range(constraints.shape[0]):
            A_ub[row][row + self.elemental.shape[0]] = 1
            A_ub[row][row + self.elemental.shape[0] + constraints.shape[0]] = -1
        for row in range(
            constraints.shape[0],
            2 * constraints.shape[0],
        ):
            A_ub[row][row] = -1
            A_ub[row][row - constraints.shape[0]] = -1

        result = linprog(
            c=np.array(
                [
                    *[1] * self.elemental.shape[0],
                    *[0] * constraints.shape[0],
                    *[1] * constraints.shape[0],
                ]
            ),
            A_eq=np.vstack(
                (
                    (np.vstack((self.elemental, -constraints))),
                    np.zeros((constraints.shape[0], constraints.shape[1])),
                )
            ).transpose(),
            b_eq=inequality,
            bounds=tuple(
                [(0, None)] * len(self.elemental)
                + [(None, None)] * (constraints.shape[0])
                + [(0, None)] * (constraints.shape[0])
            ),
            b_ub=np.zeros(2 * constraints.shape[0]),
            A_ub=A_ub,
        )
        return (
            (
                result.x[: self.elemental.shape[0]],
                result.x[
                    self.elemental.shape[0] : self.elemental.shape[0]
                    + constraints.shape[0]
                ],
            )
            if result.success
            else (None, None)
        )

    # Different from classical information theory
    # due to conditional entropy can be negative in the quantum case
    def disprove_dual_gamma(
        self, n: int, inequality: np.ndarray, constraints: np.ndarray
    ) -> np.ndarray:
        # Recall that quantum conditional entropy can be negative -> S(universal) is not the maximum entropy
        # The minimum value should be positive, as linprog finds minimum value
        result = linprog(
            c=np.array(
                [0] * (self.elemental.shape[0] + constraints.shape[0]) + [1] * n
            ),
            A_eq=np.vstack(
                (
                    np.vstack((self.elemental, -constraints)),
                    -1 * np.eye(N=n, M=inequality.shape[1], dtype=np.int64),
                )
            ).transpose(),
            b_eq=inequality,
            bounds=tuple(
                [(0, None)] * self.elemental.shape[0]
                + [(None, None)] * constraints.shape[0]
                + [(0, None)] * n
            ),
            method="interior-point",
            options={"disp": False},
        )

        if result.success is False:
            raise ValueError("Unable to find the optimal solution!")

        # print(f"Success: {result.success}")
        # print(
        #     f"The minimum value for non-von-Neumann type, {-1 * result.fun if result.success else None}, should be negative"
        # )

        return result.x[-n:]

    def disprove_primal_gamma(self, inequality: np.ndarray, constraints: np.ndarray):
        result = linprog(
            c=inequality[0],
            A_ub=-self.elemental,
            b_ub=np.zeros(self.elemental.shape[0]),
            A_eq=constraints,
            b_eq=np.zeros(constraints.shape[0]),
            bounds=tuple([(0, 10)] * inequality.shape[1]),
            method="highs",
        )

        if result.x is None:
            raise ValueError("No optimal solution!")

        print(f"Success: {result.success}")
        print(
            f"The minimum value for non-von-Neumann type, {result.fun if result.success else None}, should be negative"
        )
        print(result.ineqlin.marginals)

        return -result.fun if result.success else np.inf

    def shortest_disprove_generator(
        self, n: int, inequality: np.ndarray, constraints: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray] | tuple[None, None]:
        gamma: np.ndarray = self.disprove_dual_gamma(
            n=n, inequality=inequality, constraints=constraints
        )

        return self.shortest_proof_generator(
            inequality=inequality
            + np.matmul(gamma, np.eye(N=n, M=inequality.shape[1])),
            constraints=constraints,
        )

    def _universal_set_basis_vector(self, dim: int) -> np.ndarray:
        basis = np.zeros(dim)
        basis[-1] = 1
        return basis
