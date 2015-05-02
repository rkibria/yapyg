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

from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.window import Keyboard
from kivy.graphics import PushMatrix, Rectangle, PopMatrix

class JoystickWidget(Widget):
        KEYCODE_W = Keyboard.keycodes['w']
        KEYCODE_A = Keyboard.keycodes['a']
        KEYCODE_S = Keyboard.keycodes['s']
        KEYCODE_D = Keyboard.keycodes['d']

        def __init__(self,
                     deadzone=0,
                     joystickbkg_file="assets/img/ui/joy_bkg.png",
                     joystick_file="assets/img/ui/joy_stick.png",
                     **kwargs):
                super(JoystickWidget, self).__init__(**kwargs)
                self.joystickbkg_file = joystickbkg_file
                self.joystick_file = joystick_file
                self.bind(pos=self.redraw, size=self.redraw)
                self.direction = [0, 0,]
                self.deadzone = deadzone

                Window.bind(on_key_down=self._on_keyboard_down)
                Window.bind(on_key_up=self._on_keyboard_up)

                self.redraw(None, None)

        def _on_keyboard_down(self, window, keycode, scancode, codepoint, modifier):
                if keycode == self.KEYCODE_W:
                        self.direction[1] = 1
                elif keycode == self.KEYCODE_S:
                        self.direction[1] = -1
                elif keycode == self.KEYCODE_A:
                        self.direction[0] = -1
                elif keycode == self.KEYCODE_D:
                        self.direction[0] = 1

        def _on_keyboard_up(self, window, keycode, scancode):
                if keycode == self.KEYCODE_W or keycode == self.KEYCODE_S:
                        self.direction[1] = 0
                elif keycode == self.KEYCODE_A or keycode == self.KEYCODE_D:
                        self.direction[0] = 0

        def get_direction(self):
                return self.direction

        def redraw(self, instance, value):
                self.canvas.clear()
                with self.canvas:
                        PushMatrix()
                        Rectangle(source=self.joystickbkg_file, pos=self.pos, size=self.size)
                        sticksize = (self.size[0] / 4, self.size[1] / 4, )
                        self.joystick = Rectangle(source=self.joystick_file, pos=(0,0), size=sticksize)
                        PopMatrix()
                        self.do_center()

        def get_centerpos(self):
                return (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2,)

        def do_center(self):
                self.do_draw(self.get_centerpos())

        def do_draw(self, touchpos):
                if touchpos[0] > self.size[0] or touchpos[1] > self.size[1]:
                        self.do_draw(self.get_centerpos())
                        return

                min_x = self.pos[0] + self.size[0] / 8.0
                min_y = self.pos[1] + self.size[1] / 8.0

                max_x = self.pos[0] + self.size[0] - self.size[0] / 8.0
                max_y = self.pos[1] + self.size[1] - self.size[1] / 8.0

                stickpos_x = max(min_x, touchpos[0], )
                stickpos_y = max(min_y, touchpos[1], )

                stickpos_x = min(max_x, stickpos_x, )
                stickpos_y = min(max_y, stickpos_y, )

                centerpos = self.get_centerpos()
                delta_x = stickpos_x - centerpos[0]
                delta_y = stickpos_y - centerpos[1]

                max_delta_x = 3.0 / 4.0 * self.size[0]
                max_delta_y = 3.0 / 4.0 * self.size[1]

                direction_x = delta_x / max_delta_x * 2.0
                direction_y = delta_y / max_delta_y * 2.0

                if abs(direction_x) >= self.deadzone or abs(direction_y) >= self.deadzone:
                        self.direction[0] = direction_x
                        self.direction[1] = direction_y
                else:
                        self.direction[0] = 0
                        self.direction[1] = 0

                drawpos_x = stickpos_x - self.size[0] / 8
                drawpos_y = stickpos_y - self.size[1] / 8

                if self.joystick:
                        self.joystick.pos = (drawpos_x, drawpos_y,)

        def on_touch_down(self, touch):
                if self.collide_point(touch.x, touch.y):
                        self.do_draw((touch.x, touch.y))

        def on_touch_up(self, touch):
                self.do_center()

        def on_touch_move(self, touch):
                self.do_draw((touch.x, touch.y))
