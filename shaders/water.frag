#version 330 core

uniform sampler2D texture_water;
uniform vec3 bg_color;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1/gamma;

in vec2 position;

out vec4 fragColor;

void main() {
	float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
	vec2 uv = vec2(fract(position.x), 1-fract(position.y));
	vec3 tex_color = texture(texture_water, uv).rgb;
	tex_color = pow(tex_color, gamma);

	tex_color = mix(tex_color, bg_color, (1.0-exp2(-0.00001 * fog_dist * fog_dist)));

	tex_color = pow(tex_color, inv_gamma);
	fragColor = vec4(tex_color, 0.8);
}
