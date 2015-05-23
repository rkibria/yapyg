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

screen_width = 480
screen_height = 800
tile_size = 128
import yapyg.bootstrap
yapyg.bootstrap.initialize_screen(screen_width, screen_height)

from kivy.app import App
from yapyg import factory
from yapyg import tiles
from yapyg import entities

from yapyg import collisions
from yapyg import debug
from yapyg_widgets.screen_widget import ScreenWidget
from yapyg_helpers import tiles_helpers
from yapyg_movers import linear_mover

class TutorialApp(App):
        def build(self):
                state = factory.create(screen_width, screen_height, tile_size)

                tiles.add_tile_def(state, ' ', ("assets/img/tiles/blank.png",))
                tiles.add_tile_def(state, '+', ("assets/img/tiles/block.png",),
                                   (("rectangle", 0, 0, 1, 1),))
                area_strings = (
                        "    ",
                        " +  ",
                        "    ",
                        " +  ",
                        "    ",
                        )
                tiles.set_area(state, tiles_helpers.strings_to_chars(area_strings))

                collisions.set_handler(state, collision_handler)

                BALL_SIZE = (1.0 / 4.0)
                CIRCLE_RADIUS = BALL_SIZE / 2
                entities.insert(state,
                                "ball",
                                {
                                 "*": {
                                       "textures": ("assets/img/sprites/quarter_ball.png",),
                                       },
                                 },
                                (1.25, 0, 0,),
                                collision=(("circle", CIRCLE_RADIUS, CIRCLE_RADIUS, CIRCLE_RADIUS,),)
                                )

                linear_mover.add(state, "ball", (0, 7), 1.5)

                return ScreenWidget(state, debugging=True)

def collision_handler(state, collisions_list):
        for entity_name_1, entity_name_2 in collisions_list:
                debug.set_line(state, 0, "collision: %s <-> %s" % (entity_name_1, entity_name_2,))

TutorialApp().run()
