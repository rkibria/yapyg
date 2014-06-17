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

import globals
import fixpoint
import entities

HASH_SCALE_FACTOR = fixpoint.int2fix(4)

class YapygCollisionException(Exception):
        """
        TODO
        """
        def __init__(self, value):
                """
                TODO
                """
                self.value = value

        def __str__(self):
                """
                TODO
                """
                return repr(self.value)

IDX_COLLISIONDB_ENTITIES = 0
IDX_COLLISIONDB_HASH_MAP = 1
IDX_COLLISIONDB_HANDLER_FUNCTION = 2

IDX_COLLISION_SHAPES = 0
IDX_COLLISION_LAST_POS = 1
IDX_COLLISION_ABSOLUTE_SHAPE = 2

def initialize(state):
        """
        TODO
        """
        state[globals.IDX_STATE_COLLISIONS] = [
                {},
                {},
                None,]
        entities.add_pos_listener(state, entity_pos_listener)

def entity_pos_listener(state, entity_name, pos):
        """
        TODO
        """
        if state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES].has_key(entity_name):
                state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES][entity_name][IDX_COLLISION_ABSOLUTE_SHAPE] = None
                _update_hash(state, entity_name, pos)

def destroy(state):
        """
        TODO
        """
        state[globals.IDX_STATE_COLLISIONS] = None

def set_handler(state, handler_function):
        """
        TODO
        """
        state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_HANDLER_FUNCTION] = handler_function

def add(state, entity_name, shapes_list):
        """
        TODO
        """
        trans_shapes_list = []
        for shape in shapes_list:
                if shape[0] == "rectangle":
                        trans_shape = ("rectangle",
                                fixpoint.float2fix(float(shape[1])),
                                fixpoint.float2fix(float(shape[2])),
                                fixpoint.float2fix(float(shape[3])),
                                fixpoint.float2fix(float(shape[4])),)
                elif shape[0] == "circle":
                        trans_shape = ("circle",
                                fixpoint.float2fix(float(shape[1])),
                                fixpoint.float2fix(float(shape[2])),
                                fixpoint.float2fix(float(shape[3])),)
                else:
                        raise YapygCollisionException("Unknown shape %s" % shape[0])
                trans_shapes_list.append(trans_shape)

        state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES][entity_name] = [
                trans_shapes_list, # IDX_COLLISION_SHAPES
                None, # IDX_COLLISION_LAST_POS
                None, # IDX_COLLISION_ABSOLUTE_SHAPE
                ]

        _update_hash(state, entity_name, entities.get_pos(state, entity_name))

def _get_hash_area(state, entity_name, entity_lower_left):
        """
        Returns absolute tile positions of lower left and upper right of area to check
                ["rectangle", x, y, width, height]
                ["circle", x, y, radius]
        """
        lower_left_x_offset = 0
        lower_left_y_offset = 0
        upper_right_x_offset = 0
        upper_right_y_offset = 0

        FIXP_1_5 = fixpoint.FIXP_1_5
        div = fixpoint.div
        negate = fixpoint.negate
        mul = fixpoint.mul

        entity_shapes = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES][entity_name][IDX_COLLISION_SHAPES]
        for collision_shape in entity_shapes:
                if collision_shape[0] == "circle":
                        c_x = mul(collision_shape[1], HASH_SCALE_FACTOR)
                        c_y = mul(collision_shape[2], HASH_SCALE_FACTOR)
                        c_r = mul(collision_shape[3], HASH_SCALE_FACTOR)

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
                        r_x = mul(collision_shape[1], HASH_SCALE_FACTOR)
                        r_y = mul(collision_shape[2], HASH_SCALE_FACTOR)
                        r_w = mul(collision_shape[3], HASH_SCALE_FACTOR)
                        r_h = mul(collision_shape[4], HASH_SCALE_FACTOR)
                        rot = entities.get_rot(state, entity_name)

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
                                if r_x != 0 or r_y != 0:
                                        raise YapygCollisionException("TODO")

                                max_extent = div(negate(max(r_w, r_h)), fixpoint.FIXP_2)

                                if max_extent < lower_left_x_offset:
                                        lower_left_x_offset = max_extent

                                if max_extent < lower_left_y_offset:
                                        lower_left_y_offset = max_extent

                                max_extent = mul(FIXP_1_5, max(r_w, r_h))

                                if max_extent > upper_right_x_offset:
                                        upper_right_x_offset = max_extent
                                if max_extent > upper_right_y_offset:
                                        upper_right_y_offset = max_extent

        entity_lower_left = (mul(entity_lower_left[0], HASH_SCALE_FACTOR), mul(entity_lower_left[1], HASH_SCALE_FACTOR))

        area_lower_left = (entity_lower_left[0] + lower_left_x_offset,
                entity_lower_left[1] + lower_left_y_offset)

        area_upper_right = (entity_lower_left[0] + upper_right_x_offset,
                entity_lower_left[1] + upper_right_y_offset)

        fix2int = fixpoint.fix2int
        floor = fixpoint.floor
        area_lower_left = (fix2int(floor(area_lower_left[0])), fix2int(floor(area_lower_left[1])))
        area_upper_right = (fix2int(floor(area_upper_right[0])), fix2int(floor(area_upper_right[1])))
        return (area_lower_left, area_upper_right)

