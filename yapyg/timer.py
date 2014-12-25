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
Timer
"""


IDX_STATE_TIMER = None

IDX_TIMERS_TABLE = 0

def initialize(state_idx, state):
        """
        TODO
        """
        global IDX_STATE_TIMER
        IDX_STATE_TIMER = state_idx
        state[IDX_STATE_TIMER] = [[],]

def destroy(state):
        """
        TODO
        """
        state[IDX_STATE_TIMER] = None

def create(state, handler, timeout_ms=0):
        """
        TODO
        """
        state[IDX_STATE_TIMER][IDX_TIMERS_TABLE].append([handler, timeout_ms, 0])

def run(state, last_frame_delta):
        """
        TODO
        """
        for entry in state[IDX_STATE_TIMER][IDX_TIMERS_TABLE]:
                handler, timeout_ms, sum_time = entry
                sum_time += last_frame_delta
                if sum_time >= timeout_ms:
                        entry[2] = sum_time - timeout_ms
                        (handler)(state, last_frame_delta)
                else:
                        entry[2] = sum_time
