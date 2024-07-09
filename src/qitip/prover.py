import numpy as np
from scipy.optimize import OptimizeResult, linprog

from qitip.objects import EntropicSpace

# Prover is created with Quantum Elemental Inequalities
# In principle, it can also be created with classical elemental inequalities
from qitip.quantum_inequalities import QuantumElementalInequalities


class Prover:
    def __init__(self, space: EntropicSpace):
        self.n: int = max(max(space.vector_entry))
        self.elemental = QuantumElementalInequalities(
            space.vector_entry
        ).get_elementals()

        # This is only used for method isVonNeumannType
        self._vector_entry = space.vector_entry

    def __hash__(self) -> int:
        return hash((self.n))

    def _check_type(
        self,
        inequality: np.ndarray[
            np.ndarray[float, np.dtype[np.float64]], np.dtype[np.float64]
        ],
        constraints: np.ndarray[
            np.ndarray[np.float64, np.dtype[np.float64]], np.dtype[np.float64]
        ],
    ) -> bool:
        """_summary_
        In classical ITIP, checking if an inequality is Shannon-type can be proved with linear programming.

        In quantum information, a similar approach is applied.

        In summary, if the maximum value of the dual problem is 0, the inequality is von-Neumann type;
        otherwise, it is not provable by quantum ITIP.

        Args:
            inequality (np.ndarray[ np.ndarray[float, np.dtype[np.float64]], np.dtype[np.float64] ]):
            constraints (np.ndarray[ np.ndarray[np.float64, np.dtype[np.float64]], np.dtype[np.float64] ]):

        Raises:
            ValueError: when scipy successfully get the optimal value which fails to be 0. Inconsistent with the
            theory

        Returns:
            bool: if the inequality under the constraints is von-Neumann type, it returns True; otherwise, it returns False.
        """
        max_value: int = 0

        result: OptimizeResult = linprog(
            c=-np.zeros(self.elemental.shape[0] + constraints.shape[0]),
            A_eq=np.vstack((self.elemental, -constraints)).transpose(),
            b_eq=inequality,
            bounds=tuple(
                [(0, None)] * self.elemental.shape[0]
                + [(None, None)] * constraints.shape[0]
            ),
        )
        if not result.success or (result.success and (result.fun == max_value)):
            return result.success
        else:
            raise ValueError(
                f"Unexpected error has occurred. Expected optimal value is {max_value}, but get {result.fun} instead."
            )

    def _shortest_proof(
        self,
        inequality: np.ndarray[
            np.ndarray[np.float64, np.dtype[np.float64]], np.dtype[np.float64]
        ],
        constraints: np.ndarray[
            np.ndarray[np.float64, np.dtype[np.float64]], np.dtype[np.float64]
        ],
    ) -> tuple[
        np.ndarray[np.float64, np.dtype[np.float64]],
        np.ndarray[np.float64, np.dtype[np.float64]],
    ]:
        # The vectors are in the order of [y, mu, t] where
        # |y|_{0} = num of elemental inequalities
        # |mu|_{0} = |t|_{0} = num of constraints
        # Also -t <= mu <= t is the constraint

        num_elementals: int = self.elemental.shape[0]
        num_constraints: int = constraints.shape[0]
        dim: int = len(self._vector_entry)

        # Inequality constraints: -t <= mu <= t
        # Scipy: [A_ub][x] <= [b_ub]
        ## First, -t <= mu
        l_ineq = np.concatenate(
            (
                np.zeros((num_constraints, num_elementals)),
                -np.identity(num_constraints),
                -np.identity(num_constraints),
            ),
            axis=1,
        )
        ## Next, mu <= t
        r_ineq: np.ndarray[
            np.ndarray[np.int64, np.dtype[np.int64]], np.dtype[np.int64]
        ] = np.concatenate(
            (
                np.zeros((num_constraints, num_elementals)),
                np.identity(num_constraints),
                -np.identity(num_constraints),
            ),
            axis=1,
        )

        result = linprog(
            c=np.array(
                [1] * num_elementals + [0] * num_constraints + [1] * num_constraints
            ),
            A_ub=np.concatenate((l_ineq, r_ineq), axis=0),
            b_ub=np.zeros(2 * num_constraints),
            A_eq=np.concatenate(
                (
                    self.elemental,
                    -constraints,
                    np.zeros((num_constraints, dim)),
                ),
                axis=0,
            ).transpose(),
            b_eq=inequality,
            bounds=tuple(
                [(0, None)] * num_elementals
                + [(None, None)] * num_constraints
                + [(0, None)] * num_constraints
            ),
        )

        if not result.success:
            raise ValueError("Solution to shortest proof is not found ... ")

        return (
            result.x[:num_elementals],
            result.x[num_elementals : num_elementals + num_constraints],
        )

    # In theory, the maximal value of the dual problem cannot be found
    # We have to restrict our search in a bounded region.
    # Different from the classical information theory, marginal entropies are bounded by
    # H(all random variable)
    def _counter_proof_gamma(
        self,
        inequality: np.ndarray[
            np.ndarray[np.float64, np.dtype[np.float64]], np.dtype[np.float64]
        ],
        constraints: np.ndarray[
            np.ndarray[np.float64, np.dtype[np.float64]], np.dtype[np.float64]
        ],
    ) -> np.ndarray[np.float64, np.dtype[np.float64]]:
        # In quantum information theory, the closest counterpart is that a S(I) <= sum_{i in I}S({i})
        # Hence, I require, S({i}) <= 1 where i in {1,2,3,...,n}

        # The vector we will be working with is in the order of [y, mu, gamma]
        result: OptimizeResult = linprog(
            c=np.array(
                [0] * (self.elemental.shape[0] + constraints.shape[0]) + [1] * self.n
            ),
            A_eq=np.concatenate(
                (
                    self.elemental,
                    -constraints,
                    -np.eye(N=self.n, M=self.elemental.shape[1]),
                ),
                axis=0,
            ).transpose(),
            b_eq=inequality,
            bounds=tuple(
                [(0, None)] * self.elemental.shape[0]
                + [(None, None)] * constraints.shape[0]
                + [(0, None)] * self.n
            ),
            method="interior-point",  # This yields more desiring result than the default,  HiGHS
        )

        if result.status is False:
            raise ValueError(
                "Expect optimal value of dual problem under the bounded marginal entropies to be found ..."
            )

        return result.x[-self.n :]

    def _shortest_counter_proof(
        self,
        inequality: np.ndarray[
            np.ndarray[np.float64, np.dtype[np.float64]], np.dtype[np.float64]
        ],
        constraints: np.ndarray[
            np.ndarray[np.float64, np.dtype[np.float64]], np.dtype[np.float64]
        ],
    ) -> tuple[
        np.ndarray[np.float64, np.dtype[np.float64]],
        np.ndarray[np.float64, np.dtype[np.float64]],
    ]:
        # This is quite complicated, for more information, checkout my master's thesis about
        # the theory of quantum ITIP
        gamma: np.ndarray[np.float64, np.dtype[np.float64]] = self._counter_proof_gamma(
            inequality=inequality, constraints=constraints
        )

        return self._shortest_proof(
            inequality=inequality
            + np.matmul(gamma, np.eye(N=self.n, M=self.elemental.shape[1])),
            constraints=constraints,
        )


class ProverPool:
    def __init__(self) -> None:
        self._created: set[Prover] = set()

    def get(self, space: EntropicSpace):
        for p in self._created:
            if p.n == space.n:
                return p

        new_prover = Prover(space=space)
        self._created.add(new_prover)
        return new_prover
