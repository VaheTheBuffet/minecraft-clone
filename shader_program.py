from settings import *


class ShaderProgram:

    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.player = app.player
        self.chunk = self.get_program(shader_name='chunk')
        self.voxel_marker = self.get_program(shader_name='cube')
        self.crosshair = self.get_program(shader_name = 'crosshair')

        self.texture_0 = self.load_texture('frame.png')
        self.texture_0.use(location = 0)

        self.set_uniforms_on_init()


    def set_uniforms_on_init(self):
        self.voxel_marker['m_proj'].write(self.player.m_proj)
        self.voxel_marker['texture_0'] = 0

        self.chunk['m_proj'].write(self.player.m_proj)
        self.chunk['m_model'].write(glm.mat4())
        self.chunk['texture_0'] = 0


    def update(self):
        self.chunk['m_view'].write(self.player.m_view)
        self.voxel_marker['m_view'].write(self.player.m_view)


    def load_texture(self, filename:str):
        pg_texture = pg.image.load('assets/%s' % filename)
        pg_texture = pg.transform.flip(pg_texture, flip_x=False, flip_y=True)

        texture = self.ctx.texture(
                size=pg_texture.get_size(),
                components=4,
                data=pg.image.tostring(pg_texture, 'RGBA', False)
        )
        texture.anisotropy = 16
        texture.build_mipmaps()
        texture.filter = (mgl.NEAREST, mgl.NEAREST)

        return texture


    def get_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
