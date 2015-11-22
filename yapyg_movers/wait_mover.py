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
Waitstate mover
"""

import yapyg.movers


IDX_WAIT_MOVER_PASSED_TIME = yapyg.movers.IDX_MOVER_FIRST_PARAMETER
IDX_WAIT_MOVER_WAIT_TIME = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 1
IDX_WAIT_MOVER_ON_END_FUNCTION = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 2

def add(state, mover_name, wait_time, on_end_function=None, do_replace=False, prepend=False):
        """
        TODO
        """
        yapyg.movers.add(state, mover_name, create(mover_name, wait_time, on_end_function), do_replace, prepend)

def create(mover_name, wait_time, on_end_function=None):
        """
        TODO
        """
        return ["wait",
                run,
                mover_name,
                None,
                0,
                wait_time,
                on_end_function,]

def run(state, mover_name, mover, frame_time_delta, movers_to_delete):
        """
        TODO
        """
        passed_time = mover[IDX_WAIT_MOVER_PASSED_TIME]
        wait_time = mover[IDX_WAIT_MOVER_WAIT_TIME]

        passed_time += frame_time_delta / 1000.0
        if passed_time > wait_time:
                passed_time = wait_time
        mover[IDX_WAIT_MOVER_PASSED_TIME] = passed_time

        if passed_time == wait_time:
                movers_to_delete.append((mover_name, mover[IDX_WAIT_MOVER_ON_END_FUNCTION]))
