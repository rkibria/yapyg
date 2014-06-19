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

- movers are lists with 0=type, 1=run-function
"""

from collections import deque

from .. import globals
from .. import collisions
from .. import fixpoint

IDX_MOVER_TYPE = 0
IDX_MOVER_RUN_FUNCTION = 1
IDX_MOVER_ENTITY_NAME = 2

class YapygMoverException(Exception):
        """
        TODO
        """
        def __init__(self, value):
                """
                TODO
                """
                self.value = value

        def __str__(self):
                """
                TODO
                """
                return repr(self.value)

def initialize(state):
        """
        TODO
        """
        state[globals.IDX_STATE_MOVERS] = {}

def destroy(state):
        """
        TODO
        """
        state[globals.IDX_STATE_MOVERS] = None

def add(state, mover_name, mover, do_replace=False):
        """
        TODO
        """
        if not mover:
                raise YapygMoverException("%s was assigned null element" % mover_name)
        if do_replace:
                state[globals.IDX_STATE_MOVERS][mover_name] = deque()
                state[globals.IDX_STATE_MOVERS][mover_name].append(mover)
        else:
                if not state[globals.IDX_STATE_MOVERS].has_key(mover_name):
                        state[globals.IDX_STATE_MOVERS][mover_name] = deque()
                state[globals.IDX_STATE_MOVERS][mover_name].append(mover)

def get_active(state, mover_name):
        """
        TODO
        """
        if state[globals.IDX_STATE_MOVERS].has_key(mover_name):
                return state[globals.IDX_STATE_MOVERS][mover_name][0]
        else:
                return None

def get_type(state, mover):
        """
        TODO
        """
        return mover[IDX_MOVER_TYPE]

def remove(state, mover_name):
        """
        TODO
        """
        state[globals.IDX_STATE_MOVERS][mover_name].popleft()
        if len(state[globals.IDX_STATE_MOVERS][mover_name]) == 0:
                del state[globals.IDX_STATE_MOVERS][mover_name]

def run(state, frame_time_delta):
        """
        TODO
        """
        movers_to_delete = []
        collisions_run_func = collisions.run
        for mover_name, mover_deque in state[globals.IDX_STATE_MOVERS].iteritems():
                mover = mover_deque[0]
                (mover[IDX_MOVER_RUN_FUNCTION])(state, mover_name, mover, frame_time_delta, movers_to_delete)
                
                collisions_run_func(state, mover[IDX_MOVER_ENTITY_NAME])

        for mover_name, on_end_function in movers_to_delete:
                remove(state, mover_name)

        for mover_name, on_end_function in movers_to_delete:
                if on_end_function:
                        (on_end_function)(state, mover_name)
