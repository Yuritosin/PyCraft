from meshes.base_mesh import BaseMesh
from mesh.chunk_mesh_builder import build_chunk_mesh


class ChunkMesh(BaseMesh):
    def __init__(self, chunk):
        super().__init__()
        self.engine = chunk.engine
        self.chunk = chunk
        self.ctx = self.engine.ctx
        self.program = self.engine.shader.chunk

        self.vbo_format = "1u4"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attrs = ("packedData",)
        self.vao = self.get_vao()

    def rebuild(self):
        self.vao = self.get_vao()

    def get_vertex_data(self):
        mesh = build_chunk_mesh(
            chunk_voxels=self.chunk.voxels,
            format_size=self.format_size,
            chunk_pos=self.chunk.position,
            world_voxels=self.chunk.world.voxels
        )
        return mesh
