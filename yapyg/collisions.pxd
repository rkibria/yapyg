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

cpdef initialize(list state)
cpdef destroy(list state)
cpdef entity_pos_listener(list state, str entity_name, tuple pos)
cpdef set_handler(list state, handler_function)
cpdef add(list state, str entity_name, tuple shapes_list)
cpdef delete(list state, str entity_name)

cdef void c_update_hash(list state, str entity_name, tuple new_pos)
cdef tuple c_get_hash_area(list state, str entity_name, tuple entity_lower_left)
cdef void c_remove_hash_entries(list state, str entity_name, tuple entity_lower_left)
cdef list c_get_collision_shapes(list state, str entity_name, list collision_def)
cdef tuple c_run(list state, str entity_name_1)
cdef void c_clear_collisions_list(list state)
cdef void c_notify_collision_handler(list state)
