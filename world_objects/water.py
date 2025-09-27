from settings import *
from meshes.water_mesh import WaterMesh

class Water:
    def __init__(self, world):
        self.world = world
        self.app = world.app


    def build_mesh(self):
        self.mesh = WaterMesh(self)


    def render(self):
        self.app.ctx.disable(mgl.CULL_FACE)
        self.mesh.render()
        self.app.ctx.enable(mgl.CULL_FACE)
