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
Fixed point math
"""

cdef int c_int2fix(int value)
cdef int c_float2fix(float value)
cdef int c_fix2int(int value)
cdef float c_fix2float(int value)
cdef int c_mul(int op1, int op2)
cdef int c_div(int op1, int op2)
cdef int c_dot_product(tuple v_1, tuple v_2)
cdef tuple c_vector_product(tuple vec, int factor)
cdef tuple c_vector_diff(tuple v_1, tuple v_2)
cdef tuple c_vector_sum(tuple v_1, tuple v_2)
cdef tuple c_components(tuple normal_vector, tuple v_vector)
cdef tuple c_complex_multiply(tuple complex_1, tuple complex_2)
cdef int c_trig_linear_interpolation(int degrees, int index)
cdef int c_sin(int degrees)
cdef int c_cos(int degrees)
cdef tuple c_rotated_point(tuple origin_point, tuple point, int rot)
cdef int c_bit_len(int int_type)
cdef int c_sqrt(int x)
cdef int c_length(tuple vector)
cdef int c_distance(tuple pos_1, tuple pos_2)
cdef tuple c_unit_vector(tuple pos_1, tuple pos_2)
cdef int c_atan2(int y, int x)
cdef int c_negate(int x)
cdef int c_is_circle_circle_collision(tuple c_1, tuple c_2)
cdef int c_is_rect_circle_collision(tuple circ, tuple rect)
cdef int c_is_point_in_circle(tuple point, tuple circ)
cdef int c_heading_from_to(tuple pos1, tuple pos2)
cdef int c_floor(int x)

cdef int FIXP_minus1
cdef int FIXP_0
cdef int FIXP_1
cdef int FIXP_2
cdef int FIXP_90
cdef int FIXP_128
cdef int FIXP_180
cdef int FIXP_270
cdef int FIXP_360
cdef int FIXP_1000
cdef int FIXP_1_5
cdef int FIXP_PI
