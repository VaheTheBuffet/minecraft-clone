from settings import *
from meshes.base_mesh import BaseMesh
from numba import njit
from terrain_generation import noise2

class CloudMesh(BaseMesh):
    def __init__(self, clouds):
        self.clouds = clouds
        self.program = clouds.app.shader_program.clouds
        self.ctx = clouds.app.ctx
        self.vbo_format = '3u2'
        self.attrs = ['in_position',]

        self.get_vao()


    def get_vertex_data(self)->np.ndarray:
        return self.build_mesh()
    

    @staticmethod
    @njit
    def build_mesh()->np.ndarray:
        width = WORLD_W * CHUNK_SIZE
        depth = WORLD_D * CHUNK_SIZE
        y = CLOUD_HEIGHT

        grid_data = np.zeros((width * depth), dtype='uint8')
        for x in range(width):
            for z in range(depth):
                if noise2(0.1 * x, 0.1 * y) > 0.2:
                    grid_data[x + width * z] = 1
        

        mesh = np.empty(WORLD_AREA * CHUNK_AREA * 3 * 3, dtype = 'uint16')
        mesh_index = 0
        visited = set()

        for x in range(width):
            for z in range(depth):
                idx = x+width*z
                if grid_data[idx] == 0 or idx in visited:
                    continue

                dx = 0
                min_z = 1000
                while x + dx < width and grid_data[idx + dx] == 1:
                    dz = 0
                    while z + dz < depth and grid_data[idx + width * dz] == 1:
                        dz += 1
                    min_z = min(min_z, dz)
                    dx += 1
                
                for vx in range(x, x+dx):
                    for vz in range(z, z+min_z):
                        visited.add(vx + width * vz)
                
                p0 = (x   , y, z + min_z)
                p1 = (x+dx, y, z + min_z)
                p2 = (x+dx, y, z        )
                p3 = (x   , y, z        )

                for p in (p0, p1, p2, p2, p3, p0):
                    for attr in p:
                        mesh[mesh_index] = attr
                        mesh_index += 1

        print(mesh[:18])
        return mesh
