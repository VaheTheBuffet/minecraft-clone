from settings import *
from meshes.base_mesh import BaseMesh
from chunk_mesh_builder import build_water_mesh

class WaterMesh(BaseMesh):
    def __init__(self, water):
        self.water = water
        self.app = water.app
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.water
        self.vbo_format = '3u4'
        self.attrs = ['in_position',]

        self.get_vao()


    def get_vertex_data(self)->np.ndarray:
        return build_water_mesh(self.water.world.voxels)
