from settings.common_settings import *


class Shader:
    def __init__(self, engine):
        self.engine = engine
        self.ctx = engine.ctx
        self.player = engine.player

        self.chunk = self.get_program('chunk')
        self.clouds = self.get_program('clouds')

        self.set_uniform_on_init()

    def set_uniform_on_init(self):
        self.chunk['m_proj'].write(self.player.m_proj)
        self.chunk['m_model'].write(glm.mat4())

        self.clouds['m_proj'].write(self.player.m_proj)
        self.clouds['center'] = WORLD_CENTER_XZ
        self.clouds['bg_color'].write(BACKGROUND_COLOR)
        self.clouds['cloud_scale'] = 24

    def update(self):
        self.chunk['m_view'].write(self.player.m_view)
        self.clouds['m_view'].write(self.player.m_view)

    def get_program(self, shader_name):
        with open(f"resources/shaders/{shader_name}_vert.glsl") as file:
            vertex_shader = file.read()
        with open(f"resources/shaders/{shader_name}_frag.glsl") as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