def _update_hash(state, entity_name, new_pos):
        """
        TODO
        """
        last_pos = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES][entity_name][IDX_COLLISION_LAST_POS]
        if last_pos:
                _remove_hash_entries(state, entity_name, last_pos)

        state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES][entity_name][IDX_COLLISION_LAST_POS] = new_pos

        entity_lower_left, entity_upper_right = _get_hash_area(state, entity_name, new_pos)

        hash_map = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_HASH_MAP]
        for x in xrange(entity_lower_left[0], entity_upper_right[0] + 1):
                for y in xrange(entity_lower_left[1], entity_upper_right[1] + 1):
                        hash = (x, y)
                        if not hash_map.has_key(hash):
                                hash_map[hash] = set()
                        hash_map[hash].add(entity_name)

def _remove_hash_entries(state, entity_name, entity_lower_left):
        """
        TODO
        """
        hash_map = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_HASH_MAP]
        entity_lower_left, entity_upper_right = _get_hash_area(state, entity_name, entity_lower_left)

        for x in xrange(entity_lower_left[0], entity_upper_right[0] + 1):
                for y in xrange(entity_lower_left[1], entity_upper_right[1] + 1):
                        hash_map[(x, y)].remove(entity_name)

def delete(state, entity_name):
        """
        TODO
        """
        _remove_hash_entries(state, entity_name, entities.get_pos(state, entity_name))
        del state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES][entity_name]

def get_collision_shapes(state, entity_name, collision_def):
        """
        Get the absolute shapes taking into account position and rotation

        collision_shape:
                ["rectangle", x, y, width, height]
                ["circle", x, y, radius]
        =>
                circle: ("circle", center_x, center_y, radius)
                rectangle: ("rectangle", x, y, w, h, rotation)
        """
        cached_absolute_shapes = state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES][entity_name][IDX_COLLISION_ABSOLUTE_SHAPE]
        if cached_absolute_shapes:
                return cached_absolute_shapes

        pos = entities.get_pos(state, entity_name)
        pos_offset = entities.get_pos_offset(state, entity_name)
        absolute_shapes = []

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
                                r_w, r_h, entities.get_rot(state, entity_name)))
                else:
                        raise YapygCollisionException("Unknown shape %s" % collision_shape[0])

        state[globals.IDX_STATE_COLLISIONS][IDX_COLLISIONDB_ENTITIES][entity_name][IDX_COLLISION_ABSOLUTE_SHAPE] = absolute_shapes

        return absolute_shapes

def run(state, entity_name_1):
        """
        TODO
        """
        state_collisions = state[globals.IDX_STATE_COLLISIONS]

        collision_handler = state_collisions[IDX_COLLISIONDB_HANDLER_FUNCTION]
        if not collision_handler:
                return

        state_collisions_entities = state_collisions[IDX_COLLISIONDB_ENTITIES]
        if not state_collisions_entities.has_key(entity_name_1):
                return

        hash_map = state_collisions[IDX_COLLISIONDB_HASH_MAP]

        collision_def_1 = state_collisions_entities[entity_name_1]
        absolute_shapes_1 = get_collision_shapes(state, entity_name_1, collision_def_1)

        entity_1_lower_left, entity_1_upper_right = _get_hash_area(state,
                entity_name_1, entities.get_pos(state, entity_name_1))

        is_circle_circle_collision = fixpoint.is_circle_circle_collision
        is_rect_circle_collision = fixpoint.is_rect_circle_collision

        already_checked_set = set()
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

                                for absolute_shape_1 in absolute_shapes_1:
                                        for absolute_shape_2 in absolute_shapes_2:

                                                is_collision = False
                                                absolute_shape_1_type = absolute_shape_1[0]
                                                absolute_shape_2_type = absolute_shape_2[0]

                                                if absolute_shape_1_type == "circle":
                                                        if absolute_shape_2_type == "circle":
                                                                is_collision = is_circle_circle_collision(absolute_shape_1, absolute_shape_2)
                                                        elif absolute_shape_2_type == "rectangle":
                                                                is_collision = is_rect_circle_collision(absolute_shape_1, absolute_shape_2)
                                                elif absolute_shape_1_type == "rectangle":
                                                        if absolute_shape_2_type == "circle":
                                                                is_collision = is_rect_circle_collision(absolute_shape_2, absolute_shape_1)
                                                        elif absolute_shape_2_type == "rectangle":
                                                                # TODO
                                                                is_collision = False

                                                if is_collision:
                                                        (collision_handler)(
                                                                state,
                                                                entity_name_1, entity_name_2,
                                                                collision_def_1, collision_def_2,
                                                                absolute_shape_1, absolute_shape_2)
                                                        return
