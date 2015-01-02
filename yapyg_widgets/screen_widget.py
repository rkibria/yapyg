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
from kivy.core.window import Keyboard

from yapyg import fixpoint
from yapyg import texture_db
from yapyg import controls
from yapyg import debug
from yapyg_widgets.display_widget import DisplayWidget
from yapyg_widgets.joystick_widget import JoystickWidget

class ScreenWidget(FloatLayout):
        KEYCODE_SPACE = Keyboard.keycodes['spacebar']

        def __init__(self, state, scale=None, on_exit_function=None, debugging=False, **kwargs):
                super(ScreenWidget, self).__init__(**kwargs)

                self.state = state

                FIXP_1 = fixpoint.int2fix(1)
                texture_db.insert_color_rect(state, FIXP_1, FIXP_1, "tl_null", 0.0, 0.0, 0.0)

                if not scale:
                        scale = FIXP_1
                self.display_widget = DisplayWidget(state, [fixpoint.float2fix(float(Window.width)), fixpoint.float2fix(float(Window.height))], scale)
                self.on_exit_function = on_exit_function

                self.add_widget(self.display_widget)

                self.joystick = None

                joystick_panel_height = 0.2
                joystick_x = 0.01
                joystick_y = 0.01

                if controls.need_joystick(state) or controls.need_buttons(state):
                        joystick_height = 0.18
                        joystick_width = (joystick_height * Window.height) / Window.width
                        self.add_widget(Image(source="assets/img/ui/joy_panel.png",
                                size_hint=(1, joystick_panel_height),
                                pos_hint = {"x" : 0.0, "y" : 0.0}))

                if controls.need_joystick(state):
                        self.joystick = JoystickWidget(
                                size_hint=(joystick_width, joystick_height),
                                pos_hint = {"x" : joystick_x, "y" : joystick_y},)
                        self.add_widget(self.joystick)
                        Clock.schedule_interval(self.on_timer, 0.1)

                if controls.need_buttons(state):
                        Window.bind(on_key_down=self._on_keyboard_down)
                        Window.bind(on_key_up=self._on_keyboard_up)

                        button_width = joystick_width / 2.0
                        button_height = joystick_height / 2.0
                        button_width_big = 2 * button_width
                        button_height_big = 2 * button_height

                        background_file = "assets/img/ui/joy_button.png"
                        background_down_file = "assets/img/ui/joy_button_down.png"
                        background_file_big = "assets/img/ui/joy_button_big.png"
                        background_down_file_big = "assets/img/ui/joy_button_down_big.png"

                        button_defs = controls.get_buttons(state)

                        if button_defs:
                                if button_defs[0][controls.IDX_CONTROL_BUTTON_POS] == "right":
                                        if button_defs[0][controls.IDX_CONTROL_BUTTON_SIZE] == "small":
                                                button_0 = Button(text='[color=000000][b]%s[/b][/color]' % button_defs[0][controls.IDX_CONTROL_BUTTON_LABEL],
                                                        font_size=16,
                                                        markup=True,
                                                        background_normal=background_file,
                                                        background_down=background_down_file,
                                                        size_hint=(button_width, button_height),
                                                        pos_hint = {"x" : 1.0 - button_width - 0.01, "y" : 0.0 + 0.01},
                                                        )
                                        else:
                                                button_0 = Button(text='[color=000000][b]%s[/b][/color]' % button_defs[0][controls.IDX_CONTROL_BUTTON_LABEL],
                                                        font_size=16,
                                                        markup=True,
                                                        background_normal=background_file_big,
                                                        background_down=background_down_file_big,
                                                        size_hint=(button_width_big, button_height_big),
                                                        pos_hint = {"x" : 1.0 - button_width_big - 0.01, "y" : 0.0 + 0.01},
                                                        )
                                elif button_defs[0][controls.IDX_CONTROL_BUTTON_POS] == "left":
                                        if button_defs[0][controls.IDX_CONTROL_BUTTON_SIZE] == "small":
                                                button_0 = Button(text='[color=000000][b]%s[/b][/color]' % button_defs[0][controls.IDX_CONTROL_BUTTON_LABEL],
                                                        font_size=16,
                                                        markup=True,
                                                        background_normal=background_file,
                                                        background_down=background_down_file,
                                                        size_hint=(button_width, button_height),
                                                        pos_hint = {"x" : joystick_x, "y" : joystick_y},
                                                        )
                                        else:
                                                button_0 = Button(text='[color=000000][b]%s[/b][/color]' % button_defs[0][controls.IDX_CONTROL_BUTTON_LABEL],
                                                        font_size=16,
                                                        markup=True,
                                                        background_normal=background_file_big,
                                                        background_down=background_down_file_big,
                                                        size_hint=(button_width_big, button_height_big),
                                                        pos_hint = {"x" : joystick_x, "y" : joystick_y},
                                                        )
                                self.add_widget(button_0)
                                button_0.bind(state=self.on_button_0)

                                if len(button_defs) > 1:
                                        if button_defs[1][controls.IDX_CONTROL_BUTTON_POS] == "right":
                                                if button_defs[1][controls.IDX_CONTROL_BUTTON_SIZE] == "small":
                                                        button_1 = Button(text='[color=000000][b]%s[/b][/color]' % button_defs[1][controls.IDX_CONTROL_BUTTON_LABEL],
                                                                font_size=16,
                                                                markup=True,
                                                                background_normal=background_file,
                                                                background_down=background_down_file,
                                                                size_hint=(button_width, button_height),
                                                                pos_hint = {"x" : 1.0 - joystick_width - 0.01, "y" : 0.0 + 0.01},
                                                                )
                                                else:
                                                        button_1 = Button(text='[color=000000][b]%s[/b][/color]' % button_defs[1][controls.IDX_CONTROL_BUTTON_LABEL],
                                                                font_size=16,
                                                                markup=True,
                                                                background_normal=background_file_big,
                                                                background_down=background_down_file_big,
                                                                size_hint=(button_width_big, button_height_big),
                                                                pos_hint = {"x" : 1.0 - joystick_width - 0.01, "y" : 0.0 + 0.01},
                                                                )
                                        elif button_defs[1][controls.IDX_CONTROL_BUTTON_POS] == "left":
                                                if button_defs[1][controls.IDX_CONTROL_BUTTON_SIZE] == "small":
                                                        button_1 = Button(text='[color=000000][b]%s[/b][/color]' % button_defs[1][controls.IDX_CONTROL_BUTTON_LABEL],
                                                                font_size=16,
                                                                markup=True,
                                                                background_normal=background_file,
                                                                background_down=background_down_file,
                                                                size_hint=(button_width, button_height),
                                                                pos_hint = {"x" : joystick_x, "y" : joystick_y},
                                                                )
                                                else:
                                                        button_1 = Button(text='[color=000000][b]%s[/b][/color]' % button_defs[1][controls.IDX_CONTROL_BUTTON_LABEL],
                                                                font_size=16,
                                                                markup=True,
                                                                background_normal=background_file_big,
                                                                background_down=background_down_file_big,
                                                                size_hint=(button_width_big, button_height_big),
                                                                pos_hint = {"x" : joystick_x, "y" : joystick_y},
                                                                )
                                        self.add_widget(button_1)
                                        button_1.bind(state=self.on_button_1)

                                if len(button_defs) > 2:
                                        button_2 = Button(text='[color=000000][b]%s[/b][/color]' % button_defs[2][controls.IDX_CONTROL_BUTTON_LABEL],
                                                font_size=16,
                                                markup=True,
                                                background_normal=background_file,
                                                background_down=background_down_file,
                                                size_hint=(button_width, button_height),
                                                pos_hint = {"x" : 1.0 - button_width - 0.01, "y" : button_height + 0.01},
                                                )
                                        self.add_widget(button_2)
                                        button_2.bind(state=self.on_button_2)

                                if len(button_defs) > 3:
                                        button_3 = Button(text='[color=000000][b]%s[/b][/color]' % button_defs[3][controls.IDX_CONTROL_BUTTON_LABEL],
                                                font_size=16,
                                                markup=True,
                                                background_normal=background_file,
                                                background_down=background_down_file,
                                                size_hint=(button_width, button_height),
                                                pos_hint = {"x" : 1.0 - joystick_width - 0.01, "y" : button_height + 0.01},
                                                )
                                        self.add_widget(button_3)
                                        button_3.bind(state=self.on_button_3)

                if self.on_exit_function:
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
                        NUM_DEBUG_LINES = debug.NUM_DEBUG_LINES + 1
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
                status_output = "fps:%.1f frame_time:%.1fms" % (float(Clock.get_fps()), fixpoint.fix2float(frame_time))
                self.set_debug_text(0, status_output)

                for i in xrange(debug.NUM_DEBUG_LINES):
                        debug_line = debug.get_line(self.state, i)
                        self.set_debug_text(1 + i, debug_line)

        def on_timer(self, dt):
                if self.state:
                        controls.set_joystick(self.state, self.joystick.get_direction())

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
                        controls.set_button_state(self.state, 0, True if value == "down" else False)

        def on_button_1(self, instance, value):
                if self.state:
                        controls.set_button_state(self.state, 1, True if value == "down" else False)

        def on_button_2(self, instance, value):
                if self.state:
                        controls.set_button_state(self.state, 2, True if value == "down" else False)

        def on_button_3(self, instance, value):
                if self.state:
                        controls.set_button_state(self.state, 3, True if value == "down" else False)

        def _on_keyboard_down(self, window, keycode, scancode, codepoint, modifier):
                if self.state:
                        if keycode == self.KEYCODE_SPACE:
                                controls.set_button_state(self.state, 0, True)

        def _on_keyboard_up(self, window, keycode, scancode):
                if self.state:
                        if keycode == self.KEYCODE_SPACE:
                                controls.set_button_state(self.state, 0, False)
