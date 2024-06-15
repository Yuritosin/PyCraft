#version 400 core

layout (location = 0) out vec4 fragColor;

in float shading;
in vec3 voxelColor;

void main() {
    vec3 resultColor = voxelColor;

    resultColor.r *= shading;
    resultColor.g *= shading;
    resultColor.b *= shading;

    fragColor = vec4(resultColor, 1.0);
}