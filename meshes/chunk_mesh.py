from settings import *
from meshes.base_mesh import BaseMesh
from world_objects import chunk
from util import build_chunk_mesh


class ChunkMesh(BaseMesh):
    __slots__ = ['chunk', 'app', 'buf', 'face_indices','i_d']

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
        self.set_instance_data()
        return np.array([
            0,1,1, 1,1,1, 1,1,0, 
            1,1,0, 0,1,0, 0,1,1
        ], dtype='uint8')


    def set_instance_data(self):
        self.i_d, self.face_indices = build_chunk_mesh(self.chunk.world.voxels, self.chunk.id)


    def render(self):
        cur_idx = 0
        buf = self.ctx.buffer(reserve=len(self.i_d)*4)
        for face in range(6):
            a, b, = self.face_indices[face], self.face_indices[face+1]
            if self.chunk.visible_faces[face] and a!=b:
                buf.write(self.i_d[a:b], offset = 4 * cur_idx)
                cur_idx += (b-a)

        buf.bind_to_uniform_block(self.program['InstanceData'].binding)
        self.vao.render(mgl.TRIANGLES, instances = cur_idx)