import math
from dataclasses import dataclass
import numpy as np

from math3d import rotation_x, rotation_y, rotation_z, translation_matrix


@dataclass
class Camera:
    position: np.ndarray
    pitch: float
    yaw: float
    roll: float

    def view_matrix(self) -> np.ndarray:
        translate_inv = translation_matrix(-self.position[0], -self.position[1], -self.position[2])

        # View matrix is the inverse of camera world transform.
        rot_inv = rotation_z(-self.roll) @ rotation_x(-self.pitch) @ rotation_y(-self.yaw)
        return rot_inv @ translate_inv

    def forward(self) -> np.ndarray:
        cp = math.cos(self.pitch)
        sp = math.sin(self.pitch)
        cy = math.cos(self.yaw)
        sy = math.sin(self.yaw)
        vec = np.array([sy * cp, -sp, cy * cp], dtype=float)
        return vec / np.linalg.norm(vec)

    def right(self) -> np.ndarray:
        cy = math.cos(self.yaw)
        sy = math.sin(self.yaw)
        vec = np.array([cy, 0.0, -sy], dtype=float)
        return vec / np.linalg.norm(vec)

    def up(self) -> np.ndarray:
        f = self.forward()
        r = self.right()
        u = np.cross(r, f)
        return u / np.linalg.norm(u)
