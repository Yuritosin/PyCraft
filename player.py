import pygame as pg
from camera import Camera
from settings.common_settings import *


class Player(Camera):
    def __init__(self, engine, position=PLAYER_POS, yaw=-90, pitch=0):
        self.engine = engine
        super().__init__(position, yaw, pitch)

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        velocity = PLAYER_SPEED * self.engine.dt
        if key_state[pg.K_w]:
            self.move_forward(velocity)
        if key_state[pg.K_d]:
            self.move_right(velocity)
        if key_state[pg.K_s]:
            self.move_back(velocity)
        if key_state[pg.K_a]:
            self.move_left(velocity)
        if key_state[pg.K_e]:
            # self.move_down(velocity)
            self.position -= glm.vec3(0.0, -1.0, 0.0) * velocity
        if key_state[pg.K_q]:
            # self.move_up(velocity)
            self.position -= glm.vec3(0.0, 1.0, 0.0) * velocity

        if key_state[pg.K_LEFT]:
            self.rotate_yaw(-0.05)
        if key_state[pg.K_RIGHT]:
            self.rotate_yaw(0.05)
        if key_state[pg.K_UP]:
            self.rotate_pitch(-0.05)
        if key_state[pg.K_DOWN]:
            self.rotate_pitch(0.05)

    def update(self):
        self.keyboard_control()
        self.mouse_control()
        super().update()

    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            voxel_handler = self.engine.scene.world.voxel_handler
            if event.button == pg.BUTTON_LEFT:
                voxel_handler.remove_voxel()
            if event.button == pg.BUTTON_RIGHT:
                voxel_handler.add_voxel()

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)
