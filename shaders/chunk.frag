#version 330 core

in vec2 uv;
in float shading;
in vec3 f_position;
flat in int texture_index;
flat in int f_voxel_id;
flat in int f_face_id;

uniform sampler2DArray texture_array_0;
uniform vec3 bg_color;
uniform int underwater;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1/gamma;

out vec4 fragColor;


const vec3 normals[6] = vec3[6](
	vec3(0,1,0), vec3(0,-1,0),
	vec3(1,0,0), vec3(-1,0,0),
	vec3(0,0,1), vec3(0,0,-1)
);


const vec3 water_factor[2] = vec3[2] (
	vec3(1, 1, 1), vec3(0, 0.3, 1.0)
);


const vec3 lightColor = vec3(0.9, 0.9, 0.9);
const vec3 lightPos = vec3(100, 200, 100);


void main() {
	vec2 face_uv = uv;
	face_uv.x += texture_index;
	face_uv.x /= 3;

	vec3 norm = normals[f_face_id];
	vec3 lightDir = normalize(lightPos - f_position);
	float diff = max(dot(norm, lightDir), 0.2);
	vec3 diffuse = diff * lightColor;

	float fog_dist = gl_FragCoord.z / gl_FragCoord.w;

	vec3 tex_color = texture(texture_array_0, vec3(face_uv, f_voxel_id)).rgb;
	tex_color = pow(tex_color, gamma);

	//tex_color *= shading;
	tex_color *= diffuse;
	tex_color = mix(tex_color, bg_color, (1.0-exp2(-0.00001 * fog_dist * fog_dist)));
	tex_color *= water_factor[underwater];
	
	tex_color = pow(tex_color, inv_gamma);
	fragColor = vec4(tex_color, 1.0);
//	fragColor = fract(vec4((f_face_id+1) * 5.33, (f_face_id+1) * 9.25, (f_face_id+1) * 4.121, 0));
//	fragColor.a = 1.0;
}
