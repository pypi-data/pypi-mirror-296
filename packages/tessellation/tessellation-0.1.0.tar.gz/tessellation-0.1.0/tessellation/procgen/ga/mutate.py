"""Methods for evolving tessellation genomes."""

from typing import Optional, Iterator, Callable

import numpy as np
from leap_ec import Individual

from tessellation.procgen import Action, ALL_ACTIONS
from tessellation.procgen.ga.genome import TessellationGenome

rng = np.random.default_rng(42)


def apply_mutation(
    mutation_fn: Callable[[Action, ...], list[Action]],
    individual_iterator: Iterator,
    fn_kwargs: Optional[dict] = None,
) -> Individual:
    """Apply mutation to each individual."""
    if fn_kwargs is None:
        fn_kwargs = {}

    while True:
        individual = next(individual_iterator)
        genome = individual.genome
        new_action_list: list[Action] = []
        for action in genome.actions:
            new_actions = mutation_fn(action, **fn_kwargs)
            new_action_list.extend(new_actions)

        individual.fitness = None  # invalidate fitness since we have new genome

        individual.genome = TessellationGenome(
            actions=new_action_list, start_point=genome.start_point
        )

        yield individual


def substitute_action(
    existing_action: Action,
    substitution_prob: float = 0.1,
    action_probs: Optional[list[float]] = None,
) -> list[Action]:
    """Substitute existing action with random action with substitution_prob."""
    if action_probs is None:
        action_probs = np.ones(len(Action)) / len(Action)

    if rng.random() < substitution_prob:
        return [rng.choice(np.array(ALL_ACTIONS), p=action_probs)]
    return [existing_action]


def insert_action(
    existing_action: Action,
    insertion_prob: float = 0.1,
    action_probs: Optional[list[float]] = None,
) -> list[Action]:
    """Insert random action with insertion_prob probability."""
    if action_probs is None:
        action_probs = np.ones(len(Action)) / len(Action)

    if rng.random() < insertion_prob:
        new_action = rng.choice(np.array(ALL_ACTIONS), p=action_probs)
        if rng.random() < 0.5:
            return [existing_action, new_action]
        return [new_action, existing_action]
    return [existing_action]


def delete_action(existing_action: Action, deletion_prob: float = 0.1) -> list[Action]:
    """Delete existing action with deletion_prob probability."""
    if rng.random() < deletion_prob:
        return []
    return [existing_action]
