from settings import *
from meshes.base_mesh import BaseMesh


class CubeMesh(BaseMesh):
    def __init__(self, voxel_marker):
        super().__init__()
        self.app = voxel_marker.app
        self.ctx = voxel_marker.app.ctx
        self.program = self.app.shader_program.voxel_marker

        self.vbo_format = '3f 2f'
        self.attrs = ['in_position', 'in_uv']
        self.get_vao()


    def get_vertex_data(self)->np.ndarray:
        vertices = (
            (0,0,1), (1,0,1), (1,1,1), (0,1,1),
            (0,0,0), (1,0,0), (1,1,0), (0,1,0)
        )

        uvs = (
            (0,0), (1,0), (1,1), 
            (1,1), (0,1), (0,0)
        )

        indices = (
            (0,1,2), (2,3,0), #front
            (1,5,6), (6,2,1), #right
            (5,4,7), (7,6,5), #back
            (4,0,3), (3,7,4), #left
            (3,2,6), (6,7,3), #top
            (4,5,1), (1,0,4)  #bottom
        )

        vertex_array = np.zeros(len(indices)*3*5, dtype='f')
        index = 0
        uv_index = 0
        for triangle in indices:
            for vertex_index in triangle:

                for coord in vertices[vertex_index]:
                    vertex_array[index] = coord
                    index += 1

                for uv in uvs[uv_index%6]:
                    vertex_array[index] = uv
                    index += 1
                
                uv_index += 1
        
        return vertex_array
    

    def render(self):
        #self.app.ctx.disable(mgl.DEPTH_TEST)
        self.vao.render()
        self.app.ctx.enable(mgl.DEPTH_TEST)