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
Main screen/window
"""

from kivy.core.window import Window
from kivy.logger import Logger

cdef int IDX_STATE_SCREEN = 0

cdef int IDX_SCREEN_WIDTH = 0
cdef int IDX_SCREEN_HEIGHT = 1
cdef int IDX_SCREEN_TILE_SIZE = 2
cdef int IDX_SCREEN_ORIGIN_XY = 3
cdef int IDX_SCREEN_SCREEN_SCALE = 4

cpdef initialize(int state_idx, list state, int screen_width, int screen_height, int tile_size, tuple origin_xy=(0, 0)):
        """
        TODO
        """
        global IDX_STATE_SCREEN
        IDX_STATE_SCREEN = state_idx

        cdef int win_w = Window.width
        cdef int win_h = Window.height
        Logger.info("YAPYG window w %d h %d" % (win_w, win_h))

        cdef float screen_scale_x = float(Window.width) / screen_width
        cdef float screen_scale_y = float(Window.height) / screen_height
        state[IDX_STATE_SCREEN] = [
                                   float(screen_width),
                                   float(screen_height),
                                   float(tile_size),
                                   [
                                    origin_xy[0] * screen_scale_x,
                                    origin_xy[1] * screen_scale_y,
                                    ],
                                   (
                                    screen_scale_x,
                                    screen_scale_y,
                                    ),
                                   ]
        Logger.info("YAPYG screen w %f h %f tile %f scale %s" % (get_width(state), get_height(state), get_tile_size(state), str(get_screen_scale(state))))

cpdef destroy(list state):
        """
        TODO
        """
        state[IDX_STATE_SCREEN] = None

cpdef float get_width(list state):
        """
        TODO
        """
        return state[IDX_STATE_SCREEN][IDX_SCREEN_WIDTH]

cpdef float get_height(list state):
        """
        TODO
        """
        return state[IDX_STATE_SCREEN][IDX_SCREEN_HEIGHT]

cpdef float get_tile_size(list state):
        """
        TODO
        """
        return state[IDX_STATE_SCREEN][IDX_SCREEN_TILE_SIZE]

cpdef set_origin(list state, tuple origin_xy):
        """
        TODO
        """
        cdef list screen_origin = state[IDX_STATE_SCREEN][IDX_SCREEN_ORIGIN_XY]
        screen_origin[0] = float(origin_xy[0])
        screen_origin[1] = float(origin_xy[1])

cpdef tuple get_origin(list state):
        """
        TODO
        """
        cdef list origin_xy = state[IDX_STATE_SCREEN][IDX_SCREEN_ORIGIN_XY]
        return (origin_xy[0], origin_xy[1])

cpdef tuple get_screen_scale(list state):
        """
        TODO
        """
        return state[IDX_STATE_SCREEN][IDX_SCREEN_SCREEN_SCALE]
