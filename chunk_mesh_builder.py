from settings import *
from numba import njit 
from world_objects.chunk import Chunk


@njit
def compress_data(x:int, y:int, z:int, voxel_id:int, face_id:int, ao_id:int, orientation:int)->np.uint32:
    compressed_data = x
    compressed_data = (compressed_data << 6) | y
    compressed_data = (compressed_data << 6) | z
    compressed_data = (compressed_data << 8) | voxel_id
    compressed_data = (compressed_data << 3) | face_id
    compressed_data = (compressed_data << 2) | ao_id
    compressed_data = (compressed_data << 1) | orientation
    return np.uint32(compressed_data)


@njit
def get_ao(local_position:tuple, world_position, world_voxels:np.ndarray, normal:str)->tuple[int,...]:
    x, y, z = local_position
    wx, wy, wz = world_position

    if normal == 'Y':
        a = is_empty((x-1, y  , z+1), (wx-1, wy  , wz+1), world_voxels)
        b = is_empty((x  , y  , z+1), (wx  , wy  , wz+1), world_voxels)
        c = is_empty((x+1, y  , z+1), (wx+1, wy  , wz+1), world_voxels)
        d = is_empty((x+1, y  , z  ), (wx+1, wy  , wz  ), world_voxels)
        e = is_empty((x+1, y  , z-1), (wx+1, wy  , wz-1), world_voxels)
        f = is_empty((x  , y  , z-1), (wx  , wy  , wz-1), world_voxels)
        g = is_empty((x-1, y  , z-1), (wx-1, wy  , wz-1), world_voxels)
        h = is_empty((x-1, y  , z  ), (wx-1, wy  , wz  ), world_voxels)

    elif normal == 'X':
        a = is_empty((x  , y-1, z+1), (wx  , wy-1, wz+1), world_voxels)
        b = is_empty((x  , y-1, z  ), (wx  , wy-1, wz  ), world_voxels)
        c = is_empty((x  , y-1, z-1), (wx  , wy-1, wz-1), world_voxels)
        d = is_empty((x  , y  , z-1), (wx  , wy  , wz-1), world_voxels)
        e = is_empty((x  , y+1, z-1), (wx  , wy+1, wz-1), world_voxels)
        f = is_empty((x  , y+1, z  ), (wx  , wy+1, wz  ), world_voxels)
        g = is_empty((x  , y+1, z+1), (wx  , wy+1, wz+1), world_voxels)
        h = is_empty((x  , y  , z+1), (wx  , wy  , wz+1), world_voxels)

    else:
        a = is_empty((x-1, y-1, z  ), (wx-1, wy-1, wz  ), world_voxels)
        b = is_empty((x  , y-1, z  ), (wx  , wy-1, wz  ), world_voxels)
        c = is_empty((x+1, y-1, z  ), (wx+1, wy-1, wz  ), world_voxels)
        d = is_empty((x+1, y  , z  ), (wx+1, wy  , wz  ), world_voxels)
        e = is_empty((x+1, y+1, z  ), (wx+1, wy+1, wz  ), world_voxels)
        f = is_empty((x  , y+1, z  ), (wx  , wy+1, wz  ), world_voxels)
        g = is_empty((x-1, y+1, z  ), (wx-1, wy+1, wz  ), world_voxels)
        h = is_empty((x-1, y  , z  ), (wx-1, wy  , wz  ), world_voxels)

    return (a+b+h, b+c+d, d+e+f, f+g+h)


@njit
def world_index(*global_position:int)->tuple[int,int]:
    x, y, z = global_position
    cidx = get_chunk_index(*global_position)
    lx, ly, lz = x % CHUNK_SIZE, y % CHUNK_SIZE, z % CHUNK_SIZE
    vidx = get_voxel_index(lx, ly, lz)

    return cidx, vidx


@njit
def get_voxel_index(*local_position:int)->int:
    x, y, z = local_position

    if not(0 <= x < CHUNK_SIZE and 0 <= y < CHUNK_SIZE and 0 <= z < CHUNK_SIZE):
        return -1
    
    return x + CHUNK_SIZE * z + CHUNK_AREA * y


@njit
def get_chunk_index(*global_position:int)->int:
    wx, wy, wz = global_position

    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE

    if(not(0 <= cx < WORLD_W and 0 <= cz < WORLD_W and 0 <= cy < WORLD_H)):
        return -1

    return cx + WORLD_W * cz + WORLD_AREA * cy 


@njit
def is_empty(local_position:tuple, world_position:tuple, world_voxels:np.ndarray)->bool:

    chunk_index = get_chunk_index(*world_position)
    if chunk_index == -1:
        return False

    x, y, z = local_position
    x = x % CHUNK_SIZE
    y = y % CHUNK_SIZE
    z = z % CHUNK_SIZE

    id = world_voxels[chunk_index][x + CHUNK_SIZE * z + CHUNK_AREA * y]
    return id == EMPTY or id == WATER


@njit
def pair(a:int, b:int)->int:
    return CHUNK_VOL * a + b


