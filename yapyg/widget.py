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

import movers
import tiles
import sprites
import view
import factory
import timer
import fixpoint

MIN_FRAME_DELTA = fixpoint.int2fix(35)

class YapygWidget(Widget):
        def __init__(self,
                        state,
                        view_size,
                        scale,
                        **kwargs
                ):
                super(YapygWidget, self).__init__(**kwargs)

                self.view_size = [fixpoint.float2fix(float(view_size[0])), fixpoint.float2fix(float(view_size[1]))]
                self.scale = fixpoint.float2fix(float(scale))
                self.state = state
                self.redraw_tiles = True

                self.min_frame_time_delta = 0
                Clock.schedule_once(self.on_timer, timeout=0)

        def destroy(self):
                state = self.state
                self.state = None
                factory.destroy(state)

        def on_timer(self, dt):
                if self.state:
                        cur_fps = fixpoint.float2fix(float(Clock.get_fps())) # fixpoint
                        if cur_fps > 0:
                                last_frame_delta = fixpoint.div(fixpoint.FIXP_1000, cur_fps) # fixpoint, milliseconds
                                if self.min_frame_time_delta == 0 or last_frame_delta < self.min_frame_time_delta:
                                        self.min_frame_time_delta = last_frame_delta
                                else:
                                        last_frame_delta = self.min_frame_time_delta

                                if last_frame_delta < MIN_FRAME_DELTA:
                                        timer.run(self.state, last_frame_delta)
                                        self.redraw(last_frame_delta)

                if self.state:
                        Clock.schedule_once(self.on_timer, timeout=0)

        def redraw(self, frame_time_delta):
                movers.run(self.state, frame_time_delta)

                if view.run(self.state):
                        self.redraw_tiles = True

                if self.redraw_tiles:
                        tiles.draw(self.state, self.scale, self.canvas, self.view_size)
                        self.enable_redraw_tiles(False)

                sprites.draw(self.state, self.canvas, frame_time_delta, self.scale)

        def enable_redraw_tiles(self, value):
                self.redraw_tiles = value
                if value:
                        self.redraw(1)
