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
Simple linear mover
"""

from kivy.logger import Logger

from .. import geometry
from .. import movers

def add(state, mover_name, pos_var, rot_var, new_pos, speed, do_rotate = False, on_end_function=None, do_replace=False):
    """
    TODO
    """
    movers.add(state, mover_name, create(pos_var, rot_var, new_pos, speed, do_rotate, on_end_function), do_replace)

def create(pos_var, rot_var, rel_vector, speed, do_rotate, on_end_function):
    """
    TODO
    """
    distance = geometry.get_vector_size(rel_vector)
    travel_time = distance / speed
    travel_vector = [rel_vector[0] / travel_time, rel_vector[1] / travel_time]
    return {
            "passed_time": 0,
            "pos_var": pos_var,
            "rot_var": rot_var,
            "speed": speed,
            "travel_vector": travel_vector,
            "travel_time": travel_time,
            "run": run,
            "do_rotate": do_rotate,
            "on_end_function": on_end_function,
        }

def run(state, mover_name, mover, frame_time_delta, movers_to_delete):
    """
    TODO
    """
    travel_time = mover["travel_time"]
    travel_vector = mover["travel_vector"]
    passed_time = mover["passed_time"]

    if passed_time == 0 and mover["do_rotate"]:
        mover["rot_var"][0] = (int(geometry.get_rotation([0, 0], travel_vector)) - 90) % 360

    passed_time += frame_time_delta
    if passed_time > travel_time:
        passed_time = travel_time
    mover["passed_time"] = passed_time

    mover["pos_var"][0] += frame_time_delta * travel_vector[0]
    mover["pos_var"][1] += frame_time_delta * travel_vector[1]

    if passed_time == travel_time:
        movers_to_delete.append((mover_name, mover["on_end_function"]))
