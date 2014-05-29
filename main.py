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

from kivy.config import Config
Config.set("input", "mouse", "mouse,disable_multitouch")
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', screen_width)
Config.set('graphics', 'height', screen_height)

from kivy.app import App
from kivy.core.window import Window

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.clock import Clock

from yapyg.widget import YapygWidget
from yapyg.joystick_widget import JoystickWidget
import yapyg.controls

import demo_starship
import demo_tiles
import demo_pong
import demo_bounce
import demo_breakout
import demo_text
import demo_collision
import demo_collision_1
import demo_control_1

class MenuWidget(FloatLayout):
        def __init__(self, **kwargs):
                super(MenuWidget, self).__init__(**kwargs)

                default_choice = "demo_text"
                self.choices = {
                        "demo_text": "Text drawing",
                        "demo_bounce": "Basic physics simulation",
                        "demo_starship": "'Endless' scrolling background and animation",
                        "demo_tiles": "Tile map scrolling",
                        "demo_pong": "Simple Pong game",
                        "demo_breakout": "Breakout implemented with physical mover",
                        "demo_collision": "Optimized collision checking demo/test",
                        "demo_collision_1": "Simple collision test case",
                        "demo_control_1": "Demonstrates a more complex control scheme",
                        }

                layout = StackLayout(orientation="tb-lr", padding=[10, 20, 10, 20])

                layout.add_widget(Image(source="assets/img/ui/logo.png", size_hint=(1, 0.4)))

                layout.add_widget(Label(text="Choose demo:", size_hint=(1, 0.1)))

                self.spinner = Spinner(text=default_choice, values=[x for x in self.choices.iterkeys()], size_hint=(1, 0.1))
                layout.add_widget(self.spinner)
                self.spinner.bind(text=self.show_selected_value)

                self.description_label = Label(text=self.choices[default_choice], valign="middle", halign="center", size_hint=(1, 0.3))
                self.description_label.bind(size=self.description_label.setter("text_size"))
                layout.add_widget(self.description_label)

                run_button = Button(text="Run", size_hint=(1, 0.1))
                run_button.bind(state=self.on_run)
                layout.add_widget(run_button)

                self.add_widget(layout)

        def show_selected_value(self, spinner, value):
                self.description_label.text = self.choices[value]

        def on_run(self, instance, value):
                if self.parent:
                        parent = self.parent
                        parent.remove_widget(self)

                        state = None
                        exec("state = %s.create(float(Window.width), float(Window.height), float(tile_size))" % self.spinner.text)

                        parent.add_widget(ScreenWidget(state))

class ScreenWidget(FloatLayout):
        def __init__(self, state, **kwargs):
                super(ScreenWidget, self).__init__(**kwargs)

                self.state = state
                self.yapyg_widget = YapygWidget(state, [Window.width, Window.height], Window.width / screen_width)

                self.add_widget(self.yapyg_widget)

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

                        self.add_widget(Button(text='[color=000000][b]B[/b][/color]',
                                font_size=26,
                                markup=True,
                                background_normal="assets/img/ui/joy_button.png",
                                background_down="assets/img/ui/joy_button_down.png",
                                size_hint=(button_width, button_height),
                                pos_hint = {"x" : 1.0 - joystick_width - 0.01, "y" : 0.0 + 0.01},
                                ))

                        self.add_widget(Button(text='[color=000000][b]A[/b][/color]',
                                font_size=26,
                                markup=True,
                                background_normal="assets/img/ui/joy_button.png",
                                background_down="assets/img/ui/joy_button_down.png",
                                size_hint=(button_width, button_height),
                                pos_hint = {"x" : 1.0 - button_width - 0.01, "y" : 0.0 + 0.01},
                                ))

                        self.add_widget(Button(text='[color=000000][b]D[/b][/color]',
                                font_size=26,
                                markup=True,
                                background_normal="assets/img/ui/joy_button.png",
                                background_down="assets/img/ui/joy_button_down.png",
                                size_hint=(button_width, button_height),
                                pos_hint = {"x" : 1.0 - joystick_width - 0.01, "y" : button_height + 0.01},
                                ))

                        self.add_widget(Button(text='[color=000000][b]C[/b][/color]',
                                font_size=26,
                                markup=True,
                                background_normal="assets/img/ui/joy_button.png",
                                background_down="assets/img/ui/joy_button_down.png",
                                size_hint=(button_width, button_height),
                                pos_hint = {"x" : 1.0 - button_width - 0.01, "y" : button_height + 0.01},
                                ))

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

        def on_timer(self, dt):
                if self.state:
                        yapyg.controls.set_joystick(self.state, self.joystick.get_direction())

        def on_exit(self, instance, value):
                if self.parent:
                        self.yapyg_widget.destroy()
                        parent = self.parent
                        parent.remove_widget(self)
                        parent.add_widget(MenuWidget())

class YapygDemoApp(App):
        def build(self):
                return MenuWidget()

if __name__ == "__main__":
        YapygDemoApp().run()
