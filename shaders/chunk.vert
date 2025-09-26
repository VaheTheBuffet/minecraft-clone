#version 330 core

layout (location = 0) in uint compressed_data;


uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;


int x, y, z;
int voxel_id;
int face_id;
int ao_id;
int orientation;


flat out int texture_index;
flat out int f_voxel_id;
out vec2 uv;
out float shading;


const float ao_values[4] = float[4](
	0.1, 0.25, 0.5, 1 
);


const vec2 uv_coords[4] = vec2[4](
	vec2(0, 0), vec2(1, 0),
	vec2(1, 1), vec2(0, 1)
);


const int uv_indices[12] = int[12](
	3, 0, 1, 3, 1, 2,
	2, 3, 0, 2, 0, 1
);


const int texture_indices[6] = int[6](
	0, 2, 1, 1, 1, 1
);

const float face_shading[6] = float[6](
	1.0, 0.5,
	0.5, 0.8,
	0.5, 0.8
);


vec3 color_generator(float id) {
	return fract(id * vec3(0.222, 0.512, 0.125));
}


void unpack(uint compressed_data) {
	//(x, y, z, voxel_id,  face_id, ao_id, orientation)
	//(6, 6, 6,        8,        3,     2,           1)

	const uint mask_orientation = 1u;   const uint len_orientation  = 1u;
	const uint mask_ao_id       = 3u;   const uint len_ao_id        = 2u;
	const uint mask_face_id     = 7u;   const uint len_face_id      = 3u;
	const uint mask_voxel_id    = 255u; const uint len_voxel_id     = 8u;
	const uint mask_position    = 63u;  const uint len_position     = 6u;

	orientation = int(compressed_data & mask_orientation); compressed_data >>= len_orientation;
	ao_id       = int(compressed_data & mask_ao_id);       compressed_data >>= len_ao_id;
	face_id     = int(compressed_data & mask_face_id);     compressed_data >>= len_face_id;
	voxel_id    = int(compressed_data & mask_voxel_id);    compressed_data >>= len_voxel_id;
	z           = int(compressed_data & mask_position);    compressed_data >>= len_position;
	y           = int(compressed_data & mask_position);    compressed_data >>= len_position;
	x           = int(compressed_data & mask_position);    compressed_data >>= len_position;
}


void main() {
	unpack(compressed_data);
	
	texture_index = texture_indices[face_id];

	f_voxel_id = voxel_id;
	uv = uv_coords[uv_indices[gl_VertexID % 6 + 6 * orientation]];
	shading = ao_values[ao_id] * face_shading[face_id];
	gl_Position = m_proj * m_view * m_model * vec4(x, y, z, 1.0);
}