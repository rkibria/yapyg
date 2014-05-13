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
Controller-influenced mover
"""

from kivy.logger import Logger

from .. import movers
from .. import controls
from .. import entities

def add(state, entity_name, controller, factor, limits, on_end_function=None, do_replace=False):
    """
    TODO
    """
    movers.add(state, entity_name, create(entity_name, controller, factor, limits, on_end_function), do_replace)

def create(entity_name, controller, factor, limits, on_end_function=None):
    """
    TODO
    """
    return {
            "entity_name": entity_name,
            "controller": controller,
            "factor": factor,
            "limits": limits,

            "run": run,
            "on_end_function": on_end_function,
        }

def run(state, entity_name, mover, frame_time_delta, movers_to_delete):
    """
    TODO
    """
    direction = controls.get_joystick(state)
    pos = entities.get_pos(state, entity_name)
    factor = mover["factor"]
    limits = mover["limits"]

    new_x = pos[0] + factor * direction[0]
    if new_x < limits[0]:
        new_x = limits[0]
    elif new_x > limits[2]:
        new_x = limits[2]

    new_y = pos[1] + factor * direction[1]
    if new_y < limits[1]:
        new_y = limits[1]
    elif new_y > limits[3]:
        new_y = limits[3]

    pos[0] = new_x
    pos[1] = new_y
