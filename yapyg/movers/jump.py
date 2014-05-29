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

from .. import movers
from .. import entities

IDX_JUMP_MOVER_ENTITY_NAME = 2
IDX_JUMP_MOVER_NEW_POS = 3
IDX_JUMP_MOVER_NEW_ROT = 4
IDX_JUMP_MOVER_ON_END_FUNCTION = 5

def add(state, entity_name, new_pos=None, new_rot=None, on_end_function=None, do_replace=False):
        """
        TODO
        """
        movers.add(state, entity_name, create(entity_name, new_pos, new_rot, on_end_function), do_replace)

def create(entity_name, new_pos, new_rot=None, on_end_function=None):
        """
        TODO
        """
        return ["jump",
                run,
                entity_name,
                new_pos,
                new_rot,
                on_end_function,]

def run(state, entity_name, mover, frame_time_delta, movers_to_delete):
        """
        TODO
        """
        if mover[IDX_JUMP_MOVER_NEW_POS]:
                entities.set_pos(state, entity_name, mover[IDX_JUMP_MOVER_NEW_POS][0], mover[IDX_JUMP_MOVER_NEW_POS][1])

        if mover[IDX_JUMP_MOVER_NEW_ROT]:
                entities.get_rot(state, entity_name)[0] = mover[IDX_JUMP_MOVER_NEW_ROT]

        movers_to_delete.append((entity_name, mover[IDX_JUMP_MOVER_ON_END_FUNCTION]))
