from settings import *
from world import World
from world_objects.voxel_marker import VoxelMarker

class Scene:
    def __init__(self, app):
        self.app = app
        self.world = World(app)
        self.voxel_marker = VoxelMarker(app)


    def update(self):
        self.world.update()
        self.voxel_marker.update()


    def render(self):
        self.voxel_marker.render()
        self.world.render()
    

    def log_data(self):
        self.voxel_marker.log_data()
    
