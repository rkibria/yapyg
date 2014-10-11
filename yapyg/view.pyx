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
View setter
"""

cimport globals

cdef int IDX_VIEW_POS = 0
cdef int IDX_VIEW_SETTER = 1

cpdef initialize(list state):
        """
        TODO
        """
        state[globals.IDX_STATE_VIEW] = [
                [0, 0],
                None,]

cpdef destroy(list state):
        """
        TODO
        """
        state[globals.IDX_STATE_VIEW] = None

cpdef tuple get_view_pos(list state):
        """
        TODO
        """
        return tuple(state[globals.IDX_STATE_VIEW][IDX_VIEW_POS])

cpdef set_view_pos(list state, view_pos):
        """
        TODO
        """
        cdef list vp = state[globals.IDX_STATE_VIEW][IDX_VIEW_POS]
        vp[0] = view_pos[0]
        vp[1] = view_pos[1]

cpdef set_viewer(list state, viewer):
        """
        TODO
        """
        state[globals.IDX_STATE_VIEW][IDX_VIEW_SETTER] = viewer

cpdef int run(list state):
        """
        TODO
        """
        setter = state[globals.IDX_STATE_VIEW][IDX_VIEW_SETTER]
        if setter:
                return (setter[0])(state, setter)
        else:
                return False
