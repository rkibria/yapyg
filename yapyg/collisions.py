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

import math

import geometry
import entities

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

def initialize(state):
    """
    TODO
    """
    state["collisions"] = {
        "handler_function": None,
        "entities": {},
        "hash_map": {},
        "active_checks": [],
    }
    entities.add_pos_listener(state, entity_pos_listener)

def entity_pos_listener(state, entity_name, pos):
    """
    TODO
    """
    if state["collisions"]["entities"].has_key(entity_name):
        _update_hash(state, entity_name)

def destroy(state):
    """
    TODO
    """
    del state["collisions"]

def set_handler(state, handler_function):
    """
    TODO
    """
    state["collisions"]["handler_function"] = handler_function

def get_shape(state, entity_name):
    """
    TODO
    """
    if state["collisions"]["entities"].has_key(entity_name):
        return state["collisions"]["entities"][entity_name]["collision_shape"]
    else:
        return None

def add(state, entity_name, collision_shape, active_check=True):
    """
    TODO
    """
    state["collisions"]["entities"][entity_name] = {
        "collision_shape": collision_shape,
        "active_check": active_check,
        "last_pos": None,
        }

    if active_check:
        state["collisions"]["active_checks"].append(entity_name)

    _update_hash(state, entity_name)

def _get_hash_area(state, entity_name, entity_lower_left):
    """
    Returns absolute tile positions of lower left and upper right of area to check
    """
    lower_left_x_offset = 0
    lower_left_y_offset = 0
    upper_right_x_offset = 0
    upper_right_y_offset = 0

    collision_shape = state["collisions"]["entities"][entity_name]["collision_shape"]
    if collision_shape[0] == "circle":
        upper_right_x_offset = collision_shape[1]
        upper_right_y_offset = collision_shape[1]
    elif collision_shape[0] == "rectangle":
        rot = entities.get_rot(state, entity_name)
        if rot == 0:
            upper_right_x_offset = collision_shape[1]
            upper_right_y_offset = collision_shape[2]
        else:
            lower_left_x_offset = -1
            lower_left_y_offset = -1
            upper_right_x_offset = collision_shape[1] + 1
            upper_right_y_offset = collision_shape[2] + 1

    area_lower_left = (entity_lower_left[0] + lower_left_x_offset,
        entity_lower_left[1] + lower_left_y_offset)

    area_upper_right = (entity_lower_left[0] + upper_right_x_offset,
        entity_lower_left[1] + upper_right_y_offset)

    area_lower_left = (int(math.floor(area_lower_left[0])), int(math.floor(area_lower_left[1])))
    area_upper_right = (int(math.floor(area_upper_right[0])), int(math.floor(area_upper_right[1])))
    return (area_lower_left, area_upper_right)

def _update_hash(state, entity_name):
    """
    TODO
    """
    last_pos = state["collisions"]["entities"][entity_name]["last_pos"]
    if last_pos:
        _remove_hash_entries(state, entity_name, last_pos)

    state["collisions"]["entities"][entity_name]["last_pos"] = entities.get_pos(state, entity_name)

    _insert_hash_entries(state, entity_name, entities.get_pos(state, entity_name))

def _insert_hash_entries(state, entity_name, entity_lower_left):
    """
    TODO
    """
    hash_map = state["collisions"]["hash_map"]
    entity_lower_left, entity_upper_right = _get_hash_area(state, entity_name, entity_lower_left)

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
    hash_map = state["collisions"]["hash_map"]
    entity_lower_left, entity_upper_right = _get_hash_area(state, entity_name, entity_lower_left)

    for x in xrange(entity_lower_left[0], entity_upper_right[0] + 1):
        for y in xrange(entity_lower_left[1], entity_upper_right[1] + 1):
            hash_map[(x, y)].remove(entity_name)

