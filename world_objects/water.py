from settings import *
from meshes.water_mesh import WaterMesh

class Water:
    def __init__(self, world):
        self.world = world
        self.app = world.app


    def build_mesh(self):
        self.mesh = WaterMesh(self)
