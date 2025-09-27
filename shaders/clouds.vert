#version 330 core

uniform mat4 m_view;
uniform mat4 m_proj;
uniform vec2 center_xz;
uniform float time;

layout (location = 0) in vec3 in_position;

void main() {
    vec2 xz_position = (in_position.xz - center_xz) * 20 + center_xz;
    xz_position += 1000*sin(0.01*time);
    gl_Position = m_proj * m_view * vec4(xz_position.x, in_position.y, xz_position.y, 1);
}