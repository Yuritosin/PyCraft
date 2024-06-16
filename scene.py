import moderngl
from settings.common_settings import *
from world.world import World
from world.objects.clouds import Clouds


class Scene:
    def __init__(self, engine):
        self.engine = engine
        self.world = World(self.engine)
        self.clouds = Clouds(self.engine)

    def update(self):
        self.world.update()
        self.clouds.update()

    def render(self):
        self.world.render()

        self.engine.ctx.disable(moderngl.CULL_FACE)
        self.clouds.render()
        self.engine.ctx.enable(moderngl.CULL_FACE)
