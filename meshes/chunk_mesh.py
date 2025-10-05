from settings import *
from meshes.base_mesh import BaseMesh
from world_objects import chunk
from util import build_chunk_mesh


class ChunkMesh(BaseMesh):
    __slots__ = ['chunk', 'app', 'buf', 'buf_array', 'data_length']

    def __init__(self, chunk:'chunk.Chunk'):
        super().__init__()
        self.app = chunk.app
        self.chunk = chunk
        self.program = self.app.shader_program.chunk
        self.ctx = self.app.ctx
        self.buf = None
        self.vbo_format = '3u1'
        self.attrs = ['in_position',]

        self.get_vao()


    def get_vertex_data(self) -> np.ndarray:
        return np.array([
            0,1,1, 1,1,1, 1,1,0, 
            1,1,0, 0,1,0, 0,1,1
        ], dtype='uint8')


    def get_vao(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        i_d = build_chunk_mesh(self.chunk.world.voxels, self.chunk.id)
        self.data_length = len(i_d[0])

        if self.data_length > 0:
            buf = self.ctx.buffer(data = i_d[0])

            self.vao = self.ctx.vertex_array(
                self.program, [(vbo, self.vbo_format, *self.attrs),
                               (buf, '1u4 /i', 'compressed_data')], skip_errors = False
            )
        

    def render(self):
        self.vao.render(mgl.TRIANGLES, instances = self.data_length)
