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

from yapyg import factory
from yapyg import tiles
from yapyg import entities
from yapyg import controls
from yapyg import text
from yapyg import timer
from yapyg import collisions
from yapyg_movers import physical_mover
from yapyg_viewers import relative_viewer
from yapyg_movers import controlled_mover
from yapyg_helpers import entities_helpers
from yapyg_helpers import tiles_helpers

def create(screen_width, screen_height, tile_size):
        state = factory.create(screen_width, screen_height, tile_size)

        tiles.add_tile_def(state, ".", ("assets/img/tiles/grid_double.png",))
        tiles.set_area(state, [["." for x in xrange(10)] for x in xrange(10)])

        # controls.add_joystick(state)

        for x in xrange(100):
                for y in xrange(100):
                        ball_entity_name = "ball_%d_%d" % (x, y)
                        entities.insert(state,
                                        ball_entity_name,
                                        {
                                                "*": {
                                                      "textures": ("assets/img/sprites/half_ball.png",
                                                                   "assets/img/sprites/half_ball_2.png",
                                                                   ),
                                                      "speed" : 100.0,
                                                      },
                                        },
                                        (
                                                x * 0.5 - 0.25,
                                                y * 0.5 - 0.25,
                                                0,
                                        ),
                                        )

        return state
