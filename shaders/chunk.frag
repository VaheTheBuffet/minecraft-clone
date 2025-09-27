#version 330 core

in vec2 uv;
in float shading;
flat in int texture_index;
flat in int f_voxel_id;

uniform sampler2DArray texture_array_0;
uniform vec3 bg_color;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1/gamma;

out vec4 fragColor;

void main() {
	vec2 face_uv = uv;
	face_uv.x += texture_index;
	face_uv.x /= 3;

	float fog_dist = gl_FragCoord.z / gl_FragCoord.w;

	vec3 tex_color = texture(texture_array_0, vec3(face_uv, f_voxel_id)).rgb;
	tex_color = pow(tex_color, gamma);

	tex_color.rgb *= shading;
	tex_color = mix(tex_color, bg_color, (1.0-exp2(-0.00001 * fog_dist * fog_dist)));
	
	tex_color = pow(tex_color, inv_gamma);
	fragColor = vec4(tex_color, 1.0);
}
