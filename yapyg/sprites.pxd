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
2D Sprites
"""

cpdef initialize(list state)
cpdef destroy(list state)
cpdef insert(list state, str sprite_name, tuple textures, int speed, list pos_offset, tuple scale, int enable, list pos, list rot_list, int screen_relative=*)
cpdef delete(list state, str sprite_name)
cpdef list get(list state, str sprite_name)
cpdef tuple get_pos(list state, str sprite_name)
cpdef int get_rot(list state, str sprite_name)
cpdef set_enable(list state, str sprite_name, int enable)

cdef void c_draw_sprite(list state, canvas, tuple view_pos, int view_scale, str sprite_name, texture, list pos, list scale, int rotate, tuple origin_xy, int screen_relative)
cdef void c_draw(list state, canvas, int frame_time_delta, int view_scale)
