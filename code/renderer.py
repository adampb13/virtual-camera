import pygame
import numpy as np

from math3d import project_point


class WireframeRenderer:
    def __init__(self, width: int, height: int, near_plane: float = 0.1):
        self.width = width
        self.height = height
        self.near_plane = near_plane

    def draw(
        self,
        surface: pygame.Surface,
        camera_space_vertices: np.ndarray,
        edges: list[tuple[int, int]],
        focal_length: float,
        color: tuple[int, int, int],
    ) -> None:
        projected: dict[int, tuple[int, int]] = {}

        for i, p in enumerate(camera_space_vertices):
            if p[2] <= self.near_plane:
                continue
            projected[i] = project_point(p, focal_length, self.width, self.height)

        for i0, i1 in edges:
            p0 = camera_space_vertices[i0]
            p1 = camera_space_vertices[i1]

            if p0[2] <= self.near_plane or p1[2] <= self.near_plane:
                continue

            if i0 not in projected or i1 not in projected:
                continue

            pygame.draw.line(surface, color, projected[i0], projected[i1], 1)
