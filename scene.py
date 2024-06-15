from settings.common_settings import *
from world.world import World


class Scene:
    def __init__(self, engine):
        self.engine = engine
        self.world = World(self.engine)

    def update(self):
        self.world.update()

    def render(self):
        self.world.render()