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

import yapyg.movers
import yapyg.entities
import yapyg.fixpoint

IDX_JUMP_MOVER_NEW_POS = yapyg.movers.IDX_MOVER_FIRST_PARAMETER
IDX_JUMP_MOVER_ON_END_FUNCTION = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 1

def add(state, entity_name, new_pos=None, on_end_function=None, do_replace=False):
        """
        TODO
        """
        yapyg.movers.add(state, entity_name, create(entity_name, new_pos, on_end_function), do_replace)

def create(entity_name, new_pos, on_end_function=None):
        """
        TODO
        """
        return ["jump",
                run,
                entity_name,
                None,
                new_pos,
                on_end_function,]

def run(state, entity_name, mover, frame_time_delta, movers_to_delete):
        """
        TODO
        """
        if mover[IDX_JUMP_MOVER_NEW_POS]:
                new_pos = mover[IDX_JUMP_MOVER_NEW_POS]
                yapyg.entities.set_pos(state, entity_name, new_pos[0], new_pos[1], new_pos[2])

        movers_to_delete.append((entity_name, mover[IDX_JUMP_MOVER_ON_END_FUNCTION]))
