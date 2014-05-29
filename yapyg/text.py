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

"""
Text
"""

from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.graphics import Color, Rectangle, Fbo, Ellipse

import globals
import texture_db

def initialize(state):
        """
        TODO
        """
        state[globals.IDX_STATE_TEXT] = {}

def destroy(state):
        """
        TODO
        """
        state[globals.IDX_STATE_TEXT] = None

def load_font(state, font_name, font_path, font_w, font_h, min_code=32, max_code=127):
        """
        TODO
        """
        state[globals.IDX_STATE_TEXT][font_name] = {
                "width": font_w,
                "height": font_h,
                "min_code": min_code,
                "max_code": max_code,
                "font_path": font_path,
        }

        for code in xrange(min_code, max_code + 1):
                char_path = font_path + "/" + "char-" + str(code) + ".png"
                texture_name = font_name + "-" + str(code)
                texture_db.load(state, texture_name, char_path)

def get_character_texture(state, font_name, char):
        """
        TODO
        """
        return texture_db.get(state, font_name + "-" + str(ord(char)))

def create_texture(state, text, font_name):
        """
        TODO
        """
        font_def = state[globals.IDX_STATE_TEXT][font_name]
        text_lines = text.split("\n")
        n_lines = len(text_lines)
        max_line_length = len(max(text_lines, key=len))
        texture_w = max_line_length * font_def["width"]
        texture_h = n_lines * font_def["height"]
        texture = Texture.create(size=(texture_w, texture_h), colorfmt='rgba')
        fbo = Fbo(size=(texture_w, texture_h), texture=texture)
        for row in xrange(n_lines):
                cur_row = text_lines[row]
                for col in xrange(len(cur_row)):
                        char = cur_row[col]
                        char_texture = get_character_texture(state, font_name, char)
                        x_pos = col * font_def["width"]
                        y_pos = (n_lines - row - 1) * font_def["height"]
                        with fbo:
                                Rectangle(pos=(x_pos, y_pos), size=(font_def["width"], font_def["height"]), texture=char_texture)
                        fbo.draw()
        return texture
