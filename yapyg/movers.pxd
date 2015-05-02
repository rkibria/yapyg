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
General movements
"""

cdef int IDX_STATE_MOVERS

cpdef int IDX_MOVER_TYPE = 0
cpdef int IDX_MOVER_RUN_FUNCTION = 1
cpdef int IDX_MOVER_ENTITY_NAME = 2
cpdef int IDX_MOVER_COLLISION_HANDLER = 3

cpdef initialize(int state_idx, list state)
cpdef destroy(list state)
cpdef add(list state, str mover_name, list mover, int do_replace=*)
cpdef get_active(list state, str mover_name)
cpdef get_type(list state, list mover)
cpdef remove(list state, str mover_name)
cpdef delete(list state, str mover_name)

cdef void run(list state, float frame_time_delta)
