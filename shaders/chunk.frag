#version 330 core

in vec3 voxel_color;
in vec2 uv;
in float ao_value;

uniform sampler2D texture_0;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1/gamma;

out vec4 fragColor;

void main() {
	vec3 tex_color = texture(texture_0, uv).rgb;

	tex_color.rgb *= pow(voxel_color * ao_value, inv_gamma);

	fragColor = vec4(tex_color, 1);
}
