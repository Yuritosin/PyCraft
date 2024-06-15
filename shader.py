from settings.common_settings import glm


class Shader:
    def __init__(self, engine):
        self.engine = engine
        self.ctx = engine.ctx
        self.player = engine.player

        self.chunk = self.get_program('chunk')

        self.set_uniform_on_init()

    def set_uniform_on_init(self):
        self.chunk['m_proj'].write(self.player.m_proj)
        self.chunk['m_model'].write(glm.mat4())

    def update(self):
        self.chunk['m_view'].write(self.player.m_view)

    def get_program(self, shader_name):
        with open(f"resources/shaders/{shader_name}_vert.glsl") as file:
            vertex_shader = file.read()
        with open(f"resources/shaders/{shader_name}_frag.glsl") as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
