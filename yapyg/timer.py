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

def initialize(state):
    """
    TODO
    """
    state["timer"] = {
        "timers": [],
    }

def destroy(state):
    """
    TODO
    """
    del state["timer"]

def create(state, handler, timeout_us=0):
    """
    TODO
    """
    state["timer"]["timers"].append([handler, timeout_us, 0])

def run(state, last_frame_delta):
    """
    TODO
    """
    for entry in state["timer"]["timers"]:
        handler, timeout_us, sum_time = entry
        sum_time += last_frame_delta
        if sum_time >= timeout_us:
            entry[2] = sum_time - timeout_us
            (handler)(state, last_frame_delta)
        else:
            entry[2] = sum_time
