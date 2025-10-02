from settings import *
from meshes.base_mesh import BaseMesh
from numba import njit

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
        return self.get_vertex_buffer()

    
    @staticmethod
    @njit
    def get_vertex_buffer()->np.ndarray:
        x1 = 0.003 / ASPECT_RATIO
        x2 = 0.02 / ASPECT_RATIO
        y1 = 0.003
        y2 = 0.02
        p = [(-x1, -y2), (x1, -y2), (x1, y2), (-x1, y2),
             (-x2, -y1), (x2, -y1), (x2, y1), (-x2, y1)]
        
        vertex_data = np.empty((36), dtype = 'f')
        idx = 0
        for i in (0, 1, 2, 2, 3, 0, 4, 5, 6, 6, 7, 4):
            for attr in p[i]:
                vertex_data[idx] = attr
                idx += 1
            vertex_data[idx] = 0.1
            idx += 1
        return vertex_data
