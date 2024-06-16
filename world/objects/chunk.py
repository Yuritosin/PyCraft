from settings.common_settings import *
from meshes.chunk_mesh import ChunkMesh


class Chunk:
    def __init__(self, world, position):
        self.world = world
        self.position = position
        self.engine = world.engine

        self.m_model = self.get_model_matrix()

        self.voxels = numpy.array = None

        self.mesh = None

        self.is_empty = True

        self.center_position = (glm.vec3(self.position) + 0.5) * CHUNK_SIZE
        self.is_on_frustum = self.engine.player.frustum.is_on_frustum

    def get_model_matrix(self):
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model

    def set_uniform(self):
        self.mesh.program['m_model'].write(self.m_model)

    def build_mesh(self):
        self.mesh = ChunkMesh(self)

    def render(self):
        if not self.is_empty and self.is_on_frustum(self):
            self.set_uniform()
            self.mesh.render()

    def build_voxels(self):
        voxels = numpy.zeros(CHUNK_VOLUME, dtype='uint8')

        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE

        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                wx = x + cx
                wz = z + cz
                world_height = int(glm.simplex(glm.vec2(wx, wz) * 0.01) * 32 + 32)
                local_height = min(world_height - cy, CHUNK_SIZE)
                for y in range(local_height):
                    wy = y + cy
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = wy % 4 + 1

        if numpy.any(voxels):
            self.is_empty = False

        return voxels
