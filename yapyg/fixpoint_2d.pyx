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
Fixed point math - 2D vectors
"""

cimport fixpoint
cimport fixpoint_trig

cpdef int dot_product(tuple v_1, tuple v_2):
        """
        TODO
        """
        return fixpoint.mul(v_1[0], v_2[0]) + fixpoint.mul(v_1[1], v_2[1])

cpdef tuple vector_product(tuple vec, int factor):
        """
        TODO
        """
        return (fixpoint.mul(vec[0], factor), fixpoint.mul(vec[1], factor))

cpdef tuple vector_div(tuple vec, int factor):
        """
        TODO
        """
        return (fixpoint.div(vec[0], factor), fixpoint.div(vec[1], factor))

cpdef tuple vector_diff(tuple v_1, tuple v_2):
        """
        TODO
        """
        return (v_1[0] - v_2[0], v_1[1] - v_2[1])

cpdef tuple vector_sum(tuple v_1, tuple v_2):
        """
        TODO
        """
        return (v_1[0] + v_2[0], v_1[1] + v_2[1])

cpdef tuple components(tuple normal_vector, tuple v_vector):
        """
        TODO
        """
        cdef tuple parallel_vector
        parallel_vector = vector_product(normal_vector,
                dot_product(normal_vector, v_vector))

        cdef tuple perpendicular_vector
        perpendicular_vector = vector_diff(v_vector, parallel_vector)

        return (parallel_vector, perpendicular_vector)

cpdef tuple complex_multiply(tuple complex_1, tuple complex_2):
        """
        TODO
        """
        return (fixpoint.mul(complex_1[0], complex_2[0]) - fixpoint.mul(complex_1[1], complex_2[1]),
                fixpoint.mul(complex_1[0], complex_2[1]) + fixpoint.mul(complex_1[1], complex_2[0]))

cpdef tuple rotated_point(tuple origin_point, tuple point, int rot):
        """
        TODO
        """
        cdef tuple rot_relative_point
        rot_relative_point = complex_multiply((point[0] - origin_point[0],
                point[1] - origin_point[1]), (fixpoint_trig.cos(rot), fixpoint_trig.sin(rot)))
        return (origin_point[0] + rot_relative_point[0], origin_point[1] + rot_relative_point[1])

cpdef int length(tuple vector):
        """
        TODO
        """
        cdef int x_dist
        x_dist = vector[0]
        x_dist = fixpoint.mul(x_dist, x_dist)

        cdef int y_dist
        y_dist = vector[1]
        y_dist = fixpoint.mul(y_dist, y_dist)

        return fixpoint.sqrt(x_dist + y_dist)

cpdef int distance(tuple pos_1, tuple pos_2):
        """
        TODO
        """
        return length((pos_2[0] - pos_1[0], pos_2[1] - pos_1[1],))

cpdef tuple unit_vector(tuple pos_1, tuple pos_2):
        """
        TODO
        """
        cdef int vector_distance
        vector_distance = distance(pos_1, pos_2)
        return (fixpoint.div(pos_2[0] - pos_1[0], vector_distance),
                fixpoint.div(pos_2[1] - pos_1[1], vector_distance),)

cpdef tuple get_unit_vector(tuple vector):
        """
        TODO
        """
        cdef int vlen = length(vector)
        if vlen == 0:
                return (0, 0)
        else:
                return vector_div(vector, vlen)

cpdef int heading_from_to(tuple pos1, tuple pos2):
        """
        TODO
        """
        return fixpoint_trig.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])
