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

import globals
import entities

HASH_SCALE_FACTOR = fixpoint.int2fix(4)

cdef int IDX_COLLISIONDB_ENTITIES
cdef int IDX_COLLISIONDB_HASH_MAP
cdef int IDX_COLLISIONDB_HANDLER_FUNCTION
cdef int IDX_COLLISIONDB_COLLISIONS_LIST
IDX_COLLISIONDB_ENTITIES = 0
IDX_COLLISIONDB_HASH_MAP = 1
IDX_COLLISIONDB_HANDLER_FUNCTION = 2
IDX_COLLISIONDB_COLLISIONS_LIST = 3

cdef int IDX_COLLISION_SHAPES
cdef int IDX_COLLISION_LAST_POS
cdef int IDX_COLLISION_CACHE
IDX_COLLISION_SHAPES = 0
IDX_COLLISION_LAST_POS = 1
IDX_COLLISION_CACHE = 2

cdef int IDX_COLLISION_CACHE_ABS_SHAPE
cdef int IDX_COLLISION_CACHE_HASH_EXTENT
cdef int IDX_COLLISION_CACHE_LAST_HASH_POS
IDX_COLLISION_CACHE_ABS_SHAPE = 0
IDX_COLLISION_CACHE_HASH_EXTENT = 1
IDX_COLLISION_CACHE_LAST_HASH_POS = 2

cpdef initialize(list state):
        """
        TODO
        """
        state[globals.IDX_STATE_COLLISIONS] = [
                {},
                {},
                None,
                []
                ]

cpdef destroy(list state):
        """
        TODO
        """
        state[globals.IDX_STATE_COLLISIONS] = None

cpdef entity_pos_listener(list state, str entity_name, tuple pos):
        """
        TODO
        """
        cdef dict collision_db
        collision_db = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES]
        if collision_db.has_key(entity_name):
                collision_db[entity_name][IDX_COLLISION_CACHE][IDX_COLLISION_CACHE_ABS_SHAPE] = None
                c_update_hash(state, entity_name, pos)

cpdef set_handler(list state, handler_function):
        """
        TODO
        """
        state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_HANDLER_FUNCTION] = handler_function

cpdef add(list state, str entity_name, tuple shapes_list):
        """
        TODO
        """
        cdef list trans_shapes_list
        trans_shapes_list = []
        cdef tuple trans_shape
        for shape in shapes_list:
                trans_shape = ("UNKNOWN",)
                if shape[0] == "rectangle":
                        trans_shape = ("rectangle",
                                shape[1],
                                shape[2],
                                shape[3],
                                shape[4],)
                elif shape[0] == "circle":
                        trans_shape = ("circle",
                                shape[1],
                                shape[2],
                                shape[3],)
                trans_shapes_list.append(trans_shape)

        cdef dict collision_db
        collision_db = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES]
        collision_db[entity_name] = [
                trans_shapes_list,
                None,
                [None, None, None],
                ]

        c_update_hash(state, entity_name, entities.get_pos(state, entity_name))

cpdef delete(list state, str entity_name):
        """
        TODO
        """
        c_remove_hash_entries(state, entity_name, entities.get_pos(state, entity_name))
        cdef dict collision_db
        collision_db = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES]
        del collision_db[entity_name]

cdef void c_update_hash(list state, str entity_name, tuple new_pos):
        """
        TODO
        """
        cdef dict collision_db
        collision_db = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES]

        cdef list entity_collision_data
        entity_collision_data = collision_db[entity_name]

        cdef tuple last_pos
        last_pos = entity_collision_data[IDX_COLLISION_LAST_POS]
        if last_pos:
                c_remove_hash_entries(state, entity_name, last_pos)

        entity_collision_data[IDX_COLLISION_LAST_POS] = new_pos

        cdef tuple entity_lower_left
        cdef tuple entity_upper_right
        entity_lower_left, entity_upper_right = c_get_hash_area(state, entity_name, new_pos)

        entity_collision_data[IDX_COLLISION_CACHE][IDX_COLLISION_CACHE_LAST_HASH_POS] = (entity_lower_left, entity_upper_right)

        cdef dict hash_map
        hash_map = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_HASH_MAP]

        cdef int x
        cdef int y
        cdef tuple hash
        for x in xrange(entity_lower_left[0], entity_upper_right[0] + 1):
                for y in xrange(entity_lower_left[1], entity_upper_right[1] + 1):
                        hash = (x, y)
                        if not hash_map.has_key(hash):
                                hash_map[hash] = set()
                        hash_map[hash].add(entity_name)

