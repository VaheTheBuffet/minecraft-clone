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
        x = 0.02 / ASPECT_RATIO
        y = 0.02
        return np.array([
            x,0,-0.1, 0,y,-0.1, -x,0,-0.1,
            -x,0,-0.1, 0,-y,-0.1, x,0,-0.1
        ], dtype='f')