from settings import *
from meshes.chunk_mesh import ChunkMesh
from terrain_generation import *
from time import perf_counter

class Chunk:
    __slots__ = ['voxels', 'mesh', 'app', 'position', 'is_empty', 'world', 'center']

    def __init__(self, world, *position):
        self.position = position
        self.world = world
        self.app = world.app
        self.is_empty = True

        self.center = (glm.vec3(position) + 0.5) * CHUNK_SIZE

    
    @njit
    def get_voxel(self, x:int, y:int, z:int)->np.uint8 | int:
        if 0 <= x < CHUNK_SIZE and 0 <= y < CHUNK_SIZE and 0 <= z < CHUNK_SIZE:
            return self.voxels[x+z*CHUNK_SIZE+y*CHUNK_AREA]

        cx = x + x // 32; cy = y + y // 32; cz = z + z // 32
        lx = x % 32; ly = y % 32; lz = z % 32
        return self.world.get_voxel((cx, cy, cz), (lx, ly, lz))


    def set_uniforms(self):
        self.mesh.program['m_model'].write(
            glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        )


    def rebuild_mesh(self):
        self.mesh.get_vao()


    def build_mesh(self):
        self.mesh = ChunkMesh(self)


    def is_in_view(self):
        return self.app.player.frustum.is_on_frustum(self)


    def render(self):
        if not self.is_empty and self.is_in_view():
            self.set_uniforms()
            self.mesh.render()


    def build_voxels(self) -> np.ndarray:
        voxels = np.zeros((CHUNK_VOL), dtype = 'uint8')

        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE
        self.generate_terrain(voxels, cx, cy, cz)
        self.is_empty = not np.any(voxels)

        return voxels


    @staticmethod
    @njit
    def generate_terrain(voxels, cx, cy, cz):
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                wx = x + cx
                wz = z + cz

                global_height = get_height(wx, wz)
                local_height = min(global_height - cy, CHUNK_SIZE)

                for y in range(local_height):
                    wy = y + cy
                    set_voxel_id(voxels, x, y, z, wx, wy, wz, global_height)
