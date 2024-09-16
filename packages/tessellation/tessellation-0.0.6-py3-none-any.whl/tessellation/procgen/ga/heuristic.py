"""Heuristic functions for evaluating tessellation genomes."""

from tessellation.procgen.ga.genome import TessellationPhenome


### Penalties - return negative scores ###

DISQUALIFICATION_FITNESS = -100_000


def bottom_top_not_even_penalty(
    phenome: TessellationPhenome, max_diff_before_penalty: int
) -> float:
    """Check that the bottom and top sides have a relatively even number of points."""
    n_top_points = 0
    n_bottom_points = 0
    for idx in phenome.line_indices:
        y_idx = idx[0]
        if y_idx >= 0:
            n_top_points += 1
        else:
            n_bottom_points += 1
    n_points_diff = abs(n_top_points - n_bottom_points)
    if n_points_diff <= max_diff_before_penalty:
        return 0

    points_over_threshold = n_points_diff - max_diff_before_penalty
    return -1 * points_over_threshold


def duplicated_points_penalty(phenome: TessellationPhenome) -> float:
    """Returns negative heuristic value for duplicated points."""
    n_line_indices = len(phenome.line_indices)
    n_unique_line_indices = len(set(phenome.line_indices))
    return n_unique_line_indices - n_line_indices


def out_of_bounds_penalty(phenome: TessellationPhenome, side_len: int) -> float:
    """Check that the tessellation line does not go out of bounds."""
    max_x, max_y = side_len - 1, side_len - 1
    min_x, min_y = 0, -1 * side_len
    in_bounds = all(
        min_x <= x <= max_x and min_y <= y <= max_y for (y, x) in phenome.line_indices
    )
    if in_bounds:
        return 0
    return DISQUALIFICATION_FITNESS


def stray_pixels_penalty(phenome: TessellationPhenome) -> float:
    """Penalty for stray pixels in the tessellation line."""
    # Implement fitness function to check for stray pixels
    raise NotImplementedError()


def jagged_edges_penalty(phenome: TessellationPhenome) -> float:
    """Penalty for jagged edges in the tessellation line."""
    # Implement fitness function to check for jagged edges
    raise NotImplementedError()


### Rewards - return positive scores ###


def count_number_points_reward(phenome: TessellationPhenome) -> float:
    """Count the number of points in the tessellation line."""
    return len(phenome.line_indices)


def bottom_top_even_reward(
    phenome: TessellationPhenome, max_diff_before_reward: int
) -> float:
    """Check that the bottom and top sides have a relatively even number of points."""
    n_top_points = 0
    n_bottom_points = 0
    for idx in phenome.line_indices:
        y_idx = idx[0]
        if y_idx >= 0:
            n_top_points += 1
        else:
            n_bottom_points += 1

    n_points_diff = abs(n_top_points - n_bottom_points)
    if n_points_diff >= max_diff_before_reward:
        return 0

    return max_diff_before_reward - n_points_diff


def reaches_corner_to_corner_reward(phenome: TessellationPhenome) -> float:
    """Reward for tessellation line that reaches from corner to corner of mask."""
    # Implement fitness function to check that the line is connected
    raise NotImplementedError()
