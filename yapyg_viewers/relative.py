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
TODO
"""
from kivy.logger import Logger

import yapyg.view
import yapyg.entities
import yapyg.fixpoint

IDX_RELATIVE_VIEW_ENTITY = 1
IDX_RELATIVE_VIEW_OFFSET = 2

def create(state, entity_name, offset):
        """
        TODO
        """
        return [run,
                entity_name,
                (offset[0], offset[1]),
                ]

def run(state, viewer):
        """
        TODO
        """
        old_view_pos = yapyg.view.get_view_pos(state)
        entity_pos = yapyg.entities.get_pos(state, viewer[IDX_RELATIVE_VIEW_ENTITY])
        new_view_pos = [entity_pos[0] + viewer[IDX_RELATIVE_VIEW_OFFSET][0],
                entity_pos[1] + viewer[IDX_RELATIVE_VIEW_OFFSET][1]]
        if old_view_pos != new_view_pos:
                yapyg.view.set_view_pos(state, new_view_pos)
                return True
        else:
                return False
