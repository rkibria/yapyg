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

- movers are lists with 0=type(str), 1=run-function, 2=entity_name

mover_db = dict[entity_name] : deque(movers)

e.g. MOVE(+x,+y), WAIT(x sec), SET_PROPERTY(".."), ...


"""

from collections import deque

cimport collisions
cimport entities

cdef int IDX_STATE_MOVERS

cdef int IDX_MOVER_TYPE = 0
cdef int IDX_MOVER_RUN_FUNCTION = 1
cdef int IDX_MOVER_ENTITY_NAME = 2
cdef int IDX_MOVER_COLLISION_HANDLER = 3

IDX_MOVER_FIRST_PARAMETER = IDX_MOVER_COLLISION_HANDLER + 1

G_IDX_MOVER_RUN_FUNCTION = IDX_MOVER_RUN_FUNCTION

cpdef initialize(int state_idx, list state):
        """
        TODO
        """
        global IDX_STATE_MOVERS
        IDX_STATE_MOVERS = state_idx
        state[IDX_STATE_MOVERS] = {}

cpdef destroy(list state):
        """
        TODO
        """
        state[IDX_STATE_MOVERS] = None

cpdef add(list state, str mover_name, list mover, int do_replace=False, int prepend=False):
        """
        TODO
        """
        cdef dict movers_dict = state[IDX_STATE_MOVERS]
        if do_replace:
                movers_dict[mover_name] = deque()
                movers_dict[mover_name].append(mover)
        else:
                if not movers_dict.has_key(mover_name):
                        movers_dict[mover_name] = deque()
                if not prepend:
                        movers_dict[mover_name].append(mover)
                else:
                        movers_dict[mover_name].appendleft(mover)

cpdef get_active(list state, str mover_name):
        """
        TODO
        """
        cdef dict movers_dict = state[IDX_STATE_MOVERS]
        if movers_dict.has_key(mover_name):
                return movers_dict[mover_name][0]
        else:
                return None

cpdef get_type(list state, list mover):
        """
        TODO
        """
        return mover[IDX_MOVER_TYPE]

cpdef remove(list state, str mover_name):
        """
        TODO
        """
        cdef dict movers_dict = state[IDX_STATE_MOVERS]
        movers_dict[mover_name].popleft()
        if len(movers_dict[mover_name]) == 0:
                del movers_dict[mover_name]

cpdef delete(list state, str mover_name):
        """
        TODO
        """
        cdef dict movers_dict = state[IDX_STATE_MOVERS]
        if movers_dict.has_key(mover_name):
                del movers_dict[mover_name]

cdef void run(list state, float frame_time_delta):
        """
        TODO
        """
        cdef dict movers_dict = state[IDX_STATE_MOVERS]
        collisions.clear_collisions_list(state)
        cdef list movers_to_delete = []
        cdef list entities_to_delete = []
        cdef str mover_name
        cdef list mover
        for mover_name, mover_deque in movers_dict.iteritems():
                if mover_deque:
                        mover = mover_deque[0]
                        (mover[IDX_MOVER_RUN_FUNCTION])(state, mover_name, mover, frame_time_delta, movers_to_delete)

        for mover_to_delete in movers_to_delete:
                if mover_to_delete:
                        mover_name = mover_to_delete[0]
                        remove(state, mover_name)

        for mover_to_delete in movers_to_delete:
                if len(mover_to_delete) > 2:
                        mover_name = mover_to_delete[0]
                        delete_entity = mover_to_delete[2]
                        if delete_entity:
                                entities.delete(state, mover_name)

        for mover_to_delete in movers_to_delete:
                if mover_to_delete:
                        mover_name = mover_to_delete[0]
                        on_end_function = mover_to_delete[1]
                        if on_end_function:
                                (on_end_function)(state, mover_name)

        collisions.notify_collision_handler(state)
