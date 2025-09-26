from settings import *
from world import World
from world_objects.voxel_marker import VoxelMarker
from world_objects.crosshair import Crosshair
from world_objects.clouds import Clouds

class Scene:
    def __init__(self, app):
        self.app = app
        self.world = World(app)
        self.voxel_marker = VoxelMarker(app)
        self.crosshair = Crosshair(app)
        self.clouds = Clouds(app)


    def update(self):
        self.world.update()
        self.voxel_marker.update()
        self.clouds.update()


    def render(self):
        self.voxel_marker.render()
        self.world.render()
        self.crosshair.render()
        self.clouds.render()
    

    def log_data(self):
        self.voxel_marker.log_data()
