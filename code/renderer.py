import pygame
import numpy as np

from math3d import project_point, transform_points
from bsp import Triangle

class SolidRenderer:
    def __init__(self, width: int, height: int, near_plane: float = 0.1):
        self.width = width
        self.height = height
        self.near_plane = near_plane

    def draw(
        self,
        surface: pygame.Surface,
        triangles: list[Triangle],
        view_matrix: np.ndarray,
        focal_length: float,
    ) -> None:
        
        for tri in triangles:
            # Transform vertices to camera space
            # We stack vertices into (3, 3) matrix
            verts = np.vstack(tri.vertices)
            cam_verts = transform_points(view_matrix, verts)
            
            # Simple near plane culling: if any vertex is behind near plane, don't draw
            # A full clipping against the near plane could be written, but for now we cull.
            if any(v[2] <= self.near_plane for v in cam_verts):
                continue
                
            projected = [
                project_point(p, focal_length, self.width, self.height)
                for p in cam_verts
            ]

            pygame.draw.polygon(surface, tri.color, projected)


