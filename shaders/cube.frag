#version 330 core

in vec2 uv;
out vec4 fragColor;

uniform sampler2D texture_0;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1/gamma;

const float[2] alpha = float[2](
	1.0, 0.0
);

void main() {
	vec3 tex_color = texture(texture_0, uv).rgb;
	fragColor = vec4(0.8, 0.8, 0.8, alpha[int(tex_color.r > 0)]);
}