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
                if noise2(0.1 * x, 0.1 * z) > 0.2:
                    grid_data[x + width * z] = 1
        

        mesh = np.empty(WORLD_AREA * CHUNK_AREA * 3 * 3, dtype = 'uint16')
        mesh_index = 0
        visited = set()

        for x in range(width):
            for z in range(depth):
                idx = x+width*z
                if grid_data[idx] == 0 or idx in visited:
                    continue

                xf = x + 1
                xf_idx = idx
                min_z = z + 1000
                zf = z + 1
                while xf < width and xf_idx not in visited and grid_data[xf_idx] == 1:
                    zf = z
                    zf_idx = idx

                    while zf < depth and zf_idx not in visited and grid_data[zf_idx] == 1:
                        zf += 1
                        zf_idx += width

                    min_z = min(min_z, zf)
                    xf += 1
                    xf_idx += 1
                
                for vx in range(x, xf):
                    for vz in range(z, zf):
                        visited.add(vx + width * vz)
                
                p0 = (x , y, zf)
                p1 = (xf, y, zf)
                p2 = (xf, y, z )
                p3 = (x , y, z )

                for p in (p1, p0, p3, p3, p2, p1):
                    for attr in p:
                        mesh[mesh_index] = attr
                        mesh_index += 1

        return mesh[:mesh_index]
