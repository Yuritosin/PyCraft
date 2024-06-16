from settings.common_settings import *


def get_ao(local_pos, world_pos, world_voxels, plane):
    x, y, z = local_pos
    wx, wy, wz = world_pos

    if plane == "Y":
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)
        b = is_void((x - 1, y, z - 1), (wx - 1, wy, wz - 1), world_voxels)
        c = is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels)
        d = is_void((x - 1, y, z + 1), (wx - 1, wy, wz + 1), world_voxels)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)
        f = is_void((x + 1, y, z + 1), (wx + 1, wy, wz + 1), world_voxels)
        g = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)
        h = is_void((x + 1, y, z - 1), (wx + 1, wy, wz - 1), world_voxels)
    elif plane == "X":
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)
        b = is_void((x, y - 1, z - 1), (wx, wy - 1, wz - 1), world_voxels)
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)
        d = is_void((x, y - 1, z + 1), (wx, wy - 1, wz + 1), world_voxels)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)
        f = is_void((x, y + 1, z + 1), (wx, wy + 1, wz + 1), world_voxels)
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels)
        h = is_void((x, y + 1, z - 1), (wx, wy + 1, wz - 1), world_voxels)
    else: # Z Plane
        a = is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels)
        b = is_void((x - 1, y - 1, z), (wx - 1, wy - 1, wz), world_voxels)
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)
        d = is_void((x + 1, y - 1, z), (wx + 1, wy - 1, wz), world_voxels)
        e = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)
        f = is_void((x + 1, y + 1, z), (wx + 1, wy + 1, wz), world_voxels)
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels)
        h = is_void((x - 1, y + 1, z), (wx - 1, wy + 1, wz), world_voxels)

    ao = (a + b + c), (g + h + a), (e + f + g), (c + d + e)
    return ao


def pack_data(x, y, z, voxel_id, face_id, ao_id):
    # 5 + 5 + 8 + 3 + 2 = 10 + 8 + 3 + 2 = 18 + 3 + 2 = 21 + 2 = 21
    y_bit, z_bit, voxel_id_bit, face_id_bit, ao_id_bit = 5, 5, 8, 3, 2

    packet_data = (
        x << (y_bit + z_bit + voxel_id_bit + face_id_bit + ao_id_bit) |
        y << (z_bit + voxel_id_bit + face_id_bit + ao_id_bit) |
        z << (voxel_id_bit + face_id_bit + ao_id_bit) |
        voxel_id << (face_id_bit + ao_id_bit) |
        face_id << ao_id_bit |
        ao_id
    )

    return packet_data


def get_chunk_index(world_voxel_pos):
    wx, wy, wz = world_voxel_pos
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE
    if not (0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D):
        return -1

    index = cx + WORLD_W * cz + WORLD_AREA * cy
    return index


def is_void(local_voxel_pos, world_voxel_pos, world_voxels):
    chunk_index = get_chunk_index(world_voxel_pos)
    if chunk_index == -1:
        return False
    chunk_voxels = world_voxels[chunk_index]

    x, y, z = local_voxel_pos
    voxel_index = x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA

    if chunk_voxels[voxel_index]:
        return False
    return True


def add_data(vertex_data, index, *vertices):
    for vertex in vertices:
        vertex_data[index] = vertex
        index += 1
    return index


def build_chunk_mesh(chunk_voxels, format_size, chunk_pos, world_voxels):
    vertex_data = numpy.empty(CHUNK_VOLUME * 18 * format_size, dtype="uint32")
    index = 0

    for x in range(CHUNK_SIZE):
        for z in range(CHUNK_SIZE):
            for y in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                if not voxel_id:
                    continue

                cx, cy, cz = chunk_pos
                wx = x + cx * CHUNK_SIZE
                wy = y + cy * CHUNK_SIZE
                wz = z + cz * CHUNK_SIZE

                # Top Face
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
                    ao = get_ao((x, y + 1, z), (wx, wy + 1, wz), world_voxels, plane="Y")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x    , y + 1, z    , voxel_id, 0, ao[0])
                    v1 = pack_data(x + 1, y + 1, z    , voxel_id, 0, ao[1])
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 0, ao[2])
                    v3 = pack_data(x    , y + 1, z + 1, voxel_id, 0, ao[3])

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v0, v3, v1, v3, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)
                # Bottom Face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    ao = get_ao((x, y - 1, z), (wx, wy - 1, wz), world_voxels, plane="Y")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x    , y    , z    , voxel_id, 1, ao[0])
                    v1 = pack_data(x + 1, y    , z    , voxel_id, 1, ao[1])
                    v2 = pack_data(x + 1, y    , z + 1, voxel_id, 1, ao[2])
                    v3 = pack_data(x    , y    , z + 1, voxel_id, 1, ao[3])

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v3, v0, v1, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)
                # Right Face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    ao = get_ao((x + 1, y, z), (wx + 1, wy, wz), world_voxels, plane="X")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x + 1, y    , z    , voxel_id, 2, ao[0])
                    v1 = pack_data(x + 1, y + 1, z    , voxel_id, 2, ao[1])
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 2, ao[2])
                    v3 = pack_data(x + 1, y    , z + 1, voxel_id, 2, ao[3])

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                # Left Face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    ao = get_ao((x - 1, y, z), (wx - 1, wy, wz), world_voxels, plane="X")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x    , y    , z    , voxel_id, 3, ao[0])
                    v1 = pack_data(x    , y + 1, z    , voxel_id, 3, ao[1])
                    v2 = pack_data(x    , y + 1, z + 1, voxel_id, 3, ao[2])
                    v3 = pack_data(x    , y    , z + 1, voxel_id, 3, ao[3])

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)
                # Back Face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    ao = get_ao((x, y, z - 1), (wx, wy, wz - 1), world_voxels, plane="Z")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x    , y    , z    , voxel_id, 4, ao[0])
                    v1 = pack_data(x    , y + 1, z    , voxel_id, 4, ao[1])
                    v2 = pack_data(x + 1, y + 1, z    , voxel_id, 4, ao[2])
                    v3 = pack_data(x + 1, y    , z    , voxel_id, 4, ao[3])

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Front Face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    ao = get_ao((x, y, z + 1), (wx, wy, wz + 1), world_voxels, plane="Z")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x    , y    , z + 1, voxel_id, 5, ao[0])
                    v1 = pack_data(x    , y + 1, z + 1, voxel_id, 5, ao[1])
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 5, ao[2])
                    v3 = pack_data(x + 1, y    , z + 1, voxel_id, 5, ao[3])

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)


    return vertex_data[:index + 1]
