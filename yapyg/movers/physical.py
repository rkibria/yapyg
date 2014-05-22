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
Simulate physical movement
"""

import math

from .. import movers
from .. import entities
from .. import geometry
from .. import physics
from .. import collisions

def add(state, entity_name,
        mass=1,
        vx=0, vy=0,
        ax=0, ay=0,
        friction=0.99955, inelasticity=1,
        on_end_function=None, do_replace=False):
    """
    TODO
    """
    movers.add(state, entity_name, create(entity_name,
        mass,
        vx, vy,
        ax, ay,
        friction, inelasticity,
        on_end_function), do_replace)

def create(entity_name,
        mass,
        vx, vy,
        ax, ay,
        friction, inelasticity,
        on_end_function=None):
    """
    TODO
    """
    return {
            "type": "physics",
            "entity_name": entity_name,

            "mass": mass,
            "vx": vx,
            "vy": vy,
            "ax": ax,
            "ay": ay,
            "friction": friction,
            "inelasticity": inelasticity,

            "run": run,
            "on_end_function": on_end_function,
        }

def run(state, entity_name, mover, frame_time_delta, movers_to_delete):
    """
    TODO
    """
    entities.add_pos(state, entity_name, mover["vx"] * frame_time_delta, mover["vy"] * frame_time_delta)
    mover["vx"] += mover["ax"]
    mover["vy"] += mover["ay"]
    mover["vx"] *= mover["friction"]
    mover["vy"] *= mover["friction"]

def _rectangle_circle_collision(state, rectangle_entity_name, circle_entity_name,
        rectangle_collision_def, circle_collision_def,
        rectangle_physical_mover, circle_physical_mover):
    """
    TODO
    """
    entities.undo_last_move(state, circle_entity_name)

    abs_rectangle_shape = collisions.get_collision_shape(state, rectangle_entity_name, rectangle_collision_def)
    abs_circle_shape = collisions.get_collision_shape(state, circle_entity_name, circle_collision_def)

    circle_x = abs_circle_shape[0]
    circle_y = abs_circle_shape[1]
    circle_r = abs_circle_shape[2]

    rect_x = abs_rectangle_shape[0]
    rect_y = abs_rectangle_shape[1]
    rect_w = abs_rectangle_shape[2]
    rect_h = abs_rectangle_shape[3]
    rect_r = abs_rectangle_shape[4]

    circle_move_vector = [circle_physical_mover["vx"], circle_physical_mover["vy"]]

    if rect_r != 0:
        rotated_circle = geometry.get_rotated_point((rect_x + rect_w / 2.0, rect_y + rect_h / 2.0), (circle_x, circle_y), -rect_r)
        circle_x = rotated_circle[0]
        circle_y = rotated_circle[1]

        circle_move_vector = geometry.get_rotated_point((0, 0), circle_move_vector, -rect_r)

    if circle_y <= rect_y or circle_y >= rect_y + rect_h:
        # circle centre below or above rectangle
        if circle_x > rect_x and circle_x < rect_x + rect_w:
            # lower/upper quadrant
            if circle_y <= rect_y:
                # lower quadrant
                # print "lower quadrant"
                if circle_physical_mover:
                    circle_move_vector[1] = -abs(circle_move_vector[1]) * circle_physical_mover["inelasticity"]
                    # TODO
                    entities.add_pos(state, circle_entity_name, 0, -((circle_y + circle_r) - rect_y))
            else:
                # upper quadrant
                # print "upper quadrant"
                if circle_physical_mover:
                    circle_move_vector[1] = abs(circle_move_vector[1]) * circle_physical_mover["inelasticity"]
                    # TODO
                    entities.add_pos(state, circle_entity_name, 0, (rect_y + rect_h) - (circle_y - circle_r))
        else:
            # lower/upper left/right quadrant
            # print "lower/upper left/right quadrant"
            v_total = math.hypot(circle_move_vector[0], circle_move_vector[1])
            corner_y = None
            corner_x = None
            if circle_y <= rect_y:
                corner_y = rect_y
            else:
                corner_y = rect_y + rect_h
            if circle_x <= rect_x:
                corner_x = rect_x
            else:
                corner_x = rect_x + rect_w
            angle_dx = circle_x - corner_x
            angle_dy = circle_y - corner_y
            angle = math.atan2(angle_dy, angle_dx)
            new_vy = math.sin(angle) * v_total
            new_vx = math.cos(angle) * v_total
            if circle_physical_mover:
                circle_move_vector[0] = new_vx * circle_physical_mover["inelasticity"]
                circle_move_vector[1] = new_vy * circle_physical_mover["inelasticity"]
    else:
        # circle same height as rectangle
        if circle_x < rect_x:
            # left quadrant
            # print "left quadrant"
            if circle_physical_mover:
                circle_move_vector[0] = -abs(circle_move_vector[0]) * circle_physical_mover["inelasticity"]
                # TODO
                entities.add_pos(state, circle_entity_name, -((circle_x + circle_r) - rect_x), 0)
        elif circle_x > rect_x + rect_w:
            # right quadrant
            # print "right quadrant"
            if circle_physical_mover:
                circle_move_vector[0] = abs(circle_move_vector[0]) * circle_physical_mover["inelasticity"]
                # TODO
                entities.add_pos(state, circle_entity_name, (rect_x + rect_w) - (circle_x - circle_r), 0)
        else:
            # inside rectangle: move circle out of the rectangle
            # print "inside"
            if circle_move_vector[0] >= 0:
                if circle_move_vector[1] >= 0:
                    # moving N-NE-E
                    entities.add_pos(state, circle_entity_name, circle_r, circle_r)
                else:
                    # moving S-SE-E
                    entities.add_pos(state, circle_entity_name, circle_r, -circle_r)
            else:
                if circle_move_vector[1] >= 0:
                    # moving N-NW-W
                    entities.add_pos(state, circle_entity_name, -circle_r, circle_r)
                else:
                    # moving S-SW-W
                    entities.add_pos(state, circle_entity_name, -circle_r, -circle_r)

    if circle_physical_mover:
        circle_move_vector = geometry.get_rotated_point((0, 0), circle_move_vector, rect_r)
        circle_physical_mover["vx"] = circle_move_vector[0]
        circle_physical_mover["vy"] = circle_move_vector[1]

def _circle_circle_collision(state, circle_entity_name_1, circle_entity_name_2,
        collision_def_1, collision_def_2,
        circle_physical_mover_1, circle_physical_mover_2):
    """
    TODO
    """
    last_pos_1 = entities.get_last_pos(state, circle_entity_name_1)
    last_pos_2 = entities.get_last_pos(state, circle_entity_name_2)
    if last_pos_1 and last_pos_2:
        if _coin_toss(state):
            entities.undo_last_move(state, circle_entity_name_1)
        else:
            entities.undo_last_move(state, circle_entity_name_2)

    abs_circle_shape_1 = collisions.get_collision_shape(state, circle_entity_name_1, collision_def_1)
    abs_circle_shape_2 = collisions.get_collision_shape(state, circle_entity_name_2, collision_def_2)

    new_vx1, new_vy1, new_vx2, new_vy2 = physics.reflect_speeds(
        geometry.normal_vector(
            (abs_circle_shape_2[0], abs_circle_shape_2[1], ),
            (abs_circle_shape_1[0], abs_circle_shape_1[1], )
            ),
        (circle_physical_mover_1["vx"], circle_physical_mover_1["vy"],),
        (circle_physical_mover_2["vx"], circle_physical_mover_2["vy"]),
        circle_physical_mover_1["mass"],
        circle_physical_mover_2["mass"])
    circle_physical_mover_1["vx"] = new_vx1 * circle_physical_mover_1["inelasticity"]
    circle_physical_mover_1["vy"] = new_vy1 * circle_physical_mover_1["inelasticity"]
    circle_physical_mover_2["vx"] = new_vx2 * circle_physical_mover_2["inelasticity"]
    circle_physical_mover_2["vy"] = new_vy2 * circle_physical_mover_2["inelasticity"]

def _coin_toss(state):
    if not state.has_key("mover.physical.cointoss"):
        state["mover.physical.cointoss"] = False
    last_toss = state["mover.physical.cointoss"]
    last_toss = not last_toss
    state["mover.physical.cointoss"] = last_toss
    return last_toss

def collision_handler(state, collision_list):
    """
    TODO
    """
    for entity_name_1, entity_name_2, collision_def_1, collision_def_2 in collision_list:
        entity_mover_1 = movers.get_active(state, entity_name_1)
        entity_mover_2 = movers.get_active(state, entity_name_2)

        physics_mover_1 = None
        physics_mover_2 = None
        if (entity_mover_1 and entity_mover_1["type"] == "physics"):
            physics_mover_1 = entity_mover_1
        if (entity_mover_2 and entity_mover_2["type"] == "physics"):
            physics_mover_2 = entity_mover_2

        if (physics_mover_1 or physics_mover_2):
            entity_shape_1 = collisions.get_shape(state, entity_name_1)
            entity_shape_2 = collisions.get_shape(state, entity_name_2)

            if entity_shape_1[0] == "rectangle":
                if entity_shape_2[0] == "rectangle":
                    print "TODO r-r"
                    exit()
                elif entity_shape_2[0] == "circle":
                    _rectangle_circle_collision(state, entity_name_1, entity_name_2,
                        collision_def_1, collision_def_2,
                        physics_mover_1, physics_mover_2)
            elif entity_shape_1[0] == "circle":
                if entity_shape_2[0] == "rectangle":
                    _rectangle_circle_collision(state, entity_name_2, entity_name_1,
                        collision_def_2, collision_def_1,
                        physics_mover_2, physics_mover_1)
                elif entity_shape_2[0] == "circle":
                    _circle_circle_collision(state, entity_name_1, entity_name_2,
                        collision_def_1, collision_def_2,
                        physics_mover_1, physics_mover_2)
