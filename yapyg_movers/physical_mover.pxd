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
Simulate physical movement
"""

cpdef add(list state,
                str entity_name,
                float mass,
                float vx,
                float vy,
                float ax,
                float ay,
                float friction,
                float inelasticity,
                float vr,
                float rot_friction,
                float rot_decay,
                float stickyness,
                int do_replace=*)

cdef list c_create(str entity_name,
                float mass,
                float vx,
                float vy,
                float ax,
                float ay,
                float friction,
                float inelasticity,
                float vr,
                float rot_friction,
                float rot_decay,
                float stickyness
                )

cpdef run(list state, str entity_name, list mover, float frame_time_delta, list movers_to_delete)

cdef rectangle_circle_collision(list state,
                str rectangle_entity_name,
                str circle_entity_name,
                tuple abs_rectangle_shape,
                tuple abs_circle_shape,
                list rectangle_physical_mover,
                list circle_physical_mover)

cdef void circle_circle_collision(list state,
                str circle_entity_name_1,
                str circle_entity_name_2,
                tuple abs_circle_shape_1,
                tuple abs_circle_shape_2,
                list circle_physical_mover_1,
                list circle_physical_mover_2)

cpdef collision_handler(list state,
                str entity_name_1,
                str entity_name_2,
                list collision_def_1,
                list collision_def_2,
                tuple absolute_shape_1,
                tuple absolute_shape_2,
                list contact_points)

cpdef tuple elastic_collision(float v_1, float v_2, float m_1, float m_2)
cpdef tuple reflect_velocities(tuple unit_vector, tuple v1_vector, tuple v2_vector, float m_1, float m_2)
