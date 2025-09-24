from settings import *
from meshes.crosshair_mesh import CrosshairMesh

class Crosshair:

    def __init__(self, app):
        self.app = app
        self.mesh = CrosshairMesh(self)
    
    def render(self):
        self.mesh.render()
    
    def update(self):
        pass