cdef tuple c_get_hash_area(list state, str entity_name, tuple entity_lower_left):
        """
        Returns absolute tile positions of lower left and upper right of area to check
                ["rectangle", x, y, width, height]
                ["circle", x, y, radius]
        """
        cdef int FIXP_1_5
        FIXP_1_5 = fixpoint.FIXP_1_5
        cdef int FIXP_2
        FIXP_2 = fixpoint.FIXP_2

        cdef int lower_left_x_offset
        cdef int lower_left_y_offset
        cdef int upper_right_x_offset
        cdef int upper_right_y_offset

        lower_left_x_offset = 0
        lower_left_y_offset = 0
        upper_right_x_offset = 0
        upper_right_y_offset = 0

        cdef dict collision_db
        collision_db = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES]

        cdef list entity_collision_data
        entity_collision_data = collision_db[entity_name]

        cdef list entity_collision_cache
        entity_collision_cache = entity_collision_data[IDX_COLLISION_CACHE]

        cdef tuple cached_hash_extents
        cached_hash_extents = entity_collision_cache[IDX_COLLISION_CACHE_HASH_EXTENT]

        cdef list entity_shapes
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
        if cached_hash_extents:
                lower_left_x_offset, lower_left_y_offset, upper_right_x_offset, upper_right_y_offset = cached_hash_extents
        else:
                entity_shapes = entity_collision_data[IDX_COLLISION_SHAPES]

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

                                if rot == 0:
                                        if r_x < lower_left_x_offset:
                                                lower_left_x_offset = r_x

                                        if r_y < lower_left_y_offset:
                                                lower_left_y_offset = r_y

                                        r_x2 = r_x + r_w
                                        r_y2 = r_y + r_h
                                        if r_x2 > upper_right_x_offset:
                                                upper_right_x_offset = r_x2

                                        if r_y2 > upper_right_y_offset:
                                                upper_right_y_offset = r_y2
                                else:
                                        if r_x != 0 or r_y != 0: # TODO
                                                pass

                                        max_extent = fixpoint.div(fixpoint.negate(max(r_w, r_h)), FIXP_2)

                                        if max_extent < lower_left_x_offset:
                                                lower_left_x_offset = max_extent

                                        if max_extent < lower_left_y_offset:
                                                lower_left_y_offset = max_extent

                                        max_extent = fixpoint.mul(FIXP_1_5, max(r_w, r_h))

                                        if max_extent > upper_right_x_offset:
                                                upper_right_x_offset = max_extent
                                        if max_extent > upper_right_y_offset:
                                                upper_right_y_offset = max_extent
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

cdef void c_remove_hash_entries(list state, str entity_name, tuple entity_lower_left):
        """
        TODO
        """
        cdef list collision_cache
        collision_cache = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES][entity_name][IDX_COLLISION_CACHE]

        cdef tuple last_added_range
        last_added_range = collision_cache[IDX_COLLISION_CACHE_LAST_HASH_POS]

        cdef tuple entity_upper_right
        if last_added_range:
                entity_lower_left, entity_upper_right = last_added_range
        else:
                entity_lower_left, entity_upper_right = c_get_hash_area(state, entity_name, entity_lower_left)

        cdef dict hash_map
        hash_map = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_HASH_MAP]

        cdef int x
        cdef int y
        for x in xrange(entity_lower_left[0], entity_upper_right[0] + 1):
                for y in xrange(entity_lower_left[1], entity_upper_right[1] + 1):
                        hash_map[(x, y)].remove(entity_name)
        collision_cache[IDX_COLLISION_CACHE_LAST_HASH_POS] = None

