#version 330 core

layout (location = 0) in vec3 in_position;

layout (std140) uniform FaceIdBuffer {
	int data[6];
};

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 color;

void main() {
	int face_id = int(data[gl_InstanceID]);

	vec3 rotated_position = in_position;
	color = vec3(1,0,0);
	if(face_id == 1) {
		rotated_position = vec3(in_position.x, 0, 1-in_position.z);
		color = vec3(0,1,0);
	} else if(face_id == 2) {
		rotated_position = vec3(in_position.y, 1-in_position.z, 1-in_position.x);
		color = vec3(0,0,1);
	} else if(face_id == 3) {
		rotated_position = vec3(1-in_position.y, 1-in_position.z, in_position.x);
		color = vec3(0,0,0);
	} else if(face_id == 4) {
		rotated_position = vec3(in_position.x, 1-in_position.z, in_position.y);
		color = vec3(1,1,1);
	} else if(face_id == 5) {
		rotated_position = vec3(1-in_position.x, 1-in_position.z, 1-in_position.y);
		color = vec3(0.5,0.5,0.5);
	}

	 gl_Position = m_proj * m_view * m_model * vec4(rotated_position, 1.0);
}