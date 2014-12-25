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

cimport yapyg.fixpoint
cimport yapyg.fixpoint_2d
import yapyg.movers
cimport yapyg.entities
cimport yapyg.collisions

IDX_LINEAR_MOVER_REL_VECTOR = yapyg.movers.IDX_MOVER_FIRST_PARAMETER
IDX_LINEAR_MOVER_SPEED = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 1
IDX_LINEAR_MOVER_ROTATE_MODE = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 2
IDX_LINEAR_MOVER_TRAVEL_VECTOR = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 3
IDX_LINEAR_MOVER_TRAVEL_TIME = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 4
IDX_LINEAR_MOVER_PASSED_TIME = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 5
IDX_LINEAR_MOVER_ON_END_FUNCTION = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 6

cdef int N_ROTATE_MODE_NONE
cdef int N_ROTATE_MODE_AUTO
cdef int N_ROTATE_MODE_CONST

N_ROTATE_MODE_NONE = 0
N_ROTATE_MODE_AUTO = 1
N_ROTATE_MODE_CONST = 2

rotate_mode_trans = {
        "none": N_ROTATE_MODE_NONE,
        "auto": N_ROTATE_MODE_AUTO,
        "const": N_ROTATE_MODE_CONST,
}

cpdef add(list state, str entity_name, tuple rel_vector, int speed, tuple rotate_mode=("none", 0), on_end_function=None, int do_replace=False):
        """
        TODO
        """
        yapyg.movers.add(state, entity_name, create(entity_name, rel_vector, speed, rotate_mode, on_end_function), do_replace)

cpdef list create(str entity_name, tuple rel_vector, int speed, tuple rotate_mode, on_end_function):
        """
        TODO
        """
        cdef int distance
        distance = yapyg.fixpoint_2d.length(rel_vector)
        if distance == 0 or speed == 0:
                print "Distance and speed must be >0"
                return None

        cdef int travel_time
        travel_time = yapyg.fixpoint.div(distance, speed)

        cdef tuple travel_vector
        travel_vector = (
                yapyg.fixpoint.div(rel_vector[0], travel_time),
                yapyg.fixpoint.div(rel_vector[1], travel_time))

        return ["linear",
                run,
                entity_name,
                None,
                rel_vector, # IDX_LINEAR_MOVER_REL_VECTOR
                speed, # IDX_LINEAR_MOVER_SPEED
                (rotate_mode_trans[rotate_mode[0]], rotate_mode[1]),
                travel_vector,
                travel_time,
                0,
                on_end_function,]

cdef int FIXP_1000 = yapyg.fixpoint.int2fix(1000)
cdef int FIXP_360 = yapyg.fixpoint.int2fix(360)

cpdef run(list state, str entity_name, list mover, int frame_time_delta, list movers_to_delete):
        """
        TODO
        """
        cdef int travel_time
        cdef tuple travel_vector
        cdef int passed_time

        travel_time = mover[IDX_LINEAR_MOVER_TRAVEL_TIME]
        travel_vector = mover[IDX_LINEAR_MOVER_TRAVEL_VECTOR]
        passed_time = mover[IDX_LINEAR_MOVER_PASSED_TIME]

        cdef int heading
        cdef int heading_int
        cdef tuple rotate_mode
        rotate_mode = mover[IDX_LINEAR_MOVER_ROTATE_MODE]
        cdef int rot_type
        rot_type = rotate_mode[0]
        cdef int rot_speed
        rot_speed = rotate_mode[1]

        cdef tuple old_pos
        old_pos = yapyg.entities.get_pos(state, entity_name)
        cdef int old_rot
        old_rot = old_pos[2]

        cdef int delta_rot = 0

        if rot_type == N_ROTATE_MODE_AUTO:
                if passed_time == 0:
                        heading = yapyg.fixpoint_2d.heading_from_to((0, 0), travel_vector)
                        heading_int = (yapyg.fixpoint.fix2int(heading) - 90) % 360
                        heading = yapyg.fixpoint.int2fix(heading_int)
                        delta_rot = -old_rot + heading
        elif rot_type == N_ROTATE_MODE_CONST:
                delta_rot = yapyg.fixpoint.mul(rot_speed, frame_time_delta)

        passed_time += yapyg.fixpoint.div(frame_time_delta, FIXP_1000)
        if passed_time > travel_time:
                passed_time = travel_time
        mover[IDX_LINEAR_MOVER_PASSED_TIME] = passed_time

        cdef int d_x
        cdef int d_y
        d_x = yapyg.fixpoint.mul(frame_time_delta, travel_vector[0])
        d_y = yapyg.fixpoint.mul(frame_time_delta, travel_vector[1])

        d_x = yapyg.fixpoint.div(d_x, FIXP_1000)
        d_y = yapyg.fixpoint.div(d_y, FIXP_1000)

        yapyg.entities.add_pos(state, entity_name, d_x, d_y, delta_rot)

        if passed_time == travel_time:
                movers_to_delete.append((entity_name, mover[IDX_LINEAR_MOVER_ON_END_FUNCTION]))

        yapyg.collisions.run(state, entity_name)
