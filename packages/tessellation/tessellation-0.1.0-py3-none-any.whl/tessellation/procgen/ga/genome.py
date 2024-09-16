"""Definitions for LEAP genome/phenome primitives for tessellation generation."""

import dataclasses

from leap_ec import Decoder

from tessellation.procgen import Action


@dataclasses.dataclass
class TessellationGenome:
    """Class that represents a tessellation genome."""

    actions: list[Action]
    start_point: tuple[int, int]

    def __eq__(self, other):
        return self.actions == other.actions and self.start_point == other.start_point


@dataclasses.dataclass
class TessellationPhenome:
    """Class that represents a tessellation phenome."""

    line_indices: list[tuple[int, int]]

    def __eq__(self, other):
        return self.line_indices == other.line_indices


class TessellationDecoder(Decoder):
    """Decoder for tessellation genomes."""

    def decode(
        self, genome: TessellationGenome, *args, **kwargs
    ) -> TessellationPhenome:
        """Decode a genome into a phenome."""
        cursor = {"y": genome.start_point[0], "x": genome.start_point[1]}
        line_indices = [(cursor["y"], cursor["x"])]
        for action in genome.actions:
            if action == Action.UP:
                cursor["y"] -= 1
            elif action == Action.UP_RIGHT:
                cursor["y"] -= 1
                cursor["x"] += 1
            elif action == Action.RIGHT:
                cursor["x"] += 1
            elif action == Action.DOWN:
                cursor["y"] += 1
            elif action == Action.DOWN_RIGHT:
                cursor["y"] += 1
                cursor["x"] += 1
            else:
                raise ValueError(f"Unsupported action: {action}")

            line_indices.append((cursor["y"], cursor["x"]))
        return TessellationPhenome(line_indices=line_indices)
