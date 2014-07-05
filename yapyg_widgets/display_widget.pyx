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

from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.core.window import Window

cimport yapyg.fixpoint
cimport yapyg.movers
cimport yapyg.sprites
cimport yapyg.tiles

import yapyg.view
import yapyg.factory
import yapyg.timer

from yapyg.fixpoint import float2fix

MIN_FRAME_DELTA = yapyg.fixpoint.int2fix(1000)

class DisplayWidget(Widget):
        def __init__(self,
                        state,
                        view_size,
                        scale,
                        **kwargs
                ):
                """
                TODO
                """
                super(DisplayWidget, self).__init__(**kwargs)

                self.view_size = (view_size[0], view_size[1])
                self.scale = scale
                self.state = state
                self.redraw_tiles = [True]

                self.frame_time = 0
                Clock.schedule_once(self.on_timer, timeout=0)

        def destroy(self):
                """
                TODO
                """
                state = self.state
                self.state = None
                yapyg.factory.destroy(state)

        def on_timer(self, dt):
                """
                TODO
                """
                cdef int cur_fps
                if self.state:
                        cur_fps = float2fix(float(Clock.get_fps()))
                        if cur_fps > 0:
                                last_frame_delta = yapyg.fixpoint.div(yapyg.fixpoint.FIXP_1000, cur_fps) # milliseconds

                                if last_frame_delta < MIN_FRAME_DELTA:
                                        self.frame_time = last_frame_delta
                                else:
                                        self.frame_time = MIN_FRAME_DELTA

                                yapyg.timer.run(self.state, self.frame_time)
                                c_redraw(self.state, self.frame_time, self.redraw_tiles, self.scale, self.canvas, self.view_size)

                if self.state:
                        Clock.schedule_once(self.on_timer, timeout=0)

        def get_frame_time(self):
                return self.frame_time

        def enable_redraw_tiles(self, value):
                """
                TODO
                """
                self.redraw_tiles = value
                if value:
                        c_redraw(self.state, float2fix(0.01), self.redraw_tiles, self.scale, self.canvas, self.view_size)

cdef void c_redraw(list state, int frame_time_delta, list redraw_tiles, int scale, canvas, tuple view_size):
        """
        TODO
        """
        yapyg.movers.c_run(state, frame_time_delta)

        if yapyg.view.run(state):
                redraw_tiles[0] = True

        if redraw_tiles[0]:
                yapyg.tiles.c_draw(state, scale, canvas, view_size)
                redraw_tiles[0] = False

        yapyg.sprites.c_draw(state, canvas, frame_time_delta, scale)