@njit
def t0(a:int)->int:
    """trailing zero bits"""
    b = ~a & (a-1)
    return max(int(np.log2(b + 1)), 0)


@njit
def t1(a:int)->int:
    """trailing one bits"""
    b = ~a & (a+1)
    return int(np.log2(b))


@njit
def add_data(vertex_data:np.ndarray, index:int, *vertices:tuple)->int:
    """Adds data to vertex_data array and increments index"""
    for vertex in vertices:
        vertex_data[index] = vertex
        index += 1
    return index


#@njit
def build_chunk_mask(chunk:Chunk)->tuple[np.ndarray,...]:
    """through axis is a byte with solid faces 1 transparent empty 0"""
    faces_xy = np.zeros(CHUNK_AREA, dtype='uint32')
    faces_yz = np.zeros(CHUNK_AREA, dtype='uint32')
    faces_zx = np.zeros(CHUNK_AREA, dtype='uint32')

    for x in range(-1, CHUNK_SIZE + 1):
        for y in range(-1, CHUNK_SIZE + 1):
            for z in range(-1, CHUNK_SIZE + 1):
                voxel_id = chunk.get_voxel(x, y, z)
                if voxel_id != EMPTY and voxel_id != WATER:
                    faces_xy[x + y * P_CHUNK_SIZE] |= 1 << z
                    faces_yz[y + z * P_CHUNK_SIZE] |= 1 << x
                    faces_zx[z + x * P_CHUNK_SIZE] |= 1 << y
    

    return faces_xy, faces_yz, faces_zx


def cull_mask(mask:np.ndarray, axis:int)->np.ndarray:
    res = np.empty(CHUNK_AREA, dtype = 'uint32')
    for j in range(CHUNK_SIZE):
        for k in range(CHUNK_SIZE):
            if axis == 1:
                culled_val = mask[j+CHUNK_SIZE*k] & (mask[j+CHUNK_SIZE*k] << 1)
            else:
                culled_val = mask[j+CHUNK_SIZE*k] & (mask[j+CHUNK_SIZE*k] >> 1)
            res[j + CHUNK_SIZE * k] = culled_val
    return res


@njit
def reorder(i, j, k, axis):
    return i, j, k


@njit
def build_chunk_mesh(chunk:Chunk)->np.ndarray:
    instance_data = np.empty(H_CHUNK_VOL, dtype='uint32')
    index = 0

    mask_xy, mask_yz, mask_zx = build_chunk_mask(chunk)
    culled_mask_xyp, culled_mask_xyn = cull_mask(mask_xy, 1), cull_mask(mask_xy, -1)
    culled_mask_yzp, culled_mask_yzn = cull_mask(mask_yz, 1), cull_mask(mask_xy, -1)
    culled_mask_zxp, culled_mask_zxn = cull_mask(mask_zx, 1), cull_mask(mask_xy, -1)

    masks = (culled_mask_xyp, culled_mask_xyn, culled_mask_yzp, culled_mask_yzn,
             culled_mask_zxp, culled_mask_zxn)

    for axis in range(6):
        for i in range(CHUNK_SIZE):
            for j in range(CHUNK_SIZE):
                for k in range(CHUNK_SIZE):
                    pos = reorder(i, j, k, axis)
                    if chunk.get_voxel(*pos) != WATER or chunk.get_voxel(*pos) != EMPTY:
                        instance_data[index] = compress_data(*pos, int(chunk.get_voxel(*pos)),axis,1,0)



    return instance_data[:index]


@njit
def build_water_mesh(world_voxels:np.ndarray)->np.ndarray:
    """greedy mesher"""
    width = WORLD_W * CHUNK_SIZE
    depth = WORLD_D * CHUNK_SIZE

    y = WATER_LEVEL

    mesh = np.empty(WORLD_AREA * CHUNK_AREA * 3 * 3, dtype = 'uint32')
    mesh_index = 0
    visited = set()

    for x in range(width):
        for z in range(depth):
            idx = world_index(x, y, z)
            if world_voxels[idx] != WATER or pair(*idx) in visited:
                continue

            max_x = x
            max_x_idx = idx
            while max_x < width and pair(*max_x_idx) not in visited and world_voxels[max_x_idx] == WATER:
                max_x += 1
                max_x_idx = world_index(max_x, y, z)
            
            min_z = z + 1
            failed = False
            while min_z < width and not failed:
                for x_probe in range(x, max_x):
                    x_probe_idx = world_index(x_probe, y, min_z)
                    if world_voxels[x_probe_idx] != WATER or pair(*x_probe_idx) in visited:
                        failed = True
                        break
                if not failed:
                    min_z += 1
            
            for vx in range(x, max_x):
                for vz in range(z, min_z):
                    visited.add(pair(*world_index(vx, y, vz)))
            
            p0 = (x    , y+1, min_z)
            p1 = (max_x, y+1, min_z)
            p2 = (max_x, y+1, z    )
            p3 = (x    , y+1, z    )

            for p in (p0, p1, p2, p2, p3, p0):
                for attr in p:
                    mesh[mesh_index] = attr
                    mesh_index += 1

    return mesh[:mesh_index]
