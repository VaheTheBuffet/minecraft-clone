from settings import *
from glm import length, normalize #pyright: ignore
from chunk_mesh_builder import is_empty
from enum import Enum

class RayCaster:

    def __init__(self, world):
        self.world = world
        self.player = self.world.app.player

        self.chunk = None
        self.voxel_id = None
        self.voxel_index = None
        self.voxel_local_pos = None
        self.voxel_world_pos = None
        self.voxel_normal = None


    def update(self)->None:
        self.cast_ray()


    def remove_voxel(self)->None:
        if self.voxel_local_pos is None:
            return
        
        if self.chunk is None:
            raise Exception("Chunk is None")
        
        if self.voxel_index == -1:
            raise Exception("Invalid voxel index")


        x, y, z = self.voxel_local_pos
        cx, cy, cz = self.chunk.position

        self.chunk.voxels[self.voxel_index] = 0
        self.chunk.rebuild_mesh()

        if x == 0 and cx > 0:
            neighbor_chunk = self.world.chunks[cx-1 + WORLD_W * cz + WORLD_AREA * cy]
            neighbor_chunk.rebuild_mesh()
        elif x == CHUNK_SIZE-1 and cx < WORLD_W-1:
            neighbor_chunk = self.world.chunks[cx+1 + WORLD_W * cz + WORLD_AREA * cy]
            neighbor_chunk.rebuild_mesh()
        
        if y == 0 and cy > 0:
            neighbor_chunk = self.world.chunks[cx + WORLD_W * cz + WORLD_AREA * (cy-1)]
            neighbor_chunk.rebuild_mesh()
        elif y == CHUNK_SIZE-1 and cy < WORLD_W-1:
            neighbor_chunk = self.world.chunks[cx + WORLD_W * cz + WORLD_AREA * (cy+1)]
            neighbor_chunk.rebuild_mesh()
        
        if z == 0 and cz > 0:
            neighbor_chunk = self.world.chunks[cx + WORLD_W * (cz-1) + WORLD_AREA * cy]
            neighbor_chunk.rebuild_mesh()
        elif z == CHUNK_SIZE-1 and cz < WORLD_W-1:
            neighbor_chunk = self.world.chunks[cx + WORLD_W * (cz+1) + WORLD_AREA * cy]
            neighbor_chunk.rebuild_mesh()


    def place_voxel(self, voxel_id:int = 1)->None:

        if self.voxel_id == 0 or self.voxel_world_pos is None or self.voxel_normal is None:
            return

        place_position = self.voxel_world_pos + self.voxel_normal
        id, voxel_index, local_pos, chunk_index = self.get_voxel_id(place_position)

        self.world.voxels[chunk_index][voxel_index] = voxel_id
        self.world.chunks[chunk_index].rebuild_mesh()


    def cast_ray(self)->bool:
        x1, y1, z1 = self.player.position
        x2, y2, z2 = self.player.position + self.player.forward * MAX_RAY_DISTANCE

        current_voxel_pos = glm.ivec3(x1, y1, z1)
        self.voxel_id = 0
        self.voxel_normal = glm.ivec3(0, 0, 0)
        step_dir = -1

        dx = glm.sign(x2 - x1)
        delta_x = dx / (x2 - x1) if x1 != x2 else 100000
        max_x = delta_x * (1.0 - glm.fract(x1)) if dx > 0 else delta_x * glm.fract(x1)

        dy = glm.sign(y2 - y1)
        delta_y = dy / (y2 - y1) if y1 != y2 else 100000
        max_y = delta_y * (1.0 - glm.fract(y1)) if dy > 0 else delta_y * glm.fract(y1)

        dz = glm.sign(z2 - z1)
        delta_z = dz / (z2 - z1) if z1 != z2 else 100000
        max_z = delta_z * (1.0 - glm.fract(z1)) if dz > 0 else delta_z * glm.fract(z1)

        while not (max_x > 1.0 and max_z > 1.0 and max_y > 1.0):

            result = self.get_voxel_id(current_voxel_pos)
            if result[0] != 0:
                self.voxel_id, self.voxel_index, self.voxel_local_pos, chunk_index = result
                self.voxel_world_pos = current_voxel_pos
                self.chunk_index = chunk_index
                self.chunk = self.world.chunks[chunk_index]

                if step_dir == 0:
                    self.voxel_normal.x = -dx
                elif step_dir == 1:
                    self.voxel_normal.y = -dy
                else:
                    self.voxel_normal.z = -dz
                
                return True

            if max_x < max_y:
                if max_x < max_z:
                    current_voxel_pos.x += dx
                    max_x += delta_x
                    step_dir = 0
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2
            else:
                if max_y < max_z:
                    current_voxel_pos.y += dy
                    max_y += delta_y
                    step_dir = 1
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2
        
        return False
    

    def get_voxel_id(self, world_position:glm.ivec3)->tuple[int, int, glm.ivec3, int]:
        cx, cy, cz = chunk_position = world_position // CHUNK_SIZE
        lx, ly, lz = local_position = world_position % CHUNK_SIZE

        if(0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_W):
            chunk_index = cx + WORLD_W * cz + WORLD_AREA * cy
            voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly

            voxel_id = self.world.voxels[chunk_index][voxel_index]

            return voxel_id, voxel_index, local_position, chunk_index

        return 0, -1, local_position, -1