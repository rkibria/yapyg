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

def create(screen_width, screen_height, tile_size, origin_xy=(0, 0)):
    """
    TODO
    """
    state = {}

    screen.initialize(state, screen_width, screen_height, tile_size, origin_xy)
    texture_db.initialize(state)
    tiles.initialize(state, tile_size)
    sprites.initialize(state)
    movers.initialize(state)
    entities.initialize(state)
    view.initialize(state)
    controls.initialize(state)
    collisions.initialize(state)
    text.initialize(state)
    timer.initialize(state)

    return state

def destroy(state):
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
