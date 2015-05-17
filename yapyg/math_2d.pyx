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
2D vectors
"""

import math

cpdef float dot_product(tuple v_1, tuple v_2):
        """
        TODO
        """
        return (v_1[0] * v_2[0]) + (v_1[1] * v_2[1])

cpdef tuple vector_mul(tuple vec, float factor):
        """
        TODO
        """
        return (vec[0] * factor, vec[1] * factor)

cpdef tuple vector_div(tuple vec, float factor):
        """
        TODO
        """
        return (vec[0] / factor, vec[1] / factor)

cpdef tuple vector_sub(tuple v_1, tuple v_2):
        """
        TODO
        """
        return (v_1[0] - v_2[0], v_1[1] - v_2[1])

cpdef tuple vector_add(tuple v_1, tuple v_2):
        """
        TODO
        """
        return (v_1[0] + v_2[0], v_1[1] + v_2[1])

cpdef tuple components(tuple normal_vector, tuple v_vector):
        """
        TODO
        """
        cdef tuple parallel_vector = vector_mul(normal_vector, dot_product(normal_vector, v_vector))
        cdef tuple perpendicular_vector = vector_sub(v_vector, parallel_vector)
        return (parallel_vector, perpendicular_vector)

cpdef tuple complex_mul(tuple complex_1, tuple complex_2):
        """
        TODO
        """
        return (
                (complex_1[0] * complex_2[0]) - (complex_1[1] * complex_2[1]),
                (complex_1[0] * complex_2[1]) + (complex_1[1] * complex_2[0])
                )

cpdef tuple rotated_point(tuple origin_point, tuple point, float rot):
        """
        TODO
        """
        cdef float rot_rad = math.radians(rot)
        cdef tuple rot_relative_point
        rot_relative_point = complex_mul((point[0] - origin_point[0],
                point[1] - origin_point[1]), (math.cos(rot_rad), math.sin(rot_rad)))
        return (origin_point[0] + rot_relative_point[0], origin_point[1] + rot_relative_point[1])

cpdef float length(tuple vector):
        """
        TODO
        """
        return math.hypot(vector[0], vector[1])

cpdef float distance(tuple pos_1, tuple pos_2):
        """
        TODO
        """
        return length((pos_2[0] - pos_1[0], pos_2[1] - pos_1[1],))

cpdef tuple get_direction_unit_vector(tuple pos_1, tuple pos_2):
        """
        TODO
        """
        cdef float vector_distance = distance(pos_1, pos_2)
        return ((pos_2[0] - pos_1[0]) / vector_distance,
                (pos_2[1] - pos_1[1]) / vector_distance,)

cpdef tuple get_unit_vector(tuple vector):
        """
        TODO
        """
        cdef float vlen = length(vector)
        if vlen == 0:
                return (0, 0)
        else:
                return vector_div(vector, vlen)

cpdef float get_angle(tuple pos1, tuple pos2):
        """
        TODO
        """
        cdef float heading_degrees = math.degrees(math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0]))
        if heading_degrees < 0.0:
                heading_degrees += 360.0
        return heading_degrees
