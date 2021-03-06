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
Texture storage and operations
"""

cdef int IDX_STATE_TEXTURE_DB

cpdef initialize(int state_idx, list state)
cpdef destroy(list state)
cpdef tuple insert(list state, str texture_name, texture)
cpdef tuple load(list state, str texture_name, str texture_filename)
cpdef get(list state, str texture_name)
cpdef tuple insert_combined(list state, float texture_size, str texture_name, tuple texture_list)
cpdef tuple insert_color_rect(list state, float texture_w, float texture_h, str texture_name, float c_r, float c_g, float c_b)
cpdef tuple insert_color_ellipse(list state, float texture_w, float texture_h, str texture_name, float c_r, float c_g, float c_b)
