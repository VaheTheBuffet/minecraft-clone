#version 330 core

uniform mat4 m_proj;
uniform mat4 m_view;

layout (location = 0) in vec3 in_position;

void main() {
	gl_Position = m_proj * m_view * vec4(in_position, 1.0);
}
