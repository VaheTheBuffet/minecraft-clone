from settings import *
from numba import uint8, uint32
from numba import njit #pyright: ignore


@njit
def compress_data(x:int, y:int, z:int, voxel_id:int, face_id:int, ao_id:int, orientation:int)->uint32: #pyright: ignore because this is not a class
    compressed_data = x
    compressed_data = (compressed_data << 6) | y
    compressed_data = (compressed_data << 6) | z
    compressed_data = (compressed_data << 8) | voxel_id
    compressed_data = (compressed_data << 3) | face_id
    compressed_data = (compressed_data << 2) | ao_id
    compressed_data = (compressed_data << 1) | orientation
    return uint32(compressed_data)


@njit
def get_ao(local_position:tuple, world_position, world_voxels:np.ndarray, normal:str)->tuple:
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
def world_index(*global_position:int):
    x, y, z = global_position
    cidx = get_chunk_index(*global_position)
    lx, ly, lz = x % CHUNK_SIZE, y % CHUNK_SIZE, z % CHUNK_SIZE
    vidx = get_voxel_index(lx, ly, lz)

    return cidx, vidx


@njit
def get_voxel_index(*local_position:int):
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
    
    return world_voxels[chunk_index][x + CHUNK_SIZE * z + CHUNK_AREA * y] == EMPTY


@njit
def add_data(vertex_data:np.ndarray, index:int, *vertices:tuple)->int:
    """Adds data to vertex_data array and increments index"""
    for vertex in vertices:
        vertex_data[index] = vertex
        index += 1
    return index


@njit
def build_chunk_mesh(chunk_voxels:np.ndarray, format_size:int, chunk_position:tuple, world_voxels:np.ndarray)->np.ndarray:
    vertex_data = np.empty(CHUNK_VOL * 18, dtype='uint32')
    cx, cy, cz = chunk_position
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):

                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]

                if voxel_id == EMPTY or WATER:
                    continue
    
                wx = cx * CHUNK_SIZE + x
                wy = cy * CHUNK_SIZE + y
                wz = cz * CHUNK_SIZE + z

                if is_empty((x, y+1, z), (wx, wy+1, wz), world_voxels):
                    ao_values = get_ao((x, y+1, z), (wx, wy+1, wz), world_voxels, 'Y')
                    orientation = int(ao_values[0] + ao_values[2] > ao_values[1] + ao_values[3])
                    v0 = compress_data(x  , y+1, z+1, voxel_id, 0, ao_values[0], orientation)
                    v1 = compress_data(x+1, y+1, z+1, voxel_id, 0, ao_values[1], orientation)
                    v2 = compress_data(x+1, y+1, z  , voxel_id, 0, ao_values[2], orientation)
                    v3 = compress_data(x  , y+1, z  , voxel_id, 0, ao_values[3], orientation)

                    if(orientation):
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v1, v2, v3, v1, v3, v0)

                if is_empty((x, y-1, z), (wx, wy-1, wz), world_voxels):
                    ao_values = get_ao((x, y-1, z), (wx, wy-1, wz), world_voxels, 'Y')
                    orientation = int(ao_values[0] + ao_values[2] > ao_values[1] + ao_values[3])
                    v0 = compress_data(x  , y  , z  , voxel_id, 1, ao_values[1], orientation)
                    v1 = compress_data(x+1, y  , z  , voxel_id, 1, ao_values[0], orientation)
                    v2 = compress_data(x+1, y  , z+1, voxel_id, 1, ao_values[3], orientation)
                    v3 = compress_data(x  , y  , z+1, voxel_id, 1, ao_values[2], orientation)

                    if(orientation):
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v1, v2, v3, v1, v3, v0)
                    
                if is_empty((x+1, y, z), (wx+1, wy, wz), world_voxels):
                    ao_values = get_ao((x+1, y, z), (wx+1, wy, wz), world_voxels, 'X')
                    orientation = int(ao_values[0] + ao_values[2] > ao_values[1] + ao_values[3])
                    v0 = compress_data(x+1, y  , z+1, voxel_id, 2, ao_values[0], orientation)
                    v1 = compress_data(x+1, y  , z  , voxel_id, 2, ao_values[1], orientation)
                    v2 = compress_data(x+1, y+1, z  , voxel_id, 2, ao_values[2], orientation)
                    v3 = compress_data(x+1, y+1, z+1, voxel_id, 2, ao_values[3], orientation)

                    if(orientation):
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v1, v2, v3, v1, v3, v0)

                if is_empty((x-1, y, z), (wx-1, wy, wz), world_voxels):
                    ao_values = get_ao((x-1, y, z), (wx-1, wy, wz), world_voxels, 'X')
                    orientation = int(ao_values[0] + ao_values[2] > ao_values[1] + ao_values[3])
                    v0 = compress_data(x  , y  , z  , voxel_id, 3, ao_values[1], orientation)
                    v1 = compress_data(x  , y  , z+1, voxel_id, 3, ao_values[0], orientation)
                    v2 = compress_data(x  , y+1, z+1, voxel_id, 3, ao_values[3], orientation)
                    v3 = compress_data(x  , y+1, z  , voxel_id, 3, ao_values[2], orientation)

                    if(orientation):
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v1, v2, v3, v1, v3, v0)
                    
                if is_empty((x, y, z+1), (wx, wy, wz+1), world_voxels):
                    ao_values = get_ao((x, y, z+1), (wx, wy, wz+1), world_voxels, 'Z')
                    orientation = int(ao_values[0] + ao_values[2] > ao_values[1] + ao_values[3])
                    v0 = compress_data(x  , y  , z+1, voxel_id, 4, ao_values[0], orientation)
                    v1 = compress_data(x+1, y  , z+1, voxel_id, 4, ao_values[1], orientation)
                    v2 = compress_data(x+1, y+1, z+1, voxel_id, 4, ao_values[2], orientation)
                    v3 = compress_data(x  , y+1, z+1, voxel_id, 4, ao_values[3], orientation)

                    if(orientation):
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v1, v2, v3, v1, v3, v0)

                if is_empty((x, y, z-1), (wx, wy, wz-1), world_voxels):
                    ao_values = get_ao((x, y, z-1), (wx, wy, wz-1), world_voxels, 'Z')
                    orientation = int(ao_values[0] + ao_values[2] > ao_values[1] + ao_values[3])
                    v0 = compress_data(x+1, y  , z  , voxel_id, 5, ao_values[1], orientation)
                    v1 = compress_data(x  , y  , z  , voxel_id, 5, ao_values[0], orientation)
                    v2 = compress_data(x  , y+1, z  , voxel_id, 5, ao_values[3], orientation)
                    v3 = compress_data(x+1, y+1, z  , voxel_id, 5, ao_values[2], orientation)

                    if(orientation):
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v1, v2, v3, v1, v3, v0)

    return vertex_data[:index+1]


@njit
def build_water_mesh(world):
    width = WORLD_W * CHUNK_SIZE
    depth = WORLD_D * CHUNK_SIZE
    y = WATER_LEVEL

    mesh = np.empty(WORLD_AREA * CHUNK_AREA * 3 * 3, dtype = 'uint16')
    mesh_index = 0
    visited = set()

    for x in range(width):
        for z in range(depth):
            idx = x+width*z
            if world.voxels[idx] != WATER or idx in visited:
                continue

            xf = x + 1
            xf_idx = idx
            min_z = z + 1000
            zf = z + 1
            while xf < width and xf_idx not in visited and world.voxels[xf_idx] == WATER:
                zf = z
                zf_idx = idx

                while zf < depth and zf_idx not in visited and world.voxels[zf_idx] == WATER:
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