cdef list c_get_collision_shapes(list state, str entity_name, list collision_def):
        """
        Get the absolute shapes taking into account position and rotation

        collision_shape:
                ["rectangle", x, y, width, height]
                ["circle", x, y, radius]
        =>
                circle: ("circle", center_x, center_y, radius)
                rectangle: ("rectangle", x, y, w, h, rotation)
        """
        cdef list entity_collision_cache
        entity_collision_cache = collision_def[IDX_COLLISION_CACHE]

        cdef list cached_absolute_shapes
        cached_absolute_shapes = entity_collision_cache[IDX_COLLISION_CACHE_ABS_SHAPE]
        if cached_absolute_shapes:
                return cached_absolute_shapes

        cdef tuple pos
        pos = entities.get_pos(state, entity_name)
        
        cdef int rot
        rot = pos[2]

        cdef tuple pos_offset
        pos_offset = entities.get_pos_offset(state, entity_name)

        cdef list absolute_shapes
        absolute_shapes = []

        cdef tuple collision_shape
        for collision_shape in collision_def[IDX_COLLISION_SHAPES]:
                if collision_shape[0] == "circle":
                        c_x = collision_shape[1]
                        c_y = collision_shape[2]
                        c_r = collision_shape[3]
                        absolute_shapes.append(("circle", pos[0] + pos_offset[0] + c_x,
                                pos[1] + pos_offset[1] + c_y, c_r))
                elif collision_shape[0] == "rectangle":
                        r_x = collision_shape[1]
                        r_y = collision_shape[2]
                        r_w = collision_shape[3]
                        r_h = collision_shape[4]
                        absolute_shapes.append(("rectangle", pos[0] + pos_offset[0] + r_x, pos[1] + pos_offset[1] + r_y,
                                r_w, r_h, rot))

        entity_collision_cache[0] = absolute_shapes

        return absolute_shapes

cdef tuple c_run(list state, str entity_name_1):
        """
        TODO
        """
        cdef list state_collisions = state[globals.IDX_STATE_COLLISIONS]

        cdef dict state_collisions_entities = state_collisions[IDX_COLLISIONDB_ENTITIES]
        if not state_collisions_entities.has_key(entity_name_1):
                return

        cdef dict hash_map = state_collisions[IDX_COLLISIONDB_HASH_MAP]

        cdef list collision_def_1 = state_collisions_entities[entity_name_1]
        cdef list absolute_shapes_1 = c_get_collision_shapes(state, entity_name_1, collision_def_1)

        cdef tuple entity_1_lower_left
        cdef tuple entity_1_upper_right
        entity_1_lower_left, entity_1_upper_right = c_get_hash_area(state,
                entity_name_1, entities.get_pos(state, entity_name_1))

        cdef set already_checked_set = set()

        cdef list collisions_list = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_COLLISIONS_LIST]

        cdef int is_collision
        cdef tuple hash
        cdef set collision_candidates
        cdef str entity_name_2
        cdef list collision_def_2
        cdef list absolute_shapes_2
        cdef list contact_points = []

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
                                absolute_shapes_2 = c_get_collision_shapes(state, entity_name_2, collision_def_2)

                                for absolute_shape_1 in absolute_shapes_1:
                                        for absolute_shape_2 in absolute_shapes_2:

                                                is_collision = False
                                                absolute_shape_1_type = absolute_shape_1[0]
                                                absolute_shape_2_type = absolute_shape_2[0]

                                                del contact_points[:]
                                                if absolute_shape_1_type == "circle":
                                                        if absolute_shape_2_type == "circle":
                                                                is_collision = fixpoint.is_circle_circle_collision(absolute_shape_1, absolute_shape_2, contact_points)
                                                        elif absolute_shape_2_type == "rectangle":
                                                                is_collision = fixpoint.is_rect_circle_collision(absolute_shape_1, absolute_shape_2, contact_points)
                                                elif absolute_shape_1_type == "rectangle":
                                                        if absolute_shape_2_type == "circle":
                                                                is_collision = fixpoint.is_rect_circle_collision(absolute_shape_2, absolute_shape_1, contact_points)
                                                        elif absolute_shape_2_type == "rectangle":
                                                                is_collision = fixpoint.is_rect_rect_collision(absolute_shape_1, absolute_shape_2, contact_points)

                                                if is_collision:
                                                        collisions_list.append((entity_name_1, entity_name_2,))
                                                        return (state,
                                                                entity_name_1, entity_name_2,
                                                                collision_def_1, collision_def_2,
                                                                absolute_shape_1, absolute_shape_2,
                                                                contact_points
                                                                )
        return None

cdef void c_clear_collisions_list(list state):
        """
        TODO
        """
        state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_COLLISIONS_LIST] = []

cdef void c_notify_collision_handler(list state):
        cdef list collisions_list = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_COLLISIONS_LIST]

        handler_function = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_HANDLER_FUNCTION]
        if collisions_list and handler_function:
                (handler_function)(state, collisions_list)
