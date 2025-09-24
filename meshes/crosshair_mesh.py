from settings import *
from meshes.base_mesh import BaseMesh

class CrosshairMesh(BaseMesh):
    
    def __init__(self, crosshair):
        super().__init__()
        self.crosshair = crosshair
        self.program = crosshair.app.shader_program.crosshair
        self.ctx = crosshair.app.ctx
        self.vbo_format = '3f'
        self.attrs = ['in_position']

        self.get_vao()
    
    def get_vertex_data(self)->np.ndarray:
        d = 0.02
        return np.array([
            -d,0,-0.1,  d,0,-0.1,  d,d,-0.1
        ], dtype='f')