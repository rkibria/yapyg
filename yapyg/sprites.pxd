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
2D Sprites
"""

cdef int IDX_STATE_SPRITES

cpdef initialize(int state_idx, list state)
cpdef destroy(list state)
cpdef insert(list state, str sprite_name, tuple textures, float speed, list pos_offset,
             tuple scale, int enable, list pos, int screen_relative=*, int play_once=*)
cpdef delete(list state, str sprite_name)
cpdef list get(list state, str sprite_name)
cpdef tuple get_pos(list state, str sprite_name)
cpdef set_enable(list state, str sprite_name, int enable)
cdef void draw(list state, canvas, float frame_time_delta)
