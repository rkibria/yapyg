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
General movements

- movers are lists with 0=type(str), 1=run-function, 2=entity_name

mover_db = dict[entity_name] : deque(movers)

e.g. MOVE(+x,+y), WAIT(x sec), SET_PROPERTY(".."), ...


"""

from collections import deque

cimport collisions
cimport globals

cpdef int IDX_MOVER_TYPE = 0
cpdef int IDX_MOVER_RUN_FUNCTION = 1
cpdef int IDX_MOVER_ENTITY_NAME = 2
cpdef int IDX_MOVER_COLLISION_HANDLER = 3

IDX_MOVER_FIRST_PARAMETER = IDX_MOVER_COLLISION_HANDLER + 1

cpdef initialize(list state):
        """
        TODO
        """
        state[globals.IDX_STATE_MOVERS] = {}

cpdef destroy(list state):
        """
        TODO
        """
        state[globals.IDX_STATE_MOVERS] = None

cpdef add(list state, str mover_name, list mover, int do_replace=False):
        """
        TODO
        """
        if do_replace:
                state[globals.IDX_STATE_MOVERS][mover_name] = deque()
                state[globals.IDX_STATE_MOVERS][mover_name].append(mover)
        else:
                if not state[globals.IDX_STATE_MOVERS].has_key(mover_name):
                        state[globals.IDX_STATE_MOVERS][mover_name] = deque()
                state[globals.IDX_STATE_MOVERS][mover_name].append(mover)

cpdef get_active(list state, str mover_name):
        """
        TODO
        """
        if state[globals.IDX_STATE_MOVERS].has_key(mover_name):
                return state[globals.IDX_STATE_MOVERS][mover_name][0]
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
        state[globals.IDX_STATE_MOVERS][mover_name].popleft()
        if len(state[globals.IDX_STATE_MOVERS][mover_name]) == 0:
                del state[globals.IDX_STATE_MOVERS][mover_name]

cdef void c_run(list state, int frame_time_delta):
        """
        TODO
        """
        collisions.clear_collisions_list(state)

        cdef list movers_to_delete
        movers_to_delete = []

        cdef str mover_name
        cdef list mover
        for mover_name, mover_deque in state[globals.IDX_STATE_MOVERS].iteritems():
                mover = mover_deque[0]
                (mover[IDX_MOVER_RUN_FUNCTION])(state, mover_name, mover, frame_time_delta, movers_to_delete)

        for mover_name, on_end_function in movers_to_delete:
                remove(state, mover_name)

        for mover_name, on_end_function in movers_to_delete:
                if on_end_function:
                        (on_end_function)(state, mover_name)

        collisions.notify_collision_handler(state)
