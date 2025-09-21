from settings import *
from glm import length, normalize #pyright: ignore
from chunk_mesh_builder import is_empty

class RayCaster:

    def __init__(self, player, world):
        self.player = player
        self.world = world

    def cast_ray(self):
        v_x, v_y, v_z = self.player.foreward
        s_x, s_y, s_z = np.sign(v_x), np.sign(v_y), np.sign(v_z)
        max_x, max_y, max_z = abs(int(v_x * MAX_RAY_DISTANCE)), abs(int(v_x * MAX_RAY_DISTANCE)), abs(int(v_x * MAX_RAY_DISTANCE))

        start_x, start_y, start_z = self.player.x, self.player.y, self.player.z

        cur_x = np.floor(self.player.x) if s_x < 0 else np.ceil(self.player.x)
        cur_y = np.floor(self.player.y) if s_y < 0 else np.ceil(self.player.y)
        cur_z = np.floor(self.player.z) if s_z < 0 else np.ceil(self.player.z)

        d1, d2, d3 = None, None, None

        while abs(cur_x - start_x) < max_x:
            p1 = (cur_x, start_y + v_y/v_x * (cur_x-start_x), start_z + v_z/v_x * (cur_x-start_x))
            c = (p1[0] % CHUNK_SIZE, p1[1] % CHUNK_SIZE, p1[2] % CHUNK_SIZE)

            if not is_empty(c, p1, self.world.voxels):
                d1 = (p1[0]-start_x)**2 + (p1[1]-start_y)**2 + (p1[2]-start_z)**2

            cur_x += s_x


        while abs(cur_y - start_y) < max_y:
            p2 = (start_x + v_x/v_y * (cur_y-start_y), cur_y,  start_z + v_z/v_y * (cur_y-start_y))
            c = (p2[0] % CHUNK_SIZE, p2[1] % CHUNK_SIZE, p2[2] % CHUNK_SIZE)

            if not is_empty(c, p2, self.world.voxels):
                d2 = (p2[0]-start_x)**2 + (p2[1]-start_y)**2 + (p2[2]-start_z)**2

            cur_y += s_y

        while abs(cur_z - start_z) < max_z:
            p3 = (start_x + v_x/v_z * (cur_z-start_z), start_y + v_y/v_z * (cur_z-start_z), cur_z)
            c = (p3[0] % CHUNK_SIZE, p3[1] % CHUNK_SIZE, p3[2] % CHUNK_SIZE)

            if not is_empty(c, p3, self.world.voxels):
                d3 = (p3[0]-start_x)**2 + (p3[1]-start_y)**2 + (p3[2]-start_z)**2

            cur_y += s_y

        
        final_distances = set()
        if d1 is not None:
            final_distances.add(d1)
        if d2 is not None:
            final_distances.add(d2)
        if d3 is not None:
            final_distances.add(d3)


        if len(final_distances) == 0:
            return -1

        winner = min(final_distances)

        if winner is d1:
            return p1

        if winner is d2:
            return p2

        if winner is d3:
            return p3

