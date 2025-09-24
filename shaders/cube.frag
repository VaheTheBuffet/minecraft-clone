#version 330 core

in vec2 uv;
out vec4 fragColor;

uniform sampler2D texture_0;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1/gamma;

void main() {
	vec3 tex_color = texture(texture_0, uv).rgb;
	if(tex_color.x == 0) {
		fragColor = vec4(1,0,0,1);
	}else {
		discard;
	}
}