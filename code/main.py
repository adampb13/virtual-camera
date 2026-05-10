import math
import sys
import os

import numpy as np
import pygame

from camera import Camera
from math3d import focal_from_fov
from renderer import SolidRenderer
from scene import build_scene
from bsp import build_bsp, traverse_bsp


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))


def run() -> None:
    pygame.init()

    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("3D Solid BSP Camera Engine")
    clock = pygame.time.Clock()

    # Ensure we use an absolute path relative to main.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    scene_path = os.path.join(current_dir, "scene.txt")
    scene = build_scene(scene_path)
    bsp_tree = build_bsp(scene.triangles)

    camera = Camera(
        position=np.array([0.0, 2.0, -6.0], dtype=float),
        pitch=0.0,
        yaw=0.0,
        roll=0.0,
    )

    fov_deg = 90.0
    focal_length = focal_from_fov(width, fov_deg)

    renderer = SolidRenderer(width, height, near_plane=0.1)

    move_speed = 0.65
    rotate_speed = math.radians(1.5)
    zoom_speed_deg = 1.0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        step = move_speed * (dt * 60.0)
        angle_step = rotate_speed * (dt * 60.0)

        forward = camera.forward()
        right = camera.right()
        up = camera.up()

        # Translation controls: W/S, A/D, R/F.
        if keys[pygame.K_w]:
            camera.position += forward * step
        if keys[pygame.K_s]:
            camera.position -= forward * step
        if keys[pygame.K_d]:
            camera.position += right * step
        if keys[pygame.K_a]:
            camera.position -= right * step
        if keys[pygame.K_r]:
            camera.position += up * step
        if keys[pygame.K_f]:
            camera.position -= up * step

        # Rotation controls: arrows for pitch/yaw, Q/E for roll.
        if keys[pygame.K_UP]:
            camera.pitch += angle_step
        if keys[pygame.K_DOWN]:
            camera.pitch -= angle_step
        if keys[pygame.K_LEFT]:
            camera.yaw -= angle_step
        if keys[pygame.K_RIGHT]:
            camera.yaw += angle_step
        if keys[pygame.K_q]:
            camera.roll -= angle_step
        if keys[pygame.K_e]:
            camera.roll += angle_step

        camera.pitch = clamp(camera.pitch, math.radians(-89.0), math.radians(89.0))

        # Zoom controls: Z/X changes field of view and derived focal length.
        if keys[pygame.K_z]:
            fov_deg -= zoom_speed_deg
        if keys[pygame.K_x]:
            fov_deg += zoom_speed_deg

        fov_deg = clamp(fov_deg, 30.0, 120.0)
        focal_length = focal_from_fov(width, fov_deg)

        view = camera.view_matrix()
        
        sorted_triangles = traverse_bsp(bsp_tree, camera.position)

        screen.fill((15, 18, 24))
        renderer.draw(screen, sorted_triangles, view, focal_length)

        info = (
            f"Pos: ({camera.position[0]:6.2f}, {camera.position[1]:6.2f}, {camera.position[2]:6.2f})   "
            f"Pitch: {math.degrees(camera.pitch):6.1f}   "
            f"Yaw: {math.degrees(camera.yaw):6.1f}   "
            f"Roll: {math.degrees(camera.roll):6.1f}   "
            f"FOV: {fov_deg:5.1f}"
        )
        text = pygame.font.SysFont("consolas", 20).render(info, True, (120, 210, 130))
        screen.blit(text, (16, 16))

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    run()
