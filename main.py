import moderngl as mgl
import pygame as pg
import shader_program
import scene
import player
import sys
import sys
import ray_caster
from numba.experimental import jitclass
from settings import *


class VoxelEngine:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, MAJOR_VER)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, MINOR_VER)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, DEPTH_SIZE)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, NUM_SAMPLES)


        pg.display.set_mode(tuple(WIN_RES), flags = pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()
        self.ctx.gc_mode = 'auto'
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)

        #self.ctx.wireframe = True

        print(self.ctx.viewport)

        self.clock  = pg.time.Clock()
        self.delta_time = 0
        self.time = 0

        self.is_running = True
        self.on_init()

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)


    def on_init(self):
        self.player = player.Player(self)
        self.shader_program = shader_program.ShaderProgram(self)
        self.scene = scene.Scene(self)
        

    def update(self): 
        self.shader_program.update()
        self.scene.update()
        self.player.update()

        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        pg.display.set_caption(f'{self.clock.get_fps() :.0f}')


    def render(self):
        self.ctx.clear(BG_COLOR.x, BG_COLOR.y, BG_COLOR.z)
        self.scene.render()
        pg.display.flip()


    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False
            self.player.handle_events(event)

            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.log_data()


    def log_data(self):
        self.scene.log_data()
        self.player.log_data()


    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()

        pg.quit()
        sys.exit()


if __name__ == "__main__":
    app = VoxelEngine()
    app.run()
