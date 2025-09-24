from settings import *
from meshes.chunk_mesh import ChunkMesh
import glm

class Chunk:
    __slots__ = ['voxels', 'mesh', 'app', 'position', 'is_empty', 'world', 'center']

    def __init__(self, world, *position):
        self.position = position
        self.world = world
        self.app = world.app
        self.is_empty = True

        self.center = (glm.vec3(position) + 0.5) * CHUNK_SIZE

    
    def set_uniforms(self):
        self.mesh.program['m_model'].write(
            glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE) #pyright: ignore
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
        voxels = np.zeros(CHUNK_VOL, dtype = 'uint8')

        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE

        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                wx = x + cx
                wz = z + cz

                global_height = int(glm.simplex(glm.vec2(wx, wz) * 0.01) * 32 + 32)
                local_height = min(global_height - cy, CHUNK_SIZE)

                for y in range(local_height):
                    wy = y + cy
                    voxels[x + z * CHUNK_SIZE + y * CHUNK_AREA] = wy + 1

                self.is_empty = not np.any(voxels)

        return voxels
