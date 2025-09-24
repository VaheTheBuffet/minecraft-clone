#version 330 core

layout (location = 0) in uint compressed_data;

int x, y, z;
int voxel_id;
int uv_index;
int ao_id;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 voxel_color;
out vec2 uv;
out float ao_value;

const float ao_values[4] = float[4](
	0.1, 0.25, 0.5, 1 
);

const vec2 uv_coords[4] = vec2[4](
	vec2(0, 0), vec2(1, 0),
	vec2(1, 1), vec2(0, 1)
);

const int uv_indices[6] = int[6](
	0, 2, 3, 0, 3, 1
);

vec3 color_generator(float id) {
	return fract(id * vec3(0.222, 0.512, 0.125));

}

void unpack(uint compressed_data) {
	//(x, y, z, voxel_id, uv_index, ao_id)
	//(6, 6, 6,        8,        2,     2)

	const uint mask_ao_id    = 3u;   const uint len_ao_id    = 2u;
	const uint mask_uv_index = 3u;   const uint len_uv_index = 2u;
	const uint mask_voxel_id = 255u; const uint len_voxel_id = 8u;
	const uint mask_position = 63u;  const uint len_position = 6u;

	ao_id    = int(compressed_data & mask_ao_id);    compressed_data >>= len_ao_id;
	uv_index = int(compressed_data & mask_uv_index); compressed_data >>= len_uv_index;
	voxel_id = int(compressed_data & mask_voxel_id); compressed_data >>= len_voxel_id;
	z        = int(compressed_data & mask_position); compressed_data >>= len_position;
	y        = int(compressed_data & mask_position); compressed_data >>= len_position;
	x        = int(compressed_data & mask_position); compressed_data >>= len_position;
}

void main() {
	//int uv_index = gl_VertexID % 6;
	unpack(compressed_data);
	uv = uv_coords[uv_index];
	ao_value = ao_values[ao_id];
	voxel_color = color_generator(voxel_id);
	gl_Position = m_proj * m_view * m_model * vec4(x, y, z, 1.0);
}
