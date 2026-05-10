from dataclasses import dataclass
import numpy as np
import random
from bsp import Triangle

@dataclass
class SolidScene:
    triangles: list[Triangle]

def cuboid(center_x: float, center_z: float, width: float, depth: float, height: float, color: tuple):
    hw = width / 2.0
    hd = depth / 2.0

    y0 = 0.0
    y1 = height

    # 8 vertices
    v0 = [center_x - hw, y0, center_z - hd]
    v1 = [center_x + hw, y0, center_z - hd]
    v2 = [center_x + hw, y0, center_z + hd]
    v3 = [center_x - hw, y0, center_z + hd]
    v4 = [center_x - hw, y1, center_z - hd]
    v5 = [center_x + hw, y1, center_z - hd]
    v6 = [center_x + hw, y1, center_z + hd]
    v7 = [center_x - hw, y1, center_z + hd]

    triangles = []
    
    # helper for adding quad
    def add_quad(p1, p2, p3, p4, c):
        triangles.append(Triangle(p1, p2, p3, c))
        triangles.append(Triangle(p1, p3, p4, c))

    # slightly varied colors for faces
    r, g, b = color
    c_bottom = (max(r-20,0), max(g-20,0), max(b-20,0))
    c_top = (min(r+20,255), min(g+20,255), min(b+20,255))
    c_front = color
    c_back = (max(r-10,0), max(g-10,0), max(b-10,0))
    c_left = (min(r+10,255), min(g+10,255), min(b+10,255))
    c_right = c_back

    # Bottom (facing down)
    add_quad(v3, v2, v1, v0, c_bottom)
    # Top (facing up)
    add_quad(v4, v5, v6, v7, c_top)
    # Front (facing -Z)
    add_quad(v1, v0, v4, v5, c_front)
    # Back (facing +Z)
    add_quad(v2, v3, v7, v6, c_back)
    # Right (facing +X)
    add_quad(v1, v5, v6, v2, c_right)
    # Left (facing -X)
    add_quad(v0, v3, v7, v4, c_left)

    return triangles

def build_scene(filepath: str = "scene.txt") -> SolidScene:
    all_triangles = []

    try:
        with open(filepath, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 12:
                    v0 = [float(parts[0]), float(parts[1]), float(parts[2])]
                    v1 = [float(parts[3]), float(parts[4]), float(parts[5])]
                    v2 = [float(parts[6]), float(parts[7]), float(parts[8])]
                    color = (int(parts[9]), int(parts[10]), int(parts[11]))
                    
                    all_triangles.append(Triangle(v0, v1, v2, color))
    except FileNotFoundError:
        print(f"Warning: file {filepath} not found. Returning empty scene.")

    return SolidScene(triangles=all_triangles)
