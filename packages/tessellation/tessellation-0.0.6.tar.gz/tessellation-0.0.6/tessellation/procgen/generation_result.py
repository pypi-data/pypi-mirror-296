"""Base class for tesselation generators."""

import json
from pathlib import Path
from typing import Optional, Any, Union

import numpy as np

from tessellation.procgen.tessellation_type import TessellationType


class GenerationResult:
    """Class representing the result of a tesselation generation."""

    def __init__(
        self,
        mask: np.ndarray,
        tessellation_type: TessellationType,
        metadata: Optional[dict] = None,
    ):
        self.mask = mask
        self.tessellation_type = tessellation_type
        self.metadata = metadata or {}

    def save_as_json(self, file_path: Union[Path, str]):
        """Save the generation result as a JSON file."""
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(self.to_json(), file, indent=2)

    def to_json(self) -> dict[str, Any]:
        """Return the generation result as a JSON serializable dictionary."""
        return {
            "mask": self.mask.tolist(),
            "tessellation_type": self.tessellation_type.value,
            "metadata": {**self.metadata},
        }

    @staticmethod
    def read_json(file_path: Union[Path, str]):
        """Read the generation result from a JSON file."""
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return GenerationResult(
            mask=np.array(data["mask"]),
            tessellation_type=TessellationType(data["tessellation_type"]),
            metadata=data["metadata"],
        )
