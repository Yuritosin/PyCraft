from settings.common_settings import *


class Frustum:
    def __init__(self, camera):
        from camera import Camera
        self.camera: Camera = camera

        self.factor_y = 1.0 / math.cos(half_y := V_FOV * 0.5)
        self.tan_y = math.tan(half_y)

        self.factor_x = 1.0 / math.cos(half_x := H_FOV * 0.5)
        self.tan_x = math.tan(half_x)

    def is_on_frustum(self, chunk):
        # vector to sphere center
        sphere_vector = chunk.center_position - self.camera.position

        # outside the NEAR and FAR planes?
        sz = glm.dot(sphere_vector, self.camera.forward)
        if not (NEAR - CHUNK_SPHERE_RADIUS <= sz <= FAR + CHUNK_SPHERE_RADIUS):
            return False

        # outside the TOP and BOTTOM planes?
        sy = glm.dot(sphere_vector, self.camera.up)
        dist = self.factor_y * CHUNK_SPHERE_RADIUS + sz * self.tan_y
        if not (-dist <= sy <= dist):
            return False

        # outside the LEFT and RIGHT planes?
        sx = glm.dot(sphere_vector, self.camera.right)
        dist = self.factor_x * CHUNK_SPHERE_RADIUS + sz * self.tan_x
        if not (-dist <= sx <= dist):
            return False

        return True
