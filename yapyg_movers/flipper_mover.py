# Copyright (c) 2015 Raihan Kibria
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

"""

import math

from yapyg import entities
from yapyg import math_2d
from yapyg import collisions
from yapyg import movers

FLIPPER_MOVER_NAME = "flipper"

IDX_FLIPPER_MOVER_ORIG_POS = movers.IDX_MOVER_FIRST_PARAMETER
IDX_FLIPPER_MOVER_WIDTH = movers.IDX_MOVER_FIRST_PARAMETER + 1
IDX_FLIPPER_MOVER_HEIGHT = movers.IDX_MOVER_FIRST_PARAMETER + 2
IDX_FLIPPER_MOVER_OFFSET = movers.IDX_MOVER_FIRST_PARAMETER + 3
IDX_FLIPPER_MOVER_SPEED = movers.IDX_MOVER_FIRST_PARAMETER + 4
IDX_FLIPPER_MOVER_OFFSET_POS = movers.IDX_MOVER_FIRST_PARAMETER + 5
IDX_FLIPPER_MOVER_CENTRE_POS = movers.IDX_MOVER_FIRST_PARAMETER + 6
IDX_FLIPPER_MOVER_ANGLE = movers.IDX_MOVER_FIRST_PARAMETER + 7

def add(state, entity_name, width, height, offset, speed, do_replace=False):
        """
        speed = degrees/sec
        """
        movers.add(state, entity_name, create(state, entity_name, width, height, offset, speed), do_replace)

def create(state, entity_name, width, height, offset, speed):
        """
        """
        start_pos = entities.get_pos(state, entity_name)
        orig_x,orig_y,old_angle = start_pos
        centre_x = orig_x + (width / 2.0)
        centre_y = orig_y + (height / 2.0)
        offset_x = centre_x + offset
        return [FLIPPER_MOVER_NAME,
                run,
                entity_name,
                collision_handler,
                start_pos,
                width,
                height,
                offset,
                speed,
                (offset_x, centre_y),
                (centre_x, centre_y),
                0.0,
                ]

def run(state, entity_name, mover, frame_time_delta, movers_to_delete):
        """
        TODO
        """
        speed = mover[IDX_FLIPPER_MOVER_SPEED]
        offset_pos = mover[IDX_FLIPPER_MOVER_OFFSET_POS]
        centre_pos = mover[IDX_FLIPPER_MOVER_CENTRE_POS]
        angle = mover[IDX_FLIPPER_MOVER_ANGLE]

        rotated_centre_x,rotated_centre_y = math_2d.rotated_point(offset_pos,
                                                                      centre_pos,
                                                                      angle)

        entities.set_pos(state, entity_name, rotated_centre_x, rotated_centre_y, angle)

        collision_result = collisions.run(state, entity_name)
        if collision_result:
                entities.undo_last_move(state, entity_name)
                collision_handler(*collision_result)
        else:
                angle += (speed * frame_time_delta) / 1000.0
                angle = math.fmod(angle, 360.0)
                mover[IDX_FLIPPER_MOVER_ANGLE] = angle

def collision_handler(state,
                entity_name_1,
                entity_name_2,
                collision_def_1,
                collision_def_2,
                absolute_shape_1,
                absolute_shape_2,
                contact_points,
                ):
        """
        TODO
        """
        entity_mover_1 = movers.get_active(state, entity_name_1)
        entity_mover_2 = movers.get_active(state, entity_name_2)
        if entity_mover_1 and entity_mover_1[0] == "physics":
                hit_physical_object(state, entity_name_2, entity_mover_2, entity_name_1, entity_mover_1)
        elif entity_mover_2 and entity_mover_2[0] == "physics":
                hit_physical_object(state, entity_name_1, entity_mover_1, entity_name_2, entity_mover_2)

def hit_physical_object(state, flipper_entity_name, flipper_entity_mover, physics_entity_name, physics_entity_mover):
        speed = flipper_entity_mover[IDX_FLIPPER_MOVER_SPEED]
        # centre_pos = flipper_entity_mover[IDX_FLIPPER_MOVER_CENTRE_POS]
        # phys_pos = entities.get_pos(state, physics_entity_name)
        angle = flipper_entity_mover[IDX_FLIPPER_MOVER_ANGLE]
        angle += 90.0
        angle_rad = math.radians(angle)
        hit_vector = (math.cos(angle_rad), math.sin(angle_rad))
        hit_vector = (hit_vector[0] * speed, hit_vector[1] * speed)
        factor = 360.0
        hit_vector = (hit_vector[0] / factor, hit_vector[1] / factor)
        physics_entity_mover[5] += hit_vector[0]
        physics_entity_mover[6] += hit_vector[1]
