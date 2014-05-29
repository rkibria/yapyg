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
Simple linear mover
"""

from .. import geometry
from .. import movers
from .. import entities

IDX_LINEAR_MOVER_ENTITY_NAME = 2
IDX_LINEAR_MOVER_REL_VECTOR = 3
IDX_LINEAR_MOVER_SPEED = 4
IDX_LINEAR_MOVER_DO_ROTATE = 5
IDX_LINEAR_MOVER_TRAVEL_VECTOR = 6
IDX_LINEAR_MOVER_TRAVEL_TIME = 7
IDX_LINEAR_MOVER_PASSED_TIME = 8
IDX_LINEAR_MOVER_ON_END_FUNCTION = 9

class YapygMoverLinearException(Exception):
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

def add(state, entity_name, rel_vector, speed, do_rotate=False, on_end_function=None, do_replace=False):
        """
        TODO
        """
        movers.add(state, entity_name, create(entity_name, rel_vector, speed, do_rotate, on_end_function), do_replace)

def create(entity_name, rel_vector, speed, do_rotate, on_end_function):
        """
        TODO
        """
        distance = geometry.get_vector_size(rel_vector)
        if distance == 0 or speed == 0:
                raise YapygMoverLinearException("Distance and speed must be >0")

        travel_time = distance / speed
        travel_vector = [rel_vector[0] / travel_time, rel_vector[1] / travel_time]
        return ["linear",
                run,
                entity_name,
                rel_vector,
                speed,
                do_rotate,
                travel_vector,
                travel_time,
                0,
                on_end_function,]

def run(state, entity_name, mover, frame_time_delta, movers_to_delete):
        """
        TODO
        """
        travel_time = mover[IDX_LINEAR_MOVER_TRAVEL_TIME]
        travel_vector = mover[IDX_LINEAR_MOVER_TRAVEL_VECTOR]
        passed_time = mover[IDX_LINEAR_MOVER_PASSED_TIME]

        if passed_time == 0 and mover[IDX_LINEAR_MOVER_DO_ROTATE]:
                entities.set_rot(state, entity_name, (int(geometry.get_rotation([0, 0], travel_vector)) - 90) % 360)

        passed_time += frame_time_delta
        if passed_time > travel_time:
                passed_time = travel_time
        mover[IDX_LINEAR_MOVER_PASSED_TIME] = passed_time

        entities.add_pos(state, entity_name, frame_time_delta * travel_vector[0], frame_time_delta * travel_vector[1])

        if passed_time == travel_time:
                movers_to_delete.append((entity_name, mover[IDX_LINEAR_MOVER_ON_END_FUNCTION]))
