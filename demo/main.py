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

SCREEN_LOGICAL_WIDTH = 480
SCREEN_LOGICAL_HEIGHT = 800
TILE_SIZE = 128

import yapyg.bootstrap
SCREEN_SCALE = 1.0
SCREEN_REAL_WIDTH = int(SCREEN_LOGICAL_WIDTH * SCREEN_SCALE)
SCREEN_REAL_HEIGHT = int(SCREEN_LOGICAL_HEIGHT * SCREEN_SCALE)
yapyg.bootstrap.initialize_screen(SCREEN_REAL_WIDTH, SCREEN_REAL_HEIGHT)

from kivy.app import App
from kivy.core.window import Window

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout

from kivy import platform

from yapyg_widgets.screen_widget import ScreenWidget

DEFAULT_START_CHOICE = "demo_car"

class MenuWidget(FloatLayout):
        def __init__(self, **kwargs):
                super(MenuWidget, self).__init__(**kwargs)

                self.choices = {
                        "demo_bounce": "Basic physics simulation",
                        "demo_breakout": "Breakout demo",
                        "demo_gauntlet": "Top down tile map game",
                        "demo_starship": "'Endless' scrolling background and animation",
                        "demo_text": "Text drawing",
                        "demo_tiles": "Tile map scrolling",
                        "demo_pinball": "Simple pinball demo",
                        "demo_squares": "Random set of falling physical objects",
                        "demo_car": "Top down car driving game",
                        "demo_sprites": "Draw a large amount of sprites",
                        }

                layout = StackLayout(orientation="tb-lr", padding=[10, 20, 10, 20])

                layout.add_widget(Image(source="assets/img/ui/logo.png", size_hint=(1, 0.4), allow_stretch = True,))

                layout.add_widget(Label(text="Choose demo:", size_hint=(1, 0.1)))

                self.spinner = Spinner(text=DEFAULT_START_CHOICE, values=[x for x in self.choices.iterkeys()], size_hint=(1, 0.1))
                layout.add_widget(self.spinner)
                self.spinner.bind(text=self.show_selected_value)

                self.description_label = Label(text=self.choices[DEFAULT_START_CHOICE], valign="middle", halign="center", size_hint=(1, 0.2))
                self.description_label.bind(size=self.description_label.setter("text_size"))
                layout.add_widget(self.description_label)

                run_button = Button(text="Run", size_hint=(1, 0.1))
                run_button.bind(state=self.on_run)
                layout.add_widget(run_button)

                debug_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
                debug_layout.add_widget(Label(text=" "))
                self.debug_checkbox = CheckBox()
                self.debug_checkbox.active = False
                debug_layout.add_widget(self.debug_checkbox)
                debug_layout.add_widget(Label(text="Show debug info", valign="middle", halign="center"))
                debug_layout.add_widget(Label(text=" "))
                debug_layout.add_widget(Label(text=" "))
                self.add_widget(debug_layout)

                self.add_widget(layout)

                if platform == 'win' or platform == 'linux' or platform == 'macosx':
                        Window.bind(on_key_up=self._on_keyboard_up)

        def _on_keyboard_up(self, window, keycode, scancode):
                self.on_run(None, None)

        def show_selected_value(self, spinner, value):
                self.description_label.text = self.choices[value]

        def on_run(self, instance, value):
                if self.parent:
                        parent = self.parent
                        parent.remove_widget(self)

                        state = None
                        module_name = self.spinner.text
                        global DEFAULT_START_CHOICE
                        DEFAULT_START_CHOICE = module_name

                        exec("import %s" % module_name)
                        exec("state = %s.create(SCREEN_LOGICAL_WIDTH, SCREEN_LOGICAL_HEIGHT, TILE_SIZE)" % self.spinner.text)

                        parent.add_widget(ScreenWidget(state,
                                                       self.on_exit_game,
                                                       self.debug_checkbox.active
                                                       )
                                          )

        def on_exit_game(self, state, parent_widget):
                parent_widget.add_widget(MenuWidget())

class YapygDemoApp(App):
        def build(self):
                if True: # False to load a demo directly without the menu!
                        return MenuWidget()
                else:
                        import demo_gauntlet
                        state = demo_gauntlet.create(SCREEN_LOGICAL_WIDTH, SCREEN_LOGICAL_HEIGHT, TILE_SIZE)
                        return ScreenWidget(state,
                                            (float(Window.width) / SCREEN_LOGICAL_WIDTH),
                                            None, False)

if __name__ == "__main__":
        YapygDemoApp().run()
