from settings.common_settings import *
from world.objects.chunk import Chunk
from voxel_handler import VoxelHandler


class World:
    def __init__(self, engine):
        self.engine = engine
        self.chunks = [None for _ in range(WORLD_VOLUME)]
        self.voxels = numpy.empty([WORLD_VOLUME, CHUNK_VOLUME], dtype="uint32")
        # I'm literally don't know whats happening but it's line started throw OverflowError
        #self.voxels = numpy.empty([WORLD_VOLUME, CHUNK_VOLUME], dtype="uint8")
        self.build_chunk()
        self.build_chunk_mesh()
        self.voxel_handler = VoxelHandler(self)

    def build_chunk(self):
        for x in range(WORLD_W):
            for y in range(WORLD_H):
                for z in range(WORLD_D):
                    chunk = Chunk(self, position=(x, y, z))

                    chunk_index = x + WORLD_W * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk

                    self.voxels[chunk_index] = chunk.build_voxels()

                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def update(self):
        self.voxel_handler.update()

    def render(self):
        for chunk in self.chunks:
            chunk.render()
