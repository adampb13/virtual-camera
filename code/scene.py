from dataclasses import dataclass
import numpy as np


@dataclass
class WireframeScene:
    vertices: np.ndarray
    edges: list[tuple[int, int]]


def cuboid(center_x: float, center_z: float, width: float, depth: float, height: float):
    hw = width / 2.0
    hd = depth / 2.0

    y0 = 0.0
    y1 = height

    vertices = np.array(
        [
            [center_x - hw, y0, center_z - hd],
            [center_x + hw, y0, center_z - hd],
            [center_x + hw, y0, center_z + hd],
            [center_x - hw, y0, center_z + hd],
            [center_x - hw, y1, center_z - hd],
            [center_x + hw, y1, center_z - hd],
            [center_x + hw, y1, center_z + hd],
            [center_x - hw, y1, center_z + hd],
        ],
        dtype=float,
    )

    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    ]

    return vertices, edges


def build_scene() -> WireframeScene:
    all_vertices: list[np.ndarray] = []
    all_edges: list[tuple[int, int]] = []
    offset = 0

    buildings = [
        (-12.0, 24.0, 8.0, 8.0, 7.0),
        (12.0, 30.0, 10.0, 9.0, 12.0),
        (-10.0, 48.0, 9.0, 8.0, 16.0),
        (13.0, 56.0, 11.0, 10.0, 10.0),
    ]

    for cx, cz, w, d, h in buildings:
        verts, edges = cuboid(cx, cz, w, d, h)
        all_vertices.append(verts)
        all_edges.extend((a + offset, b + offset) for a, b in edges)
        offset += verts.shape[0]

    road_vertices = np.array(
        [
            [-4.0, 0.0, 4.0],
            [-4.0, 0.0, 120.0],
            [4.0, 0.0, 4.0],
            [4.0, 0.0, 120.0],
        ],
        dtype=float,
    )
    road_edges = [(0, 1), (2, 3)]

    all_vertices.append(road_vertices)
    all_edges.extend((a + offset, b + offset) for a, b in road_edges)

    return WireframeScene(vertices=np.vstack(all_vertices), edges=all_edges)
