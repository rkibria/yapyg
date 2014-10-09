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

"""

import yapyg.movers
import yapyg.controls
import yapyg.entities
import yapyg.fixpoint

IDX_FLIPPER_MOVER_ENTITY_NAME = 2
IDX_FLIPPER_MOVER_ANGLE = 3

def add(state, entity_name, do_replace=False):
        """
        """
        yapyg.movers.add(state, entity_name, create(entity_name), do_replace)

def create(entity_name):
        """

        """
        return ["flipper",
                run,
                entity_name,
                0,
                ]

def run(state, entity_name, mover, frame_time_delta, movers_to_delete):
        """
        TODO
        """
        orig_x = yapyg.fixpoint.float2fix(0.3)
        orig_y = yapyg.fixpoint.float2fix(0.75)
        current_angle = mover[IDX_FLIPPER_MOVER_ANGLE]
        current_angle = yapyg.fixpoint.float2fix(30.0)

#         yapyg.entities.set_pos(state, entity_name, orig_x, orig_y, current_angle)
        yapyg.entities.add_pos(state, entity_name, 0, 0, yapyg.fixpoint.int2fix(1))

        collision_result = yapyg.collisions.run(state, entity_name)
        if collision_result:
                yapyg.entities.undo_last_move(state, entity_name)
