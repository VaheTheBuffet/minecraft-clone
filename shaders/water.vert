#version 330 core

uniform mat4 m_proj;
uniform mat4 m_view;

layout (location = 0) in ivec3 in_position;

out vec2 position;

void main() {
	position = in_position.xz;
	gl_Position = m_proj * m_view * vec4(in_position.x, in_position.y - 0.1, in_position.z, 1.0);
}
