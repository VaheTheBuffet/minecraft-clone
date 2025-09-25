#version 330 core

in vec2 uv;
in float ao_value;
flat in int texture_index;
flat in int f_voxel_id;

uniform sampler2DArray texture_array_0;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1/gamma;

out vec4 fragColor;

void main() {
	vec2 face_uv = uv;
	face_uv.x += texture_index;
	face_uv.x /= 3;

	vec3 tex_color = texture(texture_array_0, vec3(face_uv, f_voxel_id)).rgb;

	pow(tex_color, gamma);
	tex_color.rgb *= ao_value;
	pow(tex_color, inv_gamma);

	fragColor = vec4(tex_color, 1);
}
