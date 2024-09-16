"""Drawing module."""

from pathlib import Path
from typing import Union

import matplotlib.pyplot as plt
import numpy as np

from tessellation.procgen import GenerationResult


class Drawer:
    """Drawer class."""

    def __init__(self, cmap: str = "binary"):
        self.cmap = cmap

    def draw(self, tessellation: np.ndarray):
        """Draw the tessellation."""
        plt.imshow(tessellation, cmap=plt.get_cmap(self.cmap))

    def save_as_png(self, file_path: Union[Path, str], tessellation: np.ndarray):
        """Save the drawing as a PNG file."""
        plt.imsave(file_path, tessellation, cmap=plt.get_cmap(self.cmap))

    @staticmethod
    def tessellate(
        generation_result: GenerationResult, n_shapes: int = 5
    ) -> np.ndarray:
        """Tessellate the mask n_shapes times."""
        mask = generation_result.mask
        side_len = mask.shape[0]
        side_len_full_image = side_len * n_shapes
        tessellation = np.zeros((side_len_full_image, side_len_full_image), dtype=int)

        row_starting_color = 1
        for i in range(n_shapes):
            cell_color = row_starting_color
            for j in range(n_shapes):
                y_start = i * side_len
                y_end = y_start + side_len

                x_start = j * side_len
                x_end = x_start + side_len

                if cell_color == 0:
                    color_mask = np.logical_not(mask)
                    cell_color = 1
                else:
                    color_mask = mask
                    cell_color = 0

                tessellation[y_start:y_end, x_start:x_end] = color_mask

            row_starting_color = 1 if row_starting_color == 0 else 0

        return tessellation
