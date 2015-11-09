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

from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.core.window import Window

cimport yapyg.movers
cimport yapyg.sprites
cimport yapyg.tiles
cimport yapyg.view

import yapyg.factory
import yapyg.timer

cdef float FRAME_DELTA_SECONDS = 1.0 / 30.0
cdef int MAX_FRAME_DELTA_MICROSECONDS = int(FRAME_DELTA_SECONDS * 1000.0)

class DisplayWidget(Widget):
        def __init__(self,
                     state,
                     **kwargs
                     ):
                """
                TODO
                """
                super(DisplayWidget, self).__init__(**kwargs)

                self.state = state
                self.redraw_tiles = [True]

                self.frame_time = 0
                Clock.schedule_interval(self.on_timer, timeout=FRAME_DELTA_SECONDS)

        def destroy(self):
                """
                TODO
                """
                Clock.unschedule(self.on_timer)
                state = self.state
                self.state = None
                yapyg.factory.destroy(state)

        def on_timer(self, dt):
                """
                TODO
                """
                cdef int cur_fps
                cdef int last_frame_delta
                if self.state:
                        cur_fps = int(Clock.get_fps())
                        if cur_fps > 0:
                                last_frame_delta = 1000 / cur_fps # milliseconds

                                if last_frame_delta < MAX_FRAME_DELTA_MICROSECONDS:
                                        self.frame_time = last_frame_delta
                                else:
                                        self.frame_time = MAX_FRAME_DELTA_MICROSECONDS

                                yapyg.timer.run(self.state, self.frame_time)
                                redraw(
                                       self.state,
                                       self.frame_time,
                                       self.redraw_tiles,
                                       self.canvas
                                       )

        def get_frame_time(self):
                """
                TODO
                """
                return self.frame_time

        def enable_redraw_tiles(self, value):
                """
                TODO
                """
                self.redraw_tiles = value
                if value:
                        redraw(
                               self.state,
                               MAX_FRAME_DELTA_MICROSECONDS,
                               self.redraw_tiles,
                               self.canvas,
                               )

cdef void redraw(list state, int frame_time_delta, list redraw_tiles, canvas):
        """
        TODO
        """
        yapyg.movers.run(state, frame_time_delta)

        if yapyg.view.run(state):
                redraw_tiles[0] = True

        if redraw_tiles[0]:
                yapyg.tiles.draw(state, canvas)
                redraw_tiles[0] = False

        yapyg.sprites.draw(state, canvas, frame_time_delta)
