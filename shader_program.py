from settings import *


class ShaderProgram:

    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.player = app.player

        self.chunk = self.get_program(shader_name='chunk')
        self.voxel_marker = self.get_program(shader_name='cube')
        self.crosshair = self.get_program(shader_name = 'crosshair')
        self.water = self.get_program(shader_name = 'water')

        self.texture_0 = self.load_texture('frame.png', False)
        self.texture_0.use(location = 0)

        self.texture_array_0 = self.load_texture('tex_array_0.png', True)
        self.texture_array_0.use(location = 1)

        self.texture_water = self.load_texture('water.png', False)
        self.texture_water.use(location = 2)

        self.clouds = self.get_program(shader_name='clouds')

        self.quad = self.get_program(shader_name='quad')


        self.set_uniforms_on_init()


    def set_uniforms_on_init(self):
        self.voxel_marker['m_proj'].write(self.player.m_proj)
        self.voxel_marker['texture_0'] = 0

        self.chunk['m_proj'].write(self.player.m_proj)
        self.chunk['m_model'].write(glm.mat4())
        self.chunk['texture_array_0'] = 1
        self.chunk['bg_color'].write(BG_COLOR)

        self.clouds['m_proj'].write(self.player.m_proj)
        self.clouds['center_xz'].write(glm.vec2(WORLD_CENTER_XZ, WORLD_CENTER_XZ))
        
        self.water['m_proj'].write(self.player.m_proj)
        self.water['texture_water'] = 2

        self.quad['m_proj'].write(self.player.m_proj)
        self.quad['m_model'].write(glm.mat4())


    def update(self):
        self.chunk['m_view'].write(self.player.m_view)
        self.voxel_marker['m_view'].write(self.player.m_view)
        self.clouds['m_view'].write(self.player.m_view)
        self.water['m_view'].write(self.player.m_view)
        self.quad['m_view'].write(self.player.m_view)


    def load_texture(self, filename:str, is_array:bool):
        pg_texture = pg.image.load('assets/%s' % filename)
        pg_texture = pg.transform.flip(pg_texture, flip_x=True, flip_y=False)

        if is_array:
            n_layers = 3 * pg_texture.get_height() // pg_texture.get_width()
            texture = self.ctx.texture_array(
                size = (pg_texture.get_width(), pg_texture.get_height() // n_layers, n_layers),
                components = 4,
                data=pg.image.tostring(pg_texture, 'RGBA', False)
            )
        else:
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
