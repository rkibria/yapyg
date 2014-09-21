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

from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

import yapyg
import yapyg_helpers
import yapyg_movers
import yapyg_viewers
import yapyg.debug

from display_widget import DisplayWidget
from joystick_widget import JoystickWidget
from yapyg.fixpoint import float2fix, fix2float

class ScreenWidget(FloatLayout):
        def __init__(self, state, on_exit_function, scale, debugging=False, **kwargs):
                super(ScreenWidget, self).__init__(**kwargs)

                self.state = state
                self.display_widget = DisplayWidget(state, [float2fix(float(Window.width)), float2fix(float(Window.height))], scale)
                self.on_exit_function = on_exit_function

                self.add_widget(self.display_widget)

                self.joystick = None
                if yapyg.controls.need_joystick(state):
                        joystick_panel_height = 0.2
                        joystick_height = 0.18
                        joystick_width = (joystick_height * Window.height) / Window.width

                        self.add_widget(Image(source="assets/img/ui/joy_panel.png",
                                size_hint=(1, joystick_panel_height),
                                pos_hint = {"x" : 0.0, "y" : 0.0}))

                        self.joystick = JoystickWidget(
                                size_hint=(joystick_width, joystick_height),
                                pos_hint = {"x" : 0.01, "y" : 0.01},)
                        self.add_widget(self.joystick)
                        Clock.schedule_interval(self.on_timer, 0.1)

                        button_width = joystick_width / 2.0
                        button_height = joystick_height / 2.0

                        button_defs = yapyg.controls.get_buttons(state)

                        if button_defs:
                                button_0 = Button(text='[color=000000][b]%s[/b][/color]' % button_defs[0][yapyg.controls.IDX_CONTROL_BUTTON_LABEL],
                                        font_size=16,
                                        markup=True,
                                        background_normal="assets/img/ui/joy_button.png",
                                        background_down="assets/img/ui/joy_button_down.png",
                                        size_hint=(button_width, button_height),
                                        pos_hint = {"x" : 1.0 - button_width - 0.01, "y" : 0.0 + 0.01},
                                        )
                                self.add_widget(button_0)
                                button_0.bind(state=self.on_button_0)

                                if len(button_defs) > 1:
                                        button_1 = Button(text='[color=000000][b]%s[/b][/color]' % button_defs[1][yapyg.controls.IDX_CONTROL_BUTTON_LABEL],
                                                font_size=16,
                                                markup=True,
                                                background_normal="assets/img/ui/joy_button.png",
                                                background_down="assets/img/ui/joy_button_down.png",
                                                size_hint=(button_width, button_height),
                                                pos_hint = {"x" : 1.0 - joystick_width - 0.01, "y" : 0.0 + 0.01},
                                                )
                                        self.add_widget(button_1)
                                        button_1.bind(state=self.on_button_1)

                                if len(button_defs) > 2:
                                        button_2 = Button(text='[color=000000][b]%s[/b][/color]' % button_defs[2][yapyg.controls.IDX_CONTROL_BUTTON_LABEL],
                                                font_size=16,
                                                markup=True,
                                                background_normal="assets/img/ui/joy_button.png",
                                                background_down="assets/img/ui/joy_button_down.png",
                                                size_hint=(button_width, button_height),
                                                pos_hint = {"x" : 1.0 - button_width - 0.01, "y" : button_height + 0.01},
                                                )
                                        self.add_widget(button_2)
                                        button_2.bind(state=self.on_button_2)

                                if len(button_defs) > 3:
                                        button_3 = Button(text='[color=000000][b]%s[/b][/color]' % button_defs[3][yapyg.controls.IDX_CONTROL_BUTTON_LABEL],
                                                font_size=16,
                                                markup=True,
                                                background_normal="assets/img/ui/joy_button.png",
                                                background_down="assets/img/ui/joy_button_down.png",
                                                size_hint=(button_width, button_height),
                                                pos_hint = {"x" : 1.0 - joystick_width - 0.01, "y" : button_height + 0.01},
                                                )
                                        self.add_widget(button_3)
                                        button_3.bind(state=self.on_button_3)

                exit_button = Button(text='[color=000000]Menu[/color]',
                                font_size=26,
                                markup=True,
                                background_normal="assets/img/ui/joy_option_button.png",
                                background_down="assets/img/ui/joy_option_button_down.png",
                                size_hint=(0.2, 0.05),
                                pos_hint = {"x":0.4, "y":0.01},
                                )
                exit_button.bind(state=self.on_exit)
                self.add_widget(exit_button)

                if debugging:
                        NUM_DEBUG_LINES = yapyg.debug.NUM_DEBUG_LINES + 1
                        DEBUG_LINE_SIZE = 0.05
                        self.debug_label_array = []
                        for i in xrange(NUM_DEBUG_LINES):
                                self.debug_label_array.append(Label(
                                        color=(0, 1, 0, 1),
                                        size_hint=(1.0, DEBUG_LINE_SIZE),
                                        pos_hint = {"x": 0.05, "y": 1.0 - DEBUG_LINE_SIZE - DEBUG_LINE_SIZE * i},
                                        markup=True,
                                        text_size=(Window.width, Window.height / NUM_DEBUG_LINES),
                                        ))
                                self.debug_label_array[i].bind(texture_size=self.setter('size'))
                                self.add_widget(self.debug_label_array[i])
                        Clock.schedule_interval(self.on_debug_timer, 0.5)

        def set_debug_text(self, line_no, txt):
                self.debug_label_array[line_no].text = txt

        def on_debug_timer(self, dt):
                frame_time = self.display_widget.get_frame_time()
                status_output = "fps:%.1f frame_time:%.1fms" % (float(Clock.get_fps()), fix2float(frame_time))
                self.set_debug_text(0, status_output)

                NUM_DEBUG_LINES = yapyg.debug.NUM_DEBUG_LINES
                for i in xrange(NUM_DEBUG_LINES):
                        debug_line = yapyg.debug.get_line(self.state, i)
                        self.set_debug_text(1 + i, debug_line)

        def on_timer(self, dt):
                if self.state:
                        yapyg.controls.set_joystick(self.state, self.joystick.get_direction())

        def on_exit(self, instance, value):
                if self.parent:
                        Clock.unschedule(self.on_debug_timer)
                        Clock.unschedule(self.on_timer)
                        self.display_widget.destroy()
                        parent = self.parent
                        parent.remove_widget(self)
                        if self.on_exit_function:
                                (self.on_exit_function)(self.state, parent)

        def on_button_0(self, instance, value):
                if self.state:
                        yapyg.controls.set_button_state(self.state, 0, True if value == "down" else False)

        def on_button_1(self, instance, value):
                if self.state:
                        yapyg.controls.set_button_state(self.state, 1, True if value == "down" else False)

        def on_button_2(self, instance, value):
                if self.state:
                        yapyg.controls.set_button_state(self.state, 2, True if value == "down" else False)

        def on_button_3(self, instance, value):
                if self.state:
                        yapyg.controls.set_button_state(self.state, 3, True if value == "down" else False)
