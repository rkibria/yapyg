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
2D Sprites
"""

import globals
import fixpoint

IDX_SCREEN_WIDTH = 0
IDX_SCREEN_HEIGHT = 1
IDX_SCREEN_TILE_SIZE = 2
IDX_SCREEN_ORIGIN_XY = 3

def initialize(state, screen_width, screen_height, tile_size, origin_xy=(0, 0)):
        """
        TODO
        """
        state[globals.IDX_STATE_SCREEN] = [
                screen_width,
                screen_height,
                tile_size,
                [origin_xy[0], origin_xy[1]],]

def destroy(state):
        """
        TODO
        """
        state[globals.IDX_STATE_SCREEN] = None

def get_width(state):
        """
        TODO
        """
        return state[globals.IDX_STATE_SCREEN][IDX_SCREEN_WIDTH]

def get_height(state):
        """
        TODO
        """
        return state[globals.IDX_STATE_SCREEN][IDX_SCREEN_HEIGHT]

def get_tile_size(state):
        """
        TODO
        """
        return state[globals.IDX_STATE_SCREEN][IDX_SCREEN_TILE_SIZE]

def set_origin(state, origin_xy):
        """
        TODO
        """
        state[globals.IDX_STATE_SCREEN][IDX_SCREEN_ORIGIN_XY][0] = origin_xy[0]
        state[globals.IDX_STATE_SCREEN][IDX_SCREEN_ORIGIN_XY][1] = origin_xy[1]

def get_origin(state):
        """
        TODO
        """
        origin_xy = state[globals.IDX_STATE_SCREEN][IDX_SCREEN_ORIGIN_XY]
        return (origin_xy[0], origin_xy[1])
