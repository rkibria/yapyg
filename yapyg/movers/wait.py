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
Waitstate mover
"""

from .. import movers

def add(state, mover_name, wait_time, on_end_function=None, do_replace=False):
    """
    TODO
    """
    movers.add(state, mover_name, create(wait_time, on_end_function), do_replace)

def create(wait_time, on_end_function=None):
    """
    TODO
    """
    return {
            "type": "wait",
            "passed_time": 0,
            "wait_time": wait_time,
            "run": run,
            "on_end_function": on_end_function,
        }

def run(state, mover_name, mover, frame_time_delta, movers_to_delete):
    """
    TODO
    """
    passed_time = mover["passed_time"]
    wait_time = mover["wait_time"]

    passed_time += frame_time_delta
    if passed_time > wait_time:
        passed_time = wait_time
    mover["passed_time"] = passed_time

    if passed_time == wait_time:
        movers_to_delete.append((mover_name, mover["on_end_function"]))
