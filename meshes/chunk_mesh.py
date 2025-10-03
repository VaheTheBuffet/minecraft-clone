from settings import *
from meshes.base_mesh import BaseMesh
from world_objects import chunk
from util import build_chunk_mesh


class ChunkMesh(BaseMesh):
    __slots__ = ['chunk', 'app', 'buf', 'data_length']

    def __init__(self, chunk:'chunk.Chunk'):
        super().__init__()
        self.app = chunk.app
        self.chunk = chunk
        self.program = self.app.shader_program.chunk
        self.ctx = self.app.ctx
        self.vbo_format = '3u1'
        self.attrs = ['in_position',]

        self.get_vao()


    def get_vertex_data(self) -> np.ndarray:
        self.set_instance_data()
        return np.array([
            0,1,1, 1,1,1, 1,1,0, 
            1,1,0, 0,1,0, 0,1,1
        ], dtype='uint8')


    def set_instance_data(self):
        i_d = build_chunk_mesh(self.chunk.world.voxels, self.chunk.id)
        self.data_length = len(i_d)
        if self.data_length == 0:
            return
        self.buf = self.ctx.buffer(data = i_d)
    

    def render(self):
        self.buf.bind_to_uniform_block(self.program['InstanceData'].binding)
        self.vao.render(mgl.TRIANGLES, instances = self.data_length)