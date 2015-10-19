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
