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
Generate new game states
"""


import screen
import tiles
import texture_db
import sprites
import movers
import entities
import view
import controls
import collisions
import text
import timer
import debug
import user
import fixpoint

def create(screen_width, screen_height, tile_size, origin_xy=(0, 0)):
        """
        TODO
        """
        state = [None for x in xrange(13)]
        tile_size = fixpoint.int2fix(tile_size)
        screen_width = fixpoint.int2fix(screen_width)
        screen_height = fixpoint.int2fix(screen_height)
        origin_xy = (fixpoint.int2fix(origin_xy[0]), fixpoint.int2fix(origin_xy[1]))

        screen.initialize(0, state, screen_width, screen_height, tile_size, origin_xy)
        texture_db.initialize(1, state)
        tiles.initialize(2, state, tile_size)
        sprites.initialize(3, state)
        movers.initialize(4, state)
        entities.initialize(5, state)
        view.initialize(6, state)
        controls.initialize(7, state)
        collisions.initialize(8, state)
        text.initialize(9, state)
        timer.initialize(10, state)
        debug.initialize(11, state)
        user.initialize(12, state)

        return state

def destroy(state):
        """
        TODO
        """
        screen.destroy(state)
        texture_db.destroy(state)
        tiles.destroy(state)
        sprites.destroy(state)
        movers.destroy(state)
        entities.destroy(state)
        view.destroy(state)
        controls.destroy(state)
        collisions.destroy(state)
        text.destroy(state)
        timer.destroy(state)
        debug.destroy(state)
        user.destroy(state)
