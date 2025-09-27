#version 330 core

uniform sampler2D texture_water;

out vec4 fragColor;

void main() {
	vec2 uv = fract(gl_FragCoord.xz);
	vec3 tex_color = texture(texture_water, uv).rgb;
	fragColor = vec4(tex_color, 1.0);
}
