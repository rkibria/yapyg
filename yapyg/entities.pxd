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
Entities
"""

cdef int IDX_STATE_ENTITIES

cdef int IDX_ENTITIES_TABLE

cdef int IDX_ENTITY_POS
cdef int IDX_ENTITY_POS_OFFSET
cdef int IDX_ENTITY_ENABLED_SPRITE
cdef int IDX_ENTITY_LAST_POS
cdef int IDX_ENTITY_SPRITES
cdef int IDX_ENTITY_COLLISION

cpdef initialize(int state_idx, list state)
cpdef destroy(list state)
cpdef insert(list state, str entity_name, dict sprite_defs, tuple pos,
             tuple pos_offset=*, tuple collision=*, int screen_relative=*, int play_once=*)
cpdef set_sprite(list state, str entity_name, str sprite_name, dict sprite_def,
                 int enable=*, int screen_relative=*, int play_once=*)
cpdef set_active_sprite(list state, str entity_name, str sprite_name, int enable=?)
cpdef delete(list state, str entity_name)
cpdef list get(list state, str entity_name)
cpdef tuple get_pos(list state, str entity_name)
cpdef tuple get_last_pos(list state, str entity_name)
cpdef tuple get_pos_offset(list state, str entity_name)
cpdef set_pos(list state, str entity_name, int x_pos, int y_pos, int rot)
cpdef add_pos(list state, str entity_name, int x_pos, int y_pos, int rot)
cpdef undo_last_move(list state, str entity_name)

cdef c_call_pos_listeners(list state, str entity_name, tuple pos)
cdef str c_get_full_sprite_name(str entity_name, str sprite_name)
