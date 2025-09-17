from settings import *
from numba import uint8
from numba import njit #pyright: ignore

@njit
def to_uint8(x:int, y:int, z:int, voxel_id:int, face_id:int, ao_id:int):
    return uint8(x), uint8(y), uint8(z), uint8(voxel_id), uint8(face_id), uint8(ao_id)


@njit
def get_ao(local_position:tuple, world_position, world_voxels:np.ndarray, normal:str)->tuple:
    x, y, z = local_position
    wx, wy, wz = world_position

    if normal == 'Y':
        a = is_void((x-1, y  , z+1), (wx-1, wy  , wz+1), world_voxels)
        b = is_void((x  , y  , z+1), (wx  , wy  , wz+1), world_voxels)
        c = is_void((x+1, y  , z+1), (wx+1, wy  , wz+1), world_voxels)
        d = is_void((x+1, y  , z  ), (wx+1, wy  , wz  ), world_voxels)
        e = is_void((x+1, y  , z-1), (wx+1, wy  , wz-1), world_voxels)
        f = is_void((x  , y  , z-1), (wx  , wy  , wz-1), world_voxels)
        g = is_void((x-1, y  , z-1), (wx-1, wy  , wz-1), world_voxels)
        h = is_void((x-1, y  , z  ), (wx-1, wy  , wz  ), world_voxels)

    elif normal == 'X':
        a = is_void((x  , y-1, z-1), (wx  , wy-1, wz-1), world_voxels)
        b = is_void((x  , y-1, z  ), (wx  , wy-1, wz  ), world_voxels)
        c = is_void((x  , y-1, z+1), (wx  , wy-1, wz+1), world_voxels)
        d = is_void((x  , y  , z+1), (wx  , wy  , wz+1), world_voxels)
        e = is_void((x  , y+1, z-1), (wx  , wy+1, wz-1), world_voxels)
        f = is_void((x  , y+1, z  ), (wx  , wy+1, wz  ), world_voxels)
        g = is_void((x  , y+1, z+1), (wx  , wy+1, wz+1), world_voxels)
        h = is_void((x  , y  , z+1), (wx  , wy  , wz+1), world_voxels)

    else:
        a = is_void((x-1, y-1, z  ), (wx-1, wy-1, wz  ), world_voxels)
        b = is_void((x  , y-1, z  ), (wx  , wy-1, wz  ), world_voxels)
        c = is_void((x+1, y-1, z  ), (wx+1, wy-1, wz  ), world_voxels)
        d = is_void((x+1, y  , z  ), (wx+1, wy  , wz  ), world_voxels)
        e = is_void((x+1, y+1, z  ), (wx+1, wy+1, wz  ), world_voxels)
        f = is_void((x  , y+1, z  ), (wx  , wy+1, wz  ), world_voxels)
        g = is_void((x-1, y+1, z  ), (wx-1, wy+1, wz  ), world_voxels)
        h = is_void((x-1, y  , z  ), (wx-1, wy  , wz  ), world_voxels)

    return (a+b+h, b+c+d, d+e+f, f+g+h)


@njit
def get_chunk_index(world_position:tuple)->int:
    wx, wy, wz = world_position

    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE

    if(not(0 <= cx < WORLD_W and 0 <= cz < WORLD_W and 0 <= cy < WORLD_H)):
        return -1

    return cx + WORLD_W * cz + WORLD_AREA * cy 


@njit
def is_void(local_position:tuple, world_position:tuple, world_voxels:np.ndarray)->bool:

    chunk_index = get_chunk_index(world_position)
    if chunk_index == -1:
        return False

    x, y, z = local_position
    x = x % CHUNK_SIZE
    y = y % CHUNK_SIZE
    z = z % CHUNK_SIZE
    
    return world_voxels[chunk_index][x + CHUNK_SIZE * z + CHUNK_AREA * y] == 0


@njit
def add_data(vertex_data:np.ndarray, index:int, *vertices:tuple)->int:
    """Adds data to vertex_data array and increments index"""
    for vertex in vertices:
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index


