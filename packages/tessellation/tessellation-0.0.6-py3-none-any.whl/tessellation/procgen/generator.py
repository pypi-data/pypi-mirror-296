"""Base class for tesselation generators."""

from abc import ABC

import numpy as np

from tessellation.procgen.action import Action
from tessellation.procgen.generation_result import GenerationResult


class Generator(ABC):
    """Base class for tesselation generators."""

    def generate(self) -> GenerationResult:
        """Generate a new tesselation."""
        raise NotImplementedError

    @staticmethod
    def _draw_line(
        mask: np.ndarray,
        start_point: tuple[int, int],  # (y, x)
        action_list: list[Action],
    ) -> np.ndarray:
        """Draw a line on the mask."""
        cursor = {"x": start_point[1], "y": start_point[0]}
        mask[cursor["y"], cursor["x"]] = 1
        for action in action_list:
            if action in [Action.UP_RIGHT, Action.UP]:
                cursor["y"] -= 1
            if action in [Action.DOWN_RIGHT, Action.DOWN]:
                cursor["y"] += 1
            if action in [Action.UP_RIGHT, Action.DOWN_RIGHT, Action.RIGHT]:
                cursor["x"] += 1

            if cursor["y"] >= 0:
                mask[0 : cursor["y"] + 1, cursor["x"]] = 1
            else:
                mask[cursor["y"] :, cursor["x"]] = 1

        return mask
