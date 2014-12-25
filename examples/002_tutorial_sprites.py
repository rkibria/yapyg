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

screen_width = 480
screen_height = 800
tile_size = 128
import yapyg.bootstrap
yapyg.bootstrap.initialize_screen(screen_width, screen_height)

from kivy.app import App
from yapyg import factory
from yapyg import tiles
from yapyg import entities
from yapyg_widgets.screen_widget import ScreenWidget

class TutorialApp(App):
        def build(self):
                state = factory.create(screen_width, screen_height, tile_size)
                tiles.add_tile_def(state, '+', ("assets/img/tiles/grid_simple.png",))
                tiles.set_area(state, [["+"] * 9] * 9)
                entities.insert(state,
                                "ball",
                                {
                                 "*": {
                                       "textures": ("assets/img/sprites/quarter_ball.png",),
                                       },
                                 },
                                (0, 0, 0,),
                                )
                return ScreenWidget(state, debugging=True)

TutorialApp().run()
