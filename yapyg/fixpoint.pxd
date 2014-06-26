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

cpdef int int2fix(int value)
cpdef int float2fix(float value)
cpdef int fix2int(int value)
cpdef float fix2float(int value)
cpdef int mul(int op1, int op2)
cpdef int div(int op1, int op2)
cpdef int dot_product(tuple v_1, tuple v_2)
cpdef tuple vector_product(tuple vec, int factor)
cpdef tuple vector_diff(tuple v_1, tuple v_2)
cpdef tuple vector_sum(tuple v_1, tuple v_2)
cpdef tuple components(tuple normal_vector, tuple v_vector)
cpdef tuple complex_multiply(tuple complex_1, tuple complex_2)
cdef int trig_linear_interpolation(int degrees, int index)
cpdef int sin(int degrees)
cpdef int cos(int degrees)
cpdef tuple rotated_point(tuple origin_point, tuple point, int rot)
cdef int bit_len(int int_type)
cpdef int sqrt(int x)
cpdef int length(tuple vector)
cpdef int distance(tuple pos_1, tuple pos_2)
cpdef tuple unit_vector(tuple pos_1, tuple pos_2)
cpdef int atan2(int y, int x)
cpdef int negate(int x)
cpdef int is_circle_circle_collision(tuple c_1, tuple c_2)
cpdef int is_rect_circle_collision(tuple circ, tuple rect)
cpdef int is_point_in_circle(tuple point, tuple circ)
cpdef int heading_from_to(tuple pos1, tuple pos2)
cpdef int floor(int x)
cpdef int modulo(int x, int d)

cpdef int FIXP_minus1
cpdef int FIXP_0
cpdef int FIXP_1
cpdef int FIXP_2
cpdef int FIXP_90
cpdef int FIXP_128
cpdef int FIXP_180
cpdef int FIXP_270
cpdef int FIXP_360
cpdef int FIXP_1000
cpdef int FIXP_1_5
cpdef int FIXP_PI
