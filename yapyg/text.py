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

"""
Text
"""

from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle, Fbo


import texture_db

IDX_STATE_TEXT = None

IDX_TEXT_WIDTH = 0
IDX_TEXT_HEIGHT = 1

def initialize(state_idx, state):
        """
        TODO
        """
        global IDX_STATE_TEXT
        IDX_STATE_TEXT = state_idx
        state[IDX_STATE_TEXT] = {}

def destroy(state):
        """
        TODO
        """
        state[IDX_STATE_TEXT] = None

def load_font(state, font_name, font_path, font_w, font_h):
        """
        TODO
        """
        font_texture = Image(source=font_path).texture
        code = 32
        for y in xrange(8):
                for x in xrange(12):
                        texture_name = font_name + "-" + str(code)
                        texture_db.insert(state, texture_name, font_texture.get_region(x * font_w, (7 - y) * font_h, font_w, font_h))
                        code += 1
        state[IDX_STATE_TEXT][font_name] = [font_w, font_h]

def get_character_texture(state, font_name, char):
        """
        TODO
        """
        return texture_db.get(state, font_name + "-" + str(ord(char)))

def create_texture(state, text, font_name):
        """
        TODO
        """
        font_def = state[IDX_STATE_TEXT][font_name]
        text_lines = text.split("\n")
        n_lines = len(text_lines)
        max_line_length = len(max(text_lines, key=len))
        texture_w = max_line_length * font_def[IDX_TEXT_WIDTH]
        texture_h = n_lines * font_def[IDX_TEXT_HEIGHT]
        texture = Texture.create(size=(texture_w, texture_h), colorfmt='rgba')
        fbo = Fbo(size=(texture_w, texture_h), texture=texture)
        for row in xrange(n_lines):
                cur_row = text_lines[row]
                for col in xrange(len(cur_row)):
                        char = cur_row[col]
                        char_texture = get_character_texture(state, font_name, char)
                        x_pos = col * font_def[IDX_TEXT_WIDTH]
                        y_pos = (n_lines - row - 1) * font_def[IDX_TEXT_HEIGHT]
                        with fbo:
                                Rectangle(pos=(x_pos, y_pos), size=(font_def[IDX_TEXT_WIDTH], font_def[IDX_TEXT_HEIGHT]), texture=char_texture)
                        fbo.draw()
        return texture
