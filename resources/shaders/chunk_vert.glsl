#version 400 core

layout (location = 0) in uint packedData;
int x, y, z;
int voxel_id;
int face_id;
int ao_id;

void unpack(uint packedData) {
    uint y_bit = 5u, z_bit = 5u, voxel_id_bit = 8u, face_id_bit = 3u, ao_id_bit = 2u;
    uint y_mask = 31u, z_mask = 31u, voxel_id_mask = 255u, face_id_mask = 7u, ao_id_mask = 3u;

    x = int(packedData >> (y_bit + z_bit + voxel_id_bit + face_id_bit + ao_id_bit));
    y = int((packedData >> (z_bit + voxel_id_bit + face_id_bit + ao_id_bit)) & y_mask);
    z = int((packedData >> (voxel_id_bit + face_id_bit + ao_id_bit)) & z_mask);

    voxel_id = int((packedData >> (face_id_bit + ao_id_bit)) & voxel_id_mask);
    face_id = int((packedData >> (ao_id_bit)) & face_id_mask);
    ao_id = int(packedData & (ao_id_mask));
}

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

const float face_shading[6] = float[6](
    1.0, 0.5, // Top Bottom
    0.5, 0.8, // Right Left
    0.5, 0.8  // Front Back
);

const float ao_values[4] = float[4](0.1, 0.25, 0.5, 1.0);

/*const vec3 voxel_colors[7] = vec3[7](
    vec3(0.8),
    vec3(0.4),
    vec3(0.7, 0.7, 0.25),
    vec3(0.25, 0.7, 0.25),
    vec3(0.7, 0.25, 0.25),
    vec3(0.25, 0.25, 0.7),
    vec3(0.43, 0.56, 0.44)
);*/

const vec3 voxel_colors[6] = vec3[6](
    vec3(1.0, 0.0, 0.0),
    vec3(0.5, 0.5, 0.5),
    vec3(0.0, 1.0, 0.0),
    vec3(0.0, 0.0, 1.0),
    vec3(0.5, 0.5, 1.0),
    vec3(1.0, 1.0, 1.0)
);

out float shading;
out vec3 voxelColor;

void main() {
    unpack(packedData);

    vec3 in_position = vec3(x, y, z);

    voxelColor = voxel_colors[voxel_id % 6];
    shading = face_shading[face_id] * ao_values[ao_id];
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}