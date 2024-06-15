from settings import gl_settings, common_settings

import moderngl as mgl
import pygame as pg

import sys

from shader import Shader
from scene import Scene
from player import Player


class Engine:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, gl_settings.GL_MAJOR_VERSION)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, gl_settings.GL_MINOR_VERSION)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, gl_settings.GL_DEPTH_BUFFER_SIZE)

        #pg.display.set_mode(common_settings.WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_mode((0, 0), flags=pg.OPENGL | pg.DOUBLEBUF | pg.FULLSCREEN)
        self.ctx = mgl.create_context()

        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = 'auto'

        self.clock = pg.time.Clock()
        self.time = 0
        self.dt = 0

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.player = None
        self.shader = None
        self.scene = None

        self.running = False

    def on_init(self):
        # Player should be init before all others!
        self.player = Player(self)
        # Shader should be init before World!
        self.shader = Shader(self)
        self.scene = Scene(self)

    def update(self):
        self.player.update()
        self.shader.update()
        self.scene.update()

        self.dt = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        # print("Update!")

    def render(self):
        self.ctx.clear(color=(0.1, 0.16, 0.25, 1.0))
        self.scene.render()
        pg.display.flip()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False
            self.player.event(event)

    def start(self):
        self.running = True
        self.on_init()

        prev_second_ticks = pg.time.get_ticks()

        unprocessed_ticks = 0
        now_ticks = pg.time.get_ticks()
        prev_ticks = now_ticks

        target_update_delta = 1000 / 60

        while self.running:
            self.event()

            now_ticks = pg.time.get_ticks()
            unprocessed_ticks += (now_ticks - prev_ticks)
            prev_ticks = now_ticks

            if unprocessed_ticks >= target_update_delta:
                self.update()
                self.render()

                unprocessed_ticks = 0

            if pg.time.get_ticks() - prev_second_ticks > 1000:
                pg.display.set_caption(f'PyCraft [FPS: {self.clock.get_fps() :.0f}]')
                prev_second_ticks = pg.time.get_ticks()

        pg.quit()
        sys.exit()


if __name__ == '__main__':
    engine = Engine()
    engine.start()
