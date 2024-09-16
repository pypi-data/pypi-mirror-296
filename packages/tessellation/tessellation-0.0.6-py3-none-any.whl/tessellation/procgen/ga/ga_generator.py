"""Genetic Algorithm based tessellation generator."""

from typing import Callable, Optional

import numpy as np
from leap_ec import Representation, ops, probe, Individual
from leap_ec.algorithm import generational_ea

from tessellation.procgen import Generator, GenerationResult, Action, TessellationType
from tessellation.procgen.ga.genome import TessellationPhenome, TessellationDecoder
from tessellation.procgen.ga.problem import TessellationProblem, initialize_genome


class GATessellationGenerator(Generator):
    """Genetic Algorithm based tessellation generator."""

    def __init__(
        self,
        heuristic_fns: list[Callable[[TessellationPhenome], float]],
        mutation_fns: list[Callable[[Action, ...], list[Action]]],
        heuristic_fn_weights: Optional[list[float]] = None,
        side_len: int = 100,
        max_generations: int = 100,
        population_size: int = 100,
    ):
        self.side_len = side_len
        self.problem = TessellationProblem(
            heuristic_fns=heuristic_fns,
            fn_weights=heuristic_fn_weights,
            side_len=self.side_len,
        )
        self.representation = Representation(
            decoder=TessellationDecoder(),
            initialize=lambda: initialize_genome(self.problem),
        )
        self.mutation_fns = mutation_fns

        self.max_generations = max_generations
        self.population_size = population_size

        self.population = None

    def generate(self, individual_idx: int = 0) -> GenerationResult:
        """Generate a new tesselation."""
        if self.population is None:
            self.evolve()

        return self.get_generation_result(self.population[individual_idx])

    def evolve(self) -> list[GenerationResult]:
        """Run genetic algorithm and evolve the population."""
        self.population = generational_ea(
            max_generations=self.max_generations,
            pop_size=self.population_size,
            problem=self.problem,
            representation=self.representation,
            # The operator pipeline
            pipeline=[
                ops.tournament_selection,  # Select parents via tournament
                ops.clone,  # Copy them (just to be safe)
                *self.mutation_fns,  # Apply mutation functions
                # Crossover w/ 40% chance of swapping gen
                # ops.UniformCrossover(p_swap=0.4), es
                ops.evaluate,  # Evaluate fitness
                # pylint: disable=no-value-for-parameter
                ops.pool(size=self.population_size),  # Collect offspring into new pop
                probe.BestSoFarProbe(),  # Print best so far
            ],
        )
        return [
            self.get_generation_result(individual) for individual in self.population
        ]

    def get_generation_result(
        self, individual: Individual
    ) -> Optional[GenerationResult]:
        """Return the generation result for the individual."""
        genome = individual.genome
        mask = np.zeros((self.side_len, self.side_len), dtype=int)
        try:
            mask = Generator._draw_line(mask, genome.start_point, genome.actions)
            mask_t = Generator._draw_line(mask.T, genome.start_point, genome.actions)
            final_mask = mask | mask_t

            return GenerationResult(
                final_mask,
                TessellationType.SQUARE_TRANSLATION,
                metadata={
                    "generator_class": "GATessellationGenerator",
                    "fitness": individual.fitness,
                },
            )
        except IndexError:
            print(f"Invalid individual: {individual}, returning None")
            return None
