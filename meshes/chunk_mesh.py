from settings import *
from meshes.base_mesh import BaseMesh
from chunk_mesh_builder import build_chunk_mesh
from numba import uint8


class ChunkMesh(BaseMesh):
    __slots__ = ['chunk', 'app', 'buf', 'data_length']

    def __init__(self, chunk):
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
        i_d = build_chunk_mesh(self.chunk.voxels, self.chunk.position, self.chunk.world.voxels)
        self.data_length = len(i_d)
        if self.data_length == 0:
            return
        final_data = np.empty(self.data_length * 4, dtype='uint32')
        index = 0
        for datum in i_d:
            final_data[index] = datum
            index +=1
            for _ in range(3):
                final_data[index] = 0
                index += 1

        self.buf = self.ctx.buffer(data = final_data)
    

    def render(self):
        self.buf.bind_to_uniform_block(self.program['InstanceData'].binding)
        self.vao.render(mgl.TRIANGLES, instances = self.data_length)