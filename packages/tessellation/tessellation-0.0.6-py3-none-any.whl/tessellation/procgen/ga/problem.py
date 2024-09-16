"""Class that defines a LEAP problem for tessellation generation."""

from typing import Optional, Callable

import numpy as np
from leap_ec.problem import Problem

from tessellation.procgen import Action
from tessellation.procgen.ga.genome import TessellationPhenome, TessellationGenome


class TessellationProblem(Problem):
    """Class that defines a LEAP problem for tessellation generation."""

    def __init__(
        self,
        heuristic_fns: list[Callable[[TessellationPhenome], float]],
        fn_weights: Optional[list[float]] = None,
        side_len: int = 100,
    ):
        super().__init__()
        self.heuristic_fns = heuristic_fns

        if fn_weights is None:
            self.fn_weights = np.ones(len(self.heuristic_fns))
        else:
            if len(fn_weights) != len(self.heuristic_fns):
                raise ValueError(
                    "fn_weights must be exact same length as heuristic_fns if provided"
                )
            self.fn_weights = np.array(fn_weights)

        self.side_len = side_len

    def evaluate(self, phenome: TessellationPhenome, *args, **kwargs) -> np.array:
        """Evaluate the phenome using the heuristic functions."""
        heuristic_vals = [fn(phenome) for fn in self.heuristic_fns]
        return np.sum(self.fn_weights * heuristic_vals)

    def equivalent(self, first_fitness: float, second_fitness: float) -> bool:
        """Return True if the two fitness values are equivalent."""
        return first_fitness == second_fitness

    def worse_than(self, first_fitness: float, second_fitness: float) -> bool:
        """Return True if the first fitness value is worse than the second."""
        return first_fitness < second_fitness


def initialize_genome(problem: TessellationProblem):
    """Initialize a genome for the tessellation problem."""
    actions = [Action.RIGHT for _ in range(problem.side_len)]
    return TessellationGenome(actions=actions, start_point=(0, 0))
