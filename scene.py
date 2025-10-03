from settings import *
from world import World
from world_objects.crosshair import Crosshair
from world_objects.clouds import Clouds

class Scene:
    def __init__(self, app):
        self.app = app
        self.world = World(app)
        self.crosshair = Crosshair(app)
        self.clouds = Clouds(app)


    def update(self):
        self.world.update()
        self.clouds.update()


    def render(self):
        self.world.render()
        self.crosshair.render()
        self.clouds.render()


    def log_data(self):
        self.world.log_data()
