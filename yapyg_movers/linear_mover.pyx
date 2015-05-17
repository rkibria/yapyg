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
Simple linear mover
"""

cimport yapyg.math_2d
import yapyg.movers
cimport yapyg.entities
cimport yapyg.collisions

cdef int IDX_LINEAR_MOVER_REL_VECTOR = yapyg.movers.IDX_MOVER_FIRST_PARAMETER
cdef int IDX_LINEAR_MOVER_SPEED = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 1
cdef int IDX_LINEAR_MOVER_ROTATE_MODE = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 2
cdef int IDX_LINEAR_MOVER_TRAVEL_VECTOR = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 3
cdef int IDX_LINEAR_MOVER_TRAVEL_TIME = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 4
cdef int IDX_LINEAR_MOVER_PASSED_TIME = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 5
cdef int IDX_LINEAR_MOVER_ON_END_FUNCTION = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 6

cdef int N_ROTATE_MODE_NONE = 0
cdef int N_ROTATE_MODE_AUTO = 1
cdef int N_ROTATE_MODE_CONST = 2

cpdef dict rotate_mode_trans = {
        "none": N_ROTATE_MODE_NONE,
        "auto": N_ROTATE_MODE_AUTO,
        "const": N_ROTATE_MODE_CONST,
}

cpdef add(list state, str entity_name, tuple rel_vector, float speed, tuple rotate_mode=("none", 0), on_end_function=None, int do_replace=False):
        """
        TODO
        """
        yapyg.movers.add(state, entity_name, create(entity_name, rel_vector, speed, rotate_mode, on_end_function), do_replace)

cpdef list create(str entity_name, tuple rel_vector, float speed, tuple rotate_mode, on_end_function):
        """
        TODO
        """
        cdef float distance = yapyg.math_2d.length(rel_vector)
        if distance == 0 or speed == 0:
                print "Distance and speed must be >0"
                return None

        cdef float travel_time = (distance / speed)
        cdef tuple travel_vector = (
                ((rel_vector[0]) / travel_time),
                ((rel_vector[1]) / travel_time))

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

cpdef run(list state, str entity_name, list mover, float frame_time_delta, list movers_to_delete):
        """
        TODO
        """
        cdef float travel_time = mover[IDX_LINEAR_MOVER_TRAVEL_TIME]
        cdef tuple travel_vector = mover[IDX_LINEAR_MOVER_TRAVEL_VECTOR]
        cdef float passed_time = mover[IDX_LINEAR_MOVER_PASSED_TIME]
        cdef tuple rotate_mode = mover[IDX_LINEAR_MOVER_ROTATE_MODE]
        cdef int rot_type = rotate_mode[0]
        cdef float rot_speed = rotate_mode[1]
        cdef tuple old_pos = yapyg.entities.get_pos(state, entity_name)
        cdef float old_rot = old_pos[2]

        cdef float heading
        cdef int heading_int
        cdef float delta_rot = 0

        if rot_type == N_ROTATE_MODE_AUTO:
                if passed_time == 0:
                        heading = yapyg.math_2d.get_angle((0, 0), travel_vector)
                        heading_int = (int(heading) - 90) % 360
                        heading = float(heading_int)
                        delta_rot = -old_rot + heading
        elif rot_type == N_ROTATE_MODE_CONST:
                delta_rot = (rot_speed * frame_time_delta)

        passed_time += frame_time_delta / 1000.0
        if passed_time > travel_time:
                passed_time = travel_time
        mover[IDX_LINEAR_MOVER_PASSED_TIME] = passed_time

        cdef float d_x = frame_time_delta * travel_vector[0]
        cdef float d_y = frame_time_delta * travel_vector[1]

        d_x /= 1000.0
        d_y /= 1000.0

        yapyg.entities.add_pos(state, entity_name, d_x, d_y, delta_rot)

        if passed_time == travel_time:
                movers_to_delete.append((entity_name, mover[IDX_LINEAR_MOVER_ON_END_FUNCTION]))

        yapyg.collisions.run(state, entity_name)
