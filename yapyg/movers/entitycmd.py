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
Entity state setting mover
"""

from kivy.logger import Logger

from .. import movers
from .. import entities

def add(state, mover_name, entity_name, command, param_1, param_2=None, on_end_function=None, do_replace=False):
    """
    TODO
    """
    movers.add(state, mover_name, create(entity_name, command, param_1, param_2, on_end_function), do_replace)

def create(entity_name, command, param_1, param_2=None, on_end_function=None):
    """
    TODO
    """
    return {
            "entity_name": entity_name,
            "command": command,
            "param_1": param_1,
            "param_2": param_2,
            "run": run,
            "on_end_function": on_end_function,
        }

def run(state, mover_name, mover, frame_time_delta, movers_to_delete):
    """
    TODO
    """
    entity_name = mover["entity_name"]
    command = mover["command"]
    param_1 = mover["param_1"]
    param_2 = mover["param_2"]

    if command == "set_sprite":
        entities.set_sprite(state, entity_name, param_1)
    else:
        Logger.debug("ERROR: unknown command %s" % command)
        zzz()

    movers_to_delete.append((mover_name, mover["on_end_function"]))