def delete(state, entity_name):
    """
    TODO
    """
    _remove_hash_entries(state, entity_name, entities.get_pos(state, entity_name))
    del state["collisions"]["entities"][entity_name]

def get_collision_shape(state, entity_name, collision_def):
    """
    Get the absolute shape taking into account position

    collision_shape:
        ["rectangle", width, height]
        ["circle", diameter]
    =>
        circle: (center_x, center_y, radius)
        rectangle: (x, y, w, h, rotation)
    """
    pos = entities.get_pos(state, entity_name)
    pos_offset = entities.get_pos_offset(state, entity_name)
    collision_shape = collision_def["collision_shape"]

    if collision_shape[0] == "circle":
        radius = collision_shape[1] / 2.0
        return (pos[0] + pos_offset[0] + radius, pos[1] + pos_offset[1] + radius, radius)
    elif collision_shape[0] == "rectangle":
        return (pos[0] + pos_offset[0], pos[1] + pos_offset[1],
            collision_shape[1], collision_shape[2], entities.get_rot(state, entity_name))
    else:
        raise YapygCollisionException("Unknown shape %s" % collision_shape[0])

def _is_collision(state, shape_type_1, shape_type_2, absolute_shape_1, absolute_shape_2):
    """
    TODO
    """
    if shape_type_1 == "circle":
        if shape_type_2 == "circle":
            return geometry.is_circle_circle_collision(absolute_shape_1, absolute_shape_2)
        elif shape_type_2 == "rectangle":
            return geometry.is_rect_circle_collision(absolute_shape_1, absolute_shape_2, exact_check=True)
        else:
            raise YapygCollisionException("Unknown shape %s" % shape_type_2)
    elif shape_type_1 == "rectangle":
        if shape_type_2 == "circle":
            return geometry.is_rect_circle_collision(absolute_shape_2, absolute_shape_1, exact_check=True)
        elif shape_type_2 == "rectangle":
            raise YapygCollisionException("TODO")
        else:
            raise YapygCollisionException("Unknown shape %s" % shape_type_2)
    else:
        raise YapygCollisionException("Unknown shape %s" % shape_type_1)

def run(state):
    """
    TODO
    """
    if not state["collisions"]["handler_function"]:
        return

    hash_map = state["collisions"]["hash_map"]
    collision_list = []
    active_checks_done = set()

    for entity_name_1 in state["collisions"]["active_checks"]:

        collision_def_1 = state["collisions"]["entities"][entity_name_1]
        absolute_shape_1 = get_collision_shape(state, entity_name_1, collision_def_1)

        entity_1_lower_left = entities.get_pos(state, entity_name_1)
        entity_1_lower_left, entity_1_upper_right = _get_hash_area(state, entity_name_1, entity_1_lower_left)

        for x in xrange(entity_1_lower_left[0], entity_1_upper_right[0] + 1):
            for y in xrange(entity_1_lower_left[1], entity_1_upper_right[1] + 1):
                hash = (x, y)
                if not hash_map.has_key(hash):
                    continue

                collision_candidates = hash_map[hash]

                for entity_name_2 in collision_candidates:
                    if entity_name_1 == entity_name_2:
                        continue

                    collision_def_2 = state["collisions"]["entities"][entity_name_2]
                    if collision_def_2["active_check"]:
                        if entity_name_2 in active_checks_done:
                            continue

                    absolute_shape_2 = get_collision_shape(state, entity_name_2, collision_def_2)

                    if _is_collision(state,
                            collision_def_1["collision_shape"][0],
                            collision_def_2["collision_shape"][0],
                            absolute_shape_1,
                            absolute_shape_2):
                        collision_list.append((entity_name_1, entity_name_2,
                            collision_def_1, collision_def_2))

                        active_checks_done.add(entity_name_1)
                        if collision_def_2["active_check"]:
                            active_checks_done.add(entity_name_2)

    if collision_list:
        (state["collisions"]["handler_function"])(state, collision_list)
