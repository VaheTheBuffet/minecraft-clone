from settings import *
from meshes.cloud_mesh import CloudMesh

class Clouds:

    def __init__(self, app):
        self.app = app
        self.mesh = CloudMesh(self)
    

    def update(self):
        #self.mesh.program['time'].write(self.app.time)
        pass
    

    def render(self):
        self.mesh.render()