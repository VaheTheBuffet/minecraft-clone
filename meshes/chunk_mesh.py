from settings import *
from meshes.base_mesh import BaseMesh
from chunk_mesh_builder import build_chunk_mesh


class ChunkMesh(BaseMesh):
    __slots__ = ['chunk', 'app', 'format_size']

    def __init__(self, chunk):
        super().__init__()
        self.app = chunk.app
        self.chunk = chunk
        self.program = self.app.shader_program.chunk
        self.ctx = self.app.ctx
        self.vbo_format = '1u4'
        self.format_size = 6
        self.attrs = ('compressed_data',)

        self.vao = self.get_vao()

    def get_vertex_data(self) -> np.ndarray:
        return build_chunk_mesh(self.chunk.voxels, self.format_size,
                                self.chunk.position, self.chunk.world.voxels)

