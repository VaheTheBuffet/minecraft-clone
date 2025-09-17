import numpy as np

class BaseMesh:
    __slots__ = ['ctx', 'program', 'vbo_format', 'attrs', 'vao']

    def get_vertex_data(self) -> np.ndarray:
        return np.array([-1])

    def get_vao(self):
        vertex_data = self.get_vertex_data()

        vbo = self.ctx.buffer(vertex_data)
        vao = self.ctx.vertex_array(
            self.program, [(vbo, self.vbo_format, *self.attrs)], skip_errors = True
        )
        return vao

    def render(self):
        self.vao.render()
