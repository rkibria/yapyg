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

cdef int IDX_MOVERS_PHYSICAL_ENTITY_NAME = 2
cdef int IDX_MOVERS_PHYSICAL_MASS = 3
cdef int IDX_MOVERS_PHYSICAL_VX = 4
cdef int IDX_MOVERS_PHYSICAL_VY = 5
cdef int IDX_MOVERS_PHYSICAL_AX = 6
cdef int IDX_MOVERS_PHYSICAL_AY = 7
cdef int IDX_MOVERS_PHYSICAL_FRICTION = 8
cdef int IDX_MOVERS_PHYSICAL_INELASTICITY = 9
cdef int IDX_MOVERS_PHYSICAL_ON_END_FUNCTION = 10

cpdef add(list state,
                str entity_name,
                int mass,
                int vx,
                int vy,
                int ax,
                int ay,
                int friction,
                int inelasticity,
                int do_replace=*)

cdef list c_create(str entity_name,
                int mass,
                int vx,
                int vy,
                int ax,
                int ay,
                int friction,
                int inelasticity,
                )

cdef int FIXP_1000

cpdef run(list state, str entity_name, list mover, int frame_time_delta, list movers_to_delete)

cdef int FIXP_2

cdef c_rectangle_circle_collision(list state,
                str rectangle_entity_name,
                str circle_entity_name,
                tuple abs_rectangle_shape,
                tuple abs_circle_shape,
                list rectangle_physical_mover,
                list circle_physical_mover)

cdef void c_circle_circle_collision(list state,
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
                tuple absolute_shape_2)

cdef tuple c_elastic_collision(int v_1, int v_2, int m_1, int m_2)

cdef tuple c_reflect_speeds(tuple unit_vector, tuple v1_vector, tuple v2_vector, int m_1, int m_2)
