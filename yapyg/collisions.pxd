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
Collisions
"""

cdef int IDX_STATE_COLLISIONS

cdef int IDX_COLLISIONDB_ENTITIES
cdef int IDX_COLLISIONDB_HASH_MAP
cdef int IDX_COLLISIONDB_HANDLER_FUNCTION
cdef int IDX_COLLISIONDB_COLLISIONS_LIST

cdef int IDX_COLLISION_SHAPES
cdef int IDX_COLLISION_LAST_POS
cdef int IDX_COLLISION_CACHE

cdef int IDX_COLLISION_CACHE_ABS_SHAPE
cdef int IDX_COLLISION_CACHE_HASH_EXTENT
cdef int IDX_COLLISION_CACHE_LAST_HASH_POS

cpdef initialize(int state_idx, list state)
cpdef destroy(list state)
cpdef entity_pos_listener(list state, str entity_name, tuple pos)
cpdef set_handler(list state, handler_function)
cpdef add_entity(list state, str entity_name, tuple shapes_list)
cpdef delete(list state, str entity_name)
cpdef add_tile(list state, str tile_name, int x, int y, tuple shapes_list)

cpdef update_hash(list state, str entity_name, tuple new_pos, int is_tile)
cpdef tuple get_hash_area(list state, str entity_name, tuple entity_lower_left, int is_tile)
cpdef remove_hash_entries(list state, str entity_name, tuple entity_lower_left)
cpdef list get_collision_shapes(list state, str entity_name, list collision_def)
cpdef tuple run(list state, str entity_name_1)
cpdef clear_collisions_list(list state)
cpdef notify_collision_handler(list state)
