import math
import numpy as np


def translation_matrix(tx: float, ty: float, tz: float) -> np.ndarray:
    return np.array(
        [
            [1.0, 0.0, 0.0, tx],
            [0.0, 1.0, 0.0, ty],
            [0.0, 0.0, 1.0, tz],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=float,
    )


def rotation_x(angle_rad: float) -> np.ndarray:
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    return np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, c, -s, 0.0],
            [0.0, s, c, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=float,
    )


def rotation_y(angle_rad: float) -> np.ndarray:
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    return np.array(
        [
            [c, 0.0, s, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-s, 0.0, c, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=float,
    )


def rotation_z(angle_rad: float) -> np.ndarray:
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    return np.array(
        [
            [c, -s, 0.0, 0.0],
            [s, c, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=float,
    )


def transform_points(matrix: np.ndarray, points: np.ndarray) -> np.ndarray:
    ones = np.ones((points.shape[0], 1), dtype=float)
    points_h = np.hstack((points, ones))
    transformed_h = (matrix @ points_h.T).T
    return transformed_h[:, :3]


def focal_from_fov(screen_width: int, fov_deg: float) -> float:
    fov_rad = math.radians(fov_deg)
    return (screen_width / 2.0) / math.tan(fov_rad / 2.0)


def project_point(point_cam: np.ndarray, focal_length: float, width: int, height: int):
    x, y, z = point_cam
    x_2d = (x * focal_length) / z + width / 2.0
    y_2d = (-y * focal_length) / z + height / 2.0
    return int(x_2d), int(y_2d)
