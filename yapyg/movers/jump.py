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
Immediate position change mover
"""

from kivy.logger import Logger

from .. import movers
from .. import entities

def add(state, entity_name, new_pos=None, new_rot=None, on_end_function=None, do_replace=False):
    """
    TODO
    """
    movers.add(state, entity_name, create(entity_name, new_pos, new_rot, on_end_function), do_replace)

def create(entity_name, new_pos, new_rot=None, on_end_function=None):
    """
    TODO
    """
    return {
            "type": "jump",
            "entity_name": entity_name,
            "new_pos": new_pos,
            "new_rot": new_rot,

            "run": run,
            "on_end_function": on_end_function,
        }

def run(state, entity_name, mover, frame_time_delta, movers_to_delete):
    """
    TODO
    """
    if mover["new_pos"]:
        entities.set_pos(state, entity_name, mover["new_pos"][0], mover["new_pos"][1])

    if mover["new_rot"]:
        entities.get_rot(state, entity_name)[0] = mover["new_rot"]

    movers_to_delete.append((entity_name, mover["on_end_function"]))
