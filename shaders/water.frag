#version 330 core

uniform sampler2D texture_water;

in vec2 position;

out vec4 fragColor;

void main() {
	vec2 uv = vec2(fract(position.x), 1-fract(position.y));
	vec3 tex_color = texture(texture_water, uv).rgb;
	fragColor = vec4(tex_color, 0.8);
}
