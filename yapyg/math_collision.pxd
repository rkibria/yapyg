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
Fixed point math - collision algorithms
"""

cpdef int is_rect_rect_collision(tuple rect_1, tuple rect_2, list contact_points)
cpdef int is_circle_circle_collision(tuple c_1, tuple c_2, list contact_points)
cpdef int is_rect_circle_collision(tuple circ, tuple rect, list contact_points)
cpdef int is_point_in_circle(tuple point, tuple circ)
cpdef int is_point_in_rect(tuple point, tuple rectangle)
cpdef tuple get_rect_points(tuple rect)
cpdef int value_in_range(float value, float min_limit, float max_limit)
cpdef tuple get_contact_sum_vector(list contact_points, tuple origin_point)

cpdef int is_rectangle_visible(int win_w, int win_h, int x1, int y1, int w, int h)
cpdef int intervals_overlap(int a1, int a2, int b1, int b2)
cpdef tuple get_clipping_rectangle(int x1, int y1, int w, int h)
cpdef tuple f_get_clipping_rectangle(float x1, float y1, float w, float h)
