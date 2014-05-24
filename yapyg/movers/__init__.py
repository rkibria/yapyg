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
"""

from collections import deque

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
    state["movers"] = {}

def destroy(state):
    """
    TODO
    """
    del state["movers"]

def add(state, mover_name, mover, do_replace=False):
    """
    TODO
    """
    if not mover:
        raise YapygMoverException("%s was assigned null element" % mover_name)
    if do_replace:
        state["movers"][mover_name] = deque()
        state["movers"][mover_name].append(mover)
    else:
        if not state["movers"].has_key(mover_name):
            state["movers"][mover_name] = deque()
        state["movers"][mover_name].append(mover)

def get_active(state, mover_name):
    """
    TODO
    """
    if state["movers"].has_key(mover_name):
        return state["movers"][mover_name][0]
    else:
        return None

def get_type(state, mover):
    """
    TODO
    """
    return mover["type"]

def remove(state, mover_name):
    """
    TODO
    """
    state["movers"][mover_name].popleft()
    if len(state["movers"][mover_name]) == 0:
        del state["movers"][mover_name]

def run(state, frame_time_delta):
    """
    TODO
    """
    movers_to_delete = []
    for mover_name, mover_deque in state["movers"].iteritems():
        mover = mover_deque[0]
        (mover["run"])(state, mover_name, mover, frame_time_delta, movers_to_delete)

    movers_to_insert = []
    for mover_name, on_end_function in movers_to_delete:
        remove(state, mover_name)

    for mover_name, mover in movers_to_insert:
        insert(state, mover_name, mover)

    for mover_name, on_end_function in movers_to_delete:
        if on_end_function:
            (on_end_function)(state, mover_name)
