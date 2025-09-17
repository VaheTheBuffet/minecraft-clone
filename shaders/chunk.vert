#version 330 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in int voxel_id;
layout (location = 2) in int face_id;
layout (location = 3) in int ao_id;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 voxel_color;
out vec2 uv;
out float ao_value;

const float ao_values[4] = float[4](
	0.05, 0.1, 0.2, 1 
);

const vec2 uv_coords[4] = vec2[4](
	vec2(0, 0), vec2(0, 1),
	vec2(1, 0), vec2(1, 1)
);

const int uv_indices[6] = int[6](
	0, 2, 3, 0, 3, 1
);

vec3 color_generator(float id) {
	return fract(id * vec3(0.222, 0.512, 0.125));

}

void main() {
	int uv_index = gl_VertexID % 6;
	uv = uv_coords[uv_indices[uv_index]];
	ao_value = ao_values[ao_id];
	voxel_color = vec3(0.99,0.99,0.99);//color_generator(voxel_id);
	gl_Position = m_proj * m_view * m_model * vec4(in_position.xyz, 1.0);
}
