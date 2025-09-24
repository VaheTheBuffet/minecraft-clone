from settings import *
from meshes.cube_mesh import CubeMesh

class VoxelMarker:
    def __init__(self, app):
        self.app = app
        self.position = glm.vec3(0,0,-5)
        self.ray_caster = app.ray_caster
        self.visible = False

        self.mesh = CubeMesh(self)
        self.set_uniforms()
    

    def set_uniforms(self):
        self.mesh.program['m_model'].write(
            glm.translate(glm.mat4(), glm.vec3(self.position)) #pyright: ignore
        )


    def update(self):
        if self.ray_caster.voxel_id != 0:
            self.position = self.ray_caster.voxel_world_pos
            self.set_uniforms()
            self.visible = True
            return
        self.visible = False


    def render(self):
        if self.visible:
            self.mesh.render()


    def log_data(self):
        print(f'voxel marker position {self.position}')