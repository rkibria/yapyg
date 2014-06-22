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

cimport fixpoint
cimport movers
cimport sprites
cimport tiles

import view
import factory
import timer

MIN_FRAME_DELTA = fixpoint.int2fix(35)

class YapygWidget(Widget):
        def __init__(self,
                        state,
                        view_size,
                        scale,
                        **kwargs
                ):
                super(YapygWidget, self).__init__(**kwargs)

                self.view_size = (fixpoint.float2fix(float(view_size[0])), fixpoint.float2fix(float(view_size[1])))
                self.scale = fixpoint.float2fix(float(scale))
                self.state = state
                self.redraw_tiles = [True]

                self.min_frame_time_delta = 0
                Clock.schedule_once(self.on_timer, timeout=0)

        def destroy(self):
                state = self.state
                self.state = None
                factory.destroy(state)

        def on_timer(self, dt):
                if self.state:
                        cur_fps = fixpoint.float2fix(float(Clock.get_fps()))
                        if cur_fps > 0:
                                last_frame_delta = fixpoint.div(fixpoint.FIXP_1000, cur_fps) # milliseconds
                                if self.min_frame_time_delta == 0 or last_frame_delta < self.min_frame_time_delta:
                                        self.min_frame_time_delta = last_frame_delta
                                else:
                                        last_frame_delta = self.min_frame_time_delta

                                if last_frame_delta < MIN_FRAME_DELTA:
                                        timer.run(self.state, last_frame_delta)
                                        c_redraw(self.state, last_frame_delta, self.redraw_tiles, self.scale, self.canvas, self.view_size)

                if self.state:
                        Clock.schedule_once(self.on_timer, timeout=0)

        def enable_redraw_tiles(self, value):
                self.redraw_tiles = value
                if value:
                        c_redraw(self.state, fixpoint.float2fix(0.01), self.redraw_tiles, self.scale, self.canvas, self.view_size)

cdef void c_redraw(list state, int frame_time_delta, list redraw_tiles, int scale, canvas, tuple view_size):
        movers.c_run(state, frame_time_delta)

        if view.run(state):
                redraw_tiles[0] = True

        if redraw_tiles[0]:
                tiles.c_draw(state, scale, canvas, view_size)
                redraw_tiles[0] = False

        sprites.c_draw(state, canvas, frame_time_delta, scale)
