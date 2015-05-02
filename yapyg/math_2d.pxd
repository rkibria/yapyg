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

cpdef float dot_product(tuple v_1, tuple v_2)
cpdef tuple vector_product(tuple vec, float factor)
cpdef tuple vector_div(tuple vec, float factor)
cpdef tuple vector_diff(tuple v_1, tuple v_2)
cpdef tuple vector_sum(tuple v_1, tuple v_2)
cpdef tuple components(tuple normal_vector, tuple v_vector)
cpdef tuple complex_multiply(tuple complex_1, tuple complex_2)
cpdef tuple rotated_point(tuple origin_point, tuple point, float rot)
cpdef float length(tuple vector)
cpdef float distance(tuple pos_1, tuple pos_2)
cpdef tuple unit_vector(tuple pos_1, tuple pos_2)
cpdef tuple get_unit_vector(tuple vector)
cpdef float heading_from_to(tuple pos1, tuple pos2)
