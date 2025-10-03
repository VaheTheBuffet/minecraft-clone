import world
from terrain_generation import *
from settings import *
from meshes.chunk_mesh import ChunkMesh


class Chunk:

    def __init__(self, w:'world.World', *position:int):
        self.position = position
        self.id = position[0] + position[2] * WORLD_W + position[1] * WORLD_AREA
        self.world = w
        self.app = w.app
        self.is_empty = True
        self.voxels:np.ndarray | None = None

        self.center = (glm.vec3(position) + 0.5) * CHUNK_SIZE


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
        generate_terrain(voxels, cx, cy, cz)
        self.is_empty = not np.any(voxels)

        return voxels


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
