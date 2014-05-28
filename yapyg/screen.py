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
2D Sprites
"""

def initialize(state, screen_width, screen_height, tile_size, origin_xy=(0, 0)):
        """
        TODO
        """
        state["screen"] = {
                "width": screen_width,
                "height": screen_height,
                "tile_size": tile_size,
                "origin_xy": [origin_xy[0], origin_xy[1]],
        }

def destroy(state):
        """
        TODO
        """
        del state["screen"]

def get_width(state):
        """
        TODO
        """
        return state["screen"]["width"]

def get_height(state):
        """
        TODO
        """
        return state["screen"]["height"]

def get_tile_size(state):
        """
        TODO
        """
        return state["screen"]["tile_size"]

def set_origin(state, origin_xy):
        """
        TODO
        """
        state["screen"]["origin_xy"][0] = origin_xy[0]
        state["screen"]["origin_xy"][1] = origin_xy[1]

def get_origin(state):
        """
        TODO
        """
        origin_xy = state["screen"]["origin_xy"]
        return (origin_xy[0], origin_xy[1])
