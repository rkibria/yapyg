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
    }

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
        }

def _get_collision_shape(state, entity_name, collision_def):
    """
    collision_shape:
        ["rectangle", width, height]
        ["circle", diameter]
    =>
        circle: (center_x, center_y, radius)
        rectangle: (x, y, w, h)
    """
    pos = entities.get_pos(state, entity_name)
    pos_offset = entities.get_pos_offset(state, entity_name)
    collision_shape = collision_def["collision_shape"]

    if collision_shape[0] == "circle":
        radius = collision_shape[1] / 2.0
        return (pos[0] + pos_offset[0] + radius, pos[1] + pos_offset[1] + radius, radius)
    elif collision_shape[0] == "rectangle":
        return (pos[0] + pos_offset[0], pos[1] + pos_offset[1], collision_shape[1], collision_shape[2])
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

    collision_list = []
    entity_list = state["collisions"]["entities"].keys()

    for index_1 in xrange(len(entity_list)):
        entity_name_1 = entity_list[index_1]
        collision_def_1 = state["collisions"]["entities"][entity_name_1]
        absolute_shape_1 = _get_collision_shape(state, entity_name_1, collision_def_1)

        for index_2 in xrange(index_1 + 1, len(entity_list)):
            entity_name_2 = entity_list[index_2]
            if entity_name_2 == entity_name_1:
                continue

            collision_def_2 = state["collisions"]["entities"][entity_name_2]
            if not collision_def_1["active_check"] and not collision_def_2["active_check"]:
                continue

            absolute_shape_2 = _get_collision_shape(state, entity_name_2, collision_def_2)

            if _is_collision(state,
                    collision_def_1["collision_shape"][0],
                    collision_def_2["collision_shape"][0],
                    absolute_shape_1,
                    absolute_shape_2):
                collision_list.append((entity_name_1, entity_name_2,
                    absolute_shape_1, absolute_shape_2))

    if collision_list:
        (state["collisions"]["handler_function"])(state, collision_list)
