from settings import *
from world_objects.chunk import Chunk
from ray_caster import RayCaster
from chunk_mesh_builder import world_index
from world_objects.water import Water

class World:

    def __init__(self, app):
        self.app = app
        self.chunks = np.empty([WORLD_VOL], dtype = 'object')
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype = 'uint8')
        self.app.ray_caster = RayCaster(self)
        self.ray_caster = self.app.ray_caster
        self.water = Water(self)

        self.build_chunks()
        self.build_chunk_mesh()


    def build_chunks(self):
        for x in range(WORLD_W):
            for z in range(WORLD_W):
                for y in range(WORLD_H):
                    chunk = Chunk(self, x, y, z)
                    chunk_index = x + WORLD_W * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk
                    self.voxels[chunk_index] = chunk.build_voxels()
                    chunk.voxels = self.voxels[chunk_index]


    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()
        self.water.build_mesh()


    def update(self):
        self.ray_caster.update()
        x, y, z = self.app.player.position
        x = int(x); y = int(y); z = int(z)
        voxel_id = self.voxels[world_index(x, y, z)]
        self.chunks[0].mesh.program['underwater'] = 1 if voxel_id == WATER else 0


    def render(self):
        for chunk in self.chunks:
            chunk.render()
        self.water.render()