@njit
def build_chunk_mesh(chunk_voxels:np.ndarray, format_size:int, chunk_position:tuple, world_voxels:np.ndarray) -> np.ndarray:
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype='uint8')
    cx, cy, cz = chunk_position
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):

                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]

                if voxel_id == 0:
                    continue
    
                wx = cx * CHUNK_SIZE + x
                wy = cy * CHUNK_SIZE + y
                wz = cz * CHUNK_SIZE + z

                if is_void((x, y+1, z), (wx, wy+1, wz), world_voxels):
                    ao_values = get_ao((x, y+1, z), (wx, wy+1, wz), world_voxels, 'Y')
                    v0 = to_uint8(x  , y+1, z+1, voxel_id, 0, ao_values[0])
                    v1 = to_uint8(x+1, y+1, z+1, voxel_id, 0, ao_values[1])
                    v2 = to_uint8(x+1, y+1, z  , voxel_id, 0, ao_values[2])
                    v3 = to_uint8(x  , y+1, z  , voxel_id, 0, ao_values[3])

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                if is_void((x, y-1, z), (wx, wy-1, wz), world_voxels):
                    ao_values = get_ao((x, y+1, z), (wx, wy+1, wz), world_voxels, 'Y')
                    v0 = to_uint8(x  , y  , z  , voxel_id, 1, ao_values[0])
                    v1 = to_uint8(x+1, y  , z  , voxel_id, 1, ao_values[1])
                    v2 = to_uint8(x+1, y  , z+1, voxel_id, 1, ao_values[2])
                    v3 = to_uint8(x  , y  , z+1, voxel_id, 1, ao_values[3])

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                    
                if is_void((x+1, y, z), (wx+1, wy, wz), world_voxels):
                    ao_values = get_ao((x, y+1, z), (wx, wy+1, wz), world_voxels, 'X')
                    v0 = to_uint8(x+1, y  , z+1, voxel_id, 2, ao_values[0])
                    v1 = to_uint8(x+1, y  , z  , voxel_id, 2, ao_values[1])
                    v2 = to_uint8(x+1, y+1, z  , voxel_id, 2, ao_values[2])
                    v3 = to_uint8(x+1, y+1, z+1, voxel_id, 2, ao_values[3])

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                if is_void((x-1, y, z), (wx-1, wy, wz), world_voxels):
                    ao_values = get_ao((x, y+1, z), (wx, wy+1, wz), world_voxels, 'X')
                    v0 = to_uint8(x  , y  , z  , voxel_id, 3, ao_values[0])
                    v1 = to_uint8(x  , y  , z+1, voxel_id, 3, ao_values[1])
                    v2 = to_uint8(x  , y+1, z+1, voxel_id, 3, ao_values[2])
                    v3 = to_uint8(x  , y+1, z  , voxel_id, 3, ao_values[3])

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                    
                if is_void((x, y, z+1), (wx, wy, wz+1), world_voxels):
                    ao_values = get_ao((x, y+1, z), (wx, wy+1, wz), world_voxels, 'Z')
                    v0 = to_uint8(x  , y  , z+1, voxel_id, 4, ao_values[0])
                    v1 = to_uint8(x+1, y  , z+1, voxel_id, 4, ao_values[1])
                    v2 = to_uint8(x+1, y+1, z+1, voxel_id, 4, ao_values[2])
                    v3 = to_uint8(x  , y+1, z+1, voxel_id, 4, ao_values[3])

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                if is_void((x, y, z-1), (wx, wy, wz-1), world_voxels):
                    ao_values = get_ao((x, y+1, z), (wx, wy+1, wz), world_voxels, 'Z')
                    v0 = to_uint8(x+1, y  , z  , voxel_id, 5, ao_values[0])
                    v1 = to_uint8(x  , y  , z  , voxel_id, 5, ao_values[1])
                    v2 = to_uint8(x  , y+1, z  , voxel_id, 5, ao_values[2])
                    v3 = to_uint8(x+1, y+1, z  , voxel_id, 5, ao_values[3])

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

    print(f'index is {index}')
    return vertex_data[:index+1]
