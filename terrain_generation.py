from noise import noise2, noise3
from random import random
from settings import *
from numba import njit #pyright: ignore


@njit
def get_height(x, y):
    a1 = WORLD_CENTER_Y
    a2, a4, a8 = a1 * 0.5, a1 * 0.25, a1 * 0.125

    f1 = 0.005
    f2, f4, f8 = f1 * 2, f1 * 4, f1 * 8

    height = 0

    if noise2(x/10, y/10) < 0:
        a1 /= 1.07

    height += noise2(x*f1, y*f1) * a1 + a1
    height += noise2(x*f2, y*f2) * a2 - a2
    height += noise2(x*f4, y*f4) * a4 + a4
    height += noise2(x*f8, y*f8) * a8 - a8

    island_mask = 1 / (math.hypot(x-WORLD_CENTER_XZ, y-WORLD_CENTER_XZ)/250 + 0.0001) ** 20
    island_mask = min(island_mask, 1)

    height = max(height, 1)
    height *= island_mask
    return int(height)


@njit
def get_index(x, y, z):
    return x + CHUNK_SIZE * z + CHUNK_AREA * y


@njit
def set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height):
    voxel_id = 0
    if voxels[get_index(x, y, z)] != 0:
        return

    if world_height - 5 < wy < world_height - 1:
        voxel_id = DIRT
    elif wy <= world_height - 5:
        #cave
        if (noise3(wx * 0.1, wy * 0.1, wz * 0.1) > 0 and
                noise2(wx * 0.1, wz * 0.1) * 3 + 3 < wy < world_height -10):
            voxel_id = 0
        else:
            voxel_id = STONE
    else:
        rng = int(7 * random())
        ry = wy - rng

        if SNOW_LEVEL <= ry <world_height:
            voxel_id = SNOW
        elif STONE_LEVEL <= ry < SNOW_LEVEL:
            voxel_id = STONE
        elif GRASS_LEVEL <= ry < STONE_LEVEL:
            voxel_id = GRASS
        else:
            voxel_id = SAND
    
    voxels[get_index(x, y, z)] = voxel_id

    if wy < STONE_LEVEL:
        place_tree(voxels, x, y, z, voxel_id)
    
    if wy < WATER_LEVEL:
        generate_water_body(voxels, x, y, z, voxel_id)


@njit
def place_tree(voxels, x, y, z, voxel_id):
    if voxel_id != GRASS or random() > TREE_PROBABILITY:
        return

    if y >= CHUNK_SIZE - TREE_HEIGHT:
        return
    if x >= CHUNK_SIZE - MAX_TREE_WIDTH or x < MAX_TREE_WIDTH:
        return 
    if z >= CHUNK_SIZE - MAX_TREE_WIDTH or z < MAX_TREE_WIDTH:
        return

    for i in range(1, 4):
        voxels[get_index(x,y+i,z)] = WOOD
    
    for yt in range(y+4, y+TREE_HEIGHT):
        for xt in range(x-MIN_TREE_WIDTH-TREE_WIDTH_RANGE*random(),x+MIN_TREE_WIDTH+TREE_WIDTH_RANGE*random()):
            for zt in range(z-MIN_TREE_WIDTH-TREE_WIDTH_RANGE*random(),z+MIN_TREE_WIDTH+TREE_WIDTH_RANGE*random()):
                voxels[get_index(xt,yt,zt)] = LEAVES


@njit
def generate_water_body(voxels, x, y, z, voxel_id):
    if voxel_id != SAND:
        return
    if y >= CHUNK_SIZE - WATER_LEVEL:
        return
    for yi in range(y+1, WATER_LEVEL + 1):
        voxels[get_index(x,yi,z)] = WATER
    #voxels[get_index(x,WATER_LEVEL,z)] = WATER

