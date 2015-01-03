# Copyright (c) 2014 Raihan Kibria
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Collisions
"""

cimport fixpoint
cimport fixpoint_coll
cimport fixpoint_2d
cimport entities

cdef int IDX_STATE_COLLISIONS

cdef int FIXP_2 = fixpoint.int2fix(2)

cdef int HASH_SCALE_FACTOR = fixpoint.int2fix(4)

cdef int IDX_COLLISIONDB_ENTITIES = 0
cdef int IDX_COLLISIONDB_HASH_MAP = 1
cdef int IDX_COLLISIONDB_HANDLER_FUNCTION = 2
cdef int IDX_COLLISIONDB_COLLISIONS_LIST = 3

# Values of state[IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES] are lists with these elements
# Key is entity_name
cdef int IDX_COLLISION_SHAPES = 0
cdef int IDX_COLLISION_LAST_POS = 1
cdef int IDX_COLLISION_CACHE = 2
cdef int IDX_COLLISION_IS_TILE = 3

# Values of the IDX_COLLISION_CACHE list
cdef int IDX_COLLISION_CACHE_ABS_SHAPE = 0
cdef int IDX_COLLISION_CACHE_LAST_HASH_POS = 1
cdef int IDX_COLLISION_CACHE_HASH_EXTENT = 2

cpdef initialize(int state_idx, list state):
        """
        TODO
        """
        global IDX_STATE_COLLISIONS
        IDX_STATE_COLLISIONS = state_idx
        state[IDX_STATE_COLLISIONS] = [
                {},
                {},
                None,
                []
                ]

cpdef destroy(list state):
        """
        TODO
        """
        state[IDX_STATE_COLLISIONS] = None

cpdef entity_pos_listener(list state, str entity_name, tuple pos):
        """
        TODO
        """
        cdef dict collision_db = state[IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES]
        cdef list entity_collision_data
        cdef list entity_collision_cache
        cdef tuple cached_hash_extents

        if collision_db.has_key(entity_name):
                collision_db[entity_name][IDX_COLLISION_CACHE][IDX_COLLISION_CACHE_ABS_SHAPE] = None

                entity_collision_data = collision_db[entity_name]
                entity_collision_cache = entity_collision_data[IDX_COLLISION_CACHE]
                cached_hash_extents = entity_collision_cache[IDX_COLLISION_CACHE_HASH_EXTENT]
                entity_collision_cache[IDX_COLLISION_CACHE_HASH_EXTENT] = None

                update_hash(state, entity_name, pos, False)

cpdef set_handler(list state, handler_function):
        """
        TODO
        """
        state[IDX_STATE_COLLISIONS][IDX_COLLISIONDB_HANDLER_FUNCTION] = handler_function

cpdef add_entity(list state, str entity_name, tuple shapes_list):
        """
        TODO
        """
        cdef dict collision_db
        collision_db = state[IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES]
        collision_db[entity_name] = [
                shapes_list,
                None,
                [None, None, None],
                False,
                ]
        update_hash(state, entity_name, entities.get_pos(state, entity_name), False)

cpdef add_tile(list state, str tile_name, int x, int y, tuple shapes_list):
        """
        TODO
        """
        cdef dict collision_db
        collision_db = state[IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES]
        cdef str full_tile_name = "TILE_%s_%d_%d" % (tile_name, fixpoint.fix2int(x), fixpoint.fix2int(y))
        collision_db[full_tile_name] = [
                shapes_list,
                None,
                [None, None, None],
                True,
                ]
        update_hash(state, full_tile_name, (x, y, 0), True)

cpdef delete(list state, str entity_name):
        """
        TODO
        """
        remove_hash_entries(state, entity_name, entities.get_pos(state, entity_name))
        cdef dict collision_db = state[IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES]
        del collision_db[entity_name]

cpdef update_hash(list state, str entity_name, tuple new_pos, int is_tile):
        """
        TODO
        """
        cdef dict collision_db = state[IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES]
        cdef list entity_collision_data = collision_db[entity_name]

        cdef tuple last_pos = entity_collision_data[IDX_COLLISION_LAST_POS]
        if last_pos:
                remove_hash_entries(state, entity_name, last_pos)

        entity_collision_data[IDX_COLLISION_LAST_POS] = new_pos

        cdef tuple entity_lower_left
        cdef tuple entity_upper_right
        entity_lower_left, entity_upper_right = get_hash_area(state, entity_name, new_pos, is_tile)

        entity_collision_data[IDX_COLLISION_CACHE][IDX_COLLISION_CACHE_LAST_HASH_POS] = (entity_lower_left, entity_upper_right)

        cdef dict hash_map = state[IDX_STATE_COLLISIONS][IDX_COLLISIONDB_HASH_MAP]

        cdef int x
        cdef int y
        cdef tuple hash
        for x in xrange(entity_lower_left[0], entity_upper_right[0] + 1):
                for y in xrange(entity_lower_left[1], entity_upper_right[1] + 1):
                        hash = (x, y)
                        if not hash_map.has_key(hash):
                                hash_map[hash] = set()
                        hash_map[hash].add(entity_name)

cpdef tuple get_hash_area(list state, str entity_name, tuple entity_lower_left, int is_tile):
        """
        Returns absolute tile positions of lower left and upper right of area to check
                ["rectangle", x, y, width, height]
                ["circle", x, y, radius]
        """
        cdef int lower_left_x_offset = 0
        cdef int lower_left_y_offset = 0
        cdef int upper_right_x_offset = 0
        cdef int upper_right_y_offset = 0

        cdef dict collision_db = state[IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES]
        cdef list entity_collision_data = collision_db[entity_name]
        cdef list entity_collision_cache = entity_collision_data[IDX_COLLISION_CACHE]
        cdef tuple entity_shapes = entity_collision_data[IDX_COLLISION_SHAPES]
        cdef tuple cached_hash_extents = entity_collision_cache[IDX_COLLISION_CACHE_HASH_EXTENT]

        cdef tuple collision_shape
        cdef int c_x
        cdef int c_y
        cdef int c_r
        cdef int c_ll_x
        cdef int c_ll_y
        cdef int c_ur_x
        cdef int c_ur_y
        cdef int r_x
        cdef int r_y
        cdef int r_w
        cdef int r_h
        cdef tuple pos
        cdef int rot
        cdef int max_extent
        cdef tuple rect_center
        cdef tuple rect_corners
        cdef int rotated_x
        cdef int rotated_y

        cdef int tile_ll_x
        cdef int tile_ll_y
        cdef int tile_ur_x
        cdef int tile_ur_y
        if is_tile:
                # Simplified: always check full tile area
                tile_ll_x = fixpoint.mul(entity_lower_left[0], HASH_SCALE_FACTOR)
                tile_ll_y = fixpoint.mul(entity_lower_left[1], HASH_SCALE_FACTOR)
                tile_ur_x = tile_ll_x + HASH_SCALE_FACTOR
                tile_ur_y = tile_ll_y + HASH_SCALE_FACTOR
                entity_collision_cache[IDX_COLLISION_CACHE_HASH_EXTENT] = (0, 0, HASH_SCALE_FACTOR, HASH_SCALE_FACTOR)
                return ((fixpoint.fix2int(tile_ll_x), fixpoint.fix2int(tile_ll_y),),
                        (fixpoint.fix2int(tile_ur_x), fixpoint.fix2int(tile_ur_y),)
                        )

        if cached_hash_extents:
                lower_left_x_offset, lower_left_y_offset, upper_right_x_offset, upper_right_y_offset = cached_hash_extents
        else:
                for collision_shape in entity_shapes:
                        if collision_shape[0] == "circle":
                                c_x = fixpoint.mul(collision_shape[1], HASH_SCALE_FACTOR)
                                c_y = fixpoint.mul(collision_shape[2], HASH_SCALE_FACTOR)
                                c_r = fixpoint.mul(collision_shape[3], HASH_SCALE_FACTOR)

                                c_ll_x = c_x - c_r
                                c_ll_y = c_y - c_r
                                c_ur_x = c_x + c_r
                                c_ur_y = c_y + c_r

                                if c_ll_x < lower_left_x_offset:
                                        lower_left_x_offset = c_ll_x

                                if c_ll_y < lower_left_y_offset:
                                        lower_left_y_offset = c_ll_y

                                if c_ur_x > upper_right_x_offset:
                                        upper_right_x_offset = c_ur_x

                                if c_ur_y > upper_right_y_offset:
                                        upper_right_y_offset = c_ur_y

                        elif collision_shape[0] == "rectangle":
                                r_x = fixpoint.mul(collision_shape[1], HASH_SCALE_FACTOR)
                                r_y = fixpoint.mul(collision_shape[2], HASH_SCALE_FACTOR)
                                r_w = fixpoint.mul(collision_shape[3], HASH_SCALE_FACTOR)
                                r_h = fixpoint.mul(collision_shape[4], HASH_SCALE_FACTOR)
                                pos = entities.get_pos(state, entity_name)
                                rot = pos[2]

                                rect_center = (r_x + fixpoint.div(r_w, FIXP_2), r_y + fixpoint.div(r_h, FIXP_2))
                                rect_corners = ((r_x, r_y),
                                                (r_x + r_w, r_y),
                                                (r_x, r_y + r_h),
                                                (r_x + r_w, r_y + r_h),
                                                )
                                for rect_corner in rect_corners:
                                        rotated_x,rotated_y = fixpoint_2d.rotated_point(rect_center, rect_corner, rot)
                                        if rotated_x < lower_left_x_offset:
                                                lower_left_x_offset = rotated_x

                                        if rotated_y < lower_left_y_offset:
                                                lower_left_y_offset = rotated_y

                                        if rotated_x > upper_right_x_offset:
                                                upper_right_x_offset = rotated_x

                                        if rotated_y > upper_right_y_offset:
                                                upper_right_y_offset = rotated_y
                entity_collision_cache[IDX_COLLISION_CACHE_HASH_EXTENT] = (lower_left_x_offset, lower_left_y_offset,
                                                                           upper_right_x_offset, upper_right_y_offset)

        entity_lower_left = (fixpoint.mul(entity_lower_left[0], HASH_SCALE_FACTOR), fixpoint.mul(entity_lower_left[1], HASH_SCALE_FACTOR))

        cdef tuple area_lower_left
        area_lower_left = (entity_lower_left[0] + lower_left_x_offset,
                entity_lower_left[1] + lower_left_y_offset)

        cdef tuple area_upper_right
        area_upper_right = (entity_lower_left[0] + upper_right_x_offset,
                entity_lower_left[1] + upper_right_y_offset)

        area_lower_left = (fixpoint.fix2int(fixpoint.floor(area_lower_left[0])), fixpoint.fix2int(fixpoint.floor(area_lower_left[1])))
        area_upper_right = (fixpoint.fix2int(fixpoint.floor(area_upper_right[0])), fixpoint.fix2int(fixpoint.floor(area_upper_right[1])))
        return (area_lower_left, area_upper_right)

cpdef remove_hash_entries(list state, str entity_name, tuple entity_lower_left):
        """
        TODO
        """
        cdef dict collision_db = state[IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES]
        cdef list entity_collision_data = collision_db[entity_name]
        cdef list collision_cache = entity_collision_data[IDX_COLLISION_CACHE]
        cdef tuple last_added_range = collision_cache[IDX_COLLISION_CACHE_LAST_HASH_POS]
        cdef int is_tile = entity_collision_data[IDX_COLLISION_IS_TILE]

        cdef tuple entity_upper_right
        if last_added_range:
                entity_lower_left, entity_upper_right = last_added_range
        else:
                entity_lower_left, entity_upper_right = get_hash_area(state, entity_name, entity_lower_left, is_tile)

        cdef dict hash_map = state[IDX_STATE_COLLISIONS][IDX_COLLISIONDB_HASH_MAP]
        cdef int x
        cdef int y
        for x in xrange(entity_lower_left[0], entity_upper_right[0] + 1):
                for y in xrange(entity_lower_left[1], entity_upper_right[1] + 1):
                        hash_map[(x, y)].remove(entity_name)
        collision_cache[IDX_COLLISION_CACHE_LAST_HASH_POS] = None

cpdef list get_collision_shapes(list state, str entity_name, list collision_def):
        """
        Get the absolute shapes taking into account position and rotation

        collision_shape:
                ["rectangle", x, y, width, height]
                ["circle", x, y, radius]
        =>
                circle: ("circle", center_x, center_y, radius)
                rectangle: ("rectangle", x, y, w, h, rotation)
        """
        cdef list entity_collision_cache = collision_def[IDX_COLLISION_CACHE]

        cdef list cached_absolute_shapes = entity_collision_cache[IDX_COLLISION_CACHE_ABS_SHAPE]
        if cached_absolute_shapes:
                return cached_absolute_shapes

        cdef tuple pos
        cdef tuple pos_offset
        cdef int is_tile = collision_def[IDX_COLLISION_IS_TILE]
        if is_tile:
                pos = collision_def[IDX_COLLISION_LAST_POS]
                pos_offset = (0, 0)
        else:
                pos = entities.get_pos(state, entity_name)
                pos_offset = entities.get_pos_offset(state, entity_name)

        cdef int rot
        rot = pos[2]
        cdef list absolute_shapes = []

        cdef tuple collision_shape
        for collision_shape in collision_def[IDX_COLLISION_SHAPES]:
                if collision_shape[0] == "circle":
                        c_x = collision_shape[1]
                        c_y = collision_shape[2]
                        c_r = collision_shape[3]
                        absolute_shapes.append(("circle", pos[0] + pos_offset[0] + c_x, pos[1] + pos_offset[1] + c_y, c_r))
                elif collision_shape[0] == "rectangle":
                        r_x = collision_shape[1]
                        r_y = collision_shape[2]
                        r_w = collision_shape[3]
                        r_h = collision_shape[4]
                        absolute_shapes.append(("rectangle", pos[0] + pos_offset[0] + r_x, pos[1] + pos_offset[1] + r_y, r_w, r_h, rot))

        entity_collision_cache[0] = absolute_shapes

        return absolute_shapes

cpdef tuple run(list state, str entity_name_1):
        """
        TODO
        """
        if not entities.is_enabled(state, entity_name_1):
                return

        cdef list state_collisions = state[IDX_STATE_COLLISIONS]

        cdef dict state_collisions_entities = state_collisions[IDX_COLLISIONDB_ENTITIES]
        if not state_collisions_entities.has_key(entity_name_1):
                return

        cdef dict hash_map = state_collisions[IDX_COLLISIONDB_HASH_MAP]

        cdef list collision_def_1 = state_collisions_entities[entity_name_1]
        cdef list absolute_shapes_1 = get_collision_shapes(state, entity_name_1, collision_def_1)
        cdef int is_tile_1 = collision_def_1[IDX_COLLISION_IS_TILE]

        cdef tuple entity_1_lower_left
        cdef tuple entity_1_upper_right
        entity_1_lower_left, entity_1_upper_right = get_hash_area(state, entity_name_1,
                                                                  entities.get_pos(state, entity_name_1),
                                                                  is_tile_1)

        cdef set already_checked_set = set()

        cdef list collisions_list = state[IDX_STATE_COLLISIONS][IDX_COLLISIONDB_COLLISIONS_LIST]

        cdef int is_collision
        cdef tuple hash
        cdef set collision_candidates
        cdef str entity_name_2
        cdef list collision_def_2
        cdef list absolute_shapes_2
        cdef list contact_points = []
        cdef int is_tile_2

        for x in xrange(entity_1_lower_left[0], entity_1_upper_right[0] + 1):
                for y in xrange(entity_1_lower_left[1], entity_1_upper_right[1] + 1):
                        hash = (x, y)
                        if not hash_map.has_key(hash):
                                continue

                        collision_candidates = hash_map[hash]

                        for entity_name_2 in collision_candidates:
                                if entity_name_1 == entity_name_2:
                                        continue

                                if entity_name_2 in already_checked_set:
                                        continue

                                already_checked_set.add(entity_name_2)

                                collision_def_2 = state_collisions_entities[entity_name_2]
                                absolute_shapes_2 = get_collision_shapes(state, entity_name_2, collision_def_2)

                                is_tile_2 = collision_def_2[IDX_COLLISION_IS_TILE]
                                if not is_tile_2 and not entities.is_enabled(state, entity_name_2):
                                        continue

                                for absolute_shape_1 in absolute_shapes_1:
                                        for absolute_shape_2 in absolute_shapes_2:
                                                is_collision = False
                                                absolute_shape_1_type = absolute_shape_1[0]
                                                absolute_shape_2_type = absolute_shape_2[0]

                                                del contact_points[:]
                                                if absolute_shape_1_type == "circle":
                                                        if absolute_shape_2_type == "circle":
                                                                is_collision = fixpoint_coll.is_circle_circle_collision(absolute_shape_1, absolute_shape_2, contact_points)
                                                        elif absolute_shape_2_type == "rectangle":
                                                                is_collision = fixpoint_coll.is_rect_circle_collision(absolute_shape_1, absolute_shape_2, contact_points)
                                                elif absolute_shape_1_type == "rectangle":
                                                        if absolute_shape_2_type == "circle":
                                                                is_collision = fixpoint_coll.is_rect_circle_collision(absolute_shape_2, absolute_shape_1, contact_points)
                                                        elif absolute_shape_2_type == "rectangle":
                                                                is_collision = fixpoint_coll.is_rect_rect_collision(absolute_shape_1, absolute_shape_2, contact_points)

                                                if is_collision:
                                                        if entity_name_1 < entity_name_2:
                                                                collisions_list.append((entity_name_1, entity_name_2,))
                                                        else:
                                                                collisions_list.append((entity_name_2, entity_name_1,))
                                                        return (state,
                                                                entity_name_1, entity_name_2,
                                                                collision_def_1, collision_def_2,
                                                                absolute_shape_1, absolute_shape_2,
                                                                contact_points
                                                                )
        return None

cpdef clear_collisions_list(list state):
        """
        TODO
        """
        state[IDX_STATE_COLLISIONS][IDX_COLLISIONDB_COLLISIONS_LIST] = []

cpdef notify_collision_handler(list state):
        """
        TODO
        """
        cdef list collisions_list = state[IDX_STATE_COLLISIONS][IDX_COLLISIONDB_COLLISIONS_LIST]

        handler_function = state[IDX_STATE_COLLISIONS][IDX_COLLISIONDB_HANDLER_FUNCTION]
        if collisions_list and handler_function:
                (handler_function)(state, collisions_list)
