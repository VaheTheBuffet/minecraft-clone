from settings import *
from meshes.base_mesh import BaseMesh

class QuadMesh(BaseMesh):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.ctx = app.ctx
        self.program = app.shader_program.quad

        self.vbo_format = '3f4'
        self.attrs = ['in_position']

        self.get_vao()


    def get_vertex_data(self):
        vertices = ((0,1,1), (1,1,1), (1,1,0), (0,1,0))
        indices = (0,1,2,2,3,0)
        vertex_data = np.empty(18,dtype='float32')
        index = 0
        for idx in indices:
            for coord in vertices[idx]:
                vertex_data[index] = coord
                index +=1

        faces = [0,1,2,3,4,5]
        face_id = np.empty(24, dtype='uint32')
        index = 0
        for face in faces:
            face_id[index] = face
            index += 1
            for _ in range(3):
                face_id[index] = 0
                index += 1

        self.buf = self.ctx.buffer(data=face_id)

        print(self.program['FaceIdBuffer'].size)
        print(vertex_data)
        return vertex_data
    

    def render(self):
        self.buf.bind_to_uniform_block(self.program['FaceIdBuffer'].binding)
        self.vao.render(mgl.TRIANGLES, instances=6)