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
Controls
"""

def initialize(state):
    """
    TODO
    """
    state["controls"] = {
        "joystick": False,
        "joystick_direction": [0, 0],
    }

def destroy(state):
    """
    TODO
    """
    del state["controls"]

def add_joystick(state):
    """
    TODO
    """
    state["controls"]["joystick"] = True

def need_joystick(state):
    """
    TODO
    """
    return state["controls"]["joystick"]

def set_joystick(state, directions):
    """
    TODO
    """
    state["controls"]["joystick_direction"][0] = directions[0]
    state["controls"]["joystick_direction"][1] = directions[1]

def get_joystick(state):
    """
    TODO
    """
    return state["controls"]["joystick_direction"]

def get_joystick_properties():
    """
    TODO
    """
    return {
        "x" : 0.0,
        "y" : 0.0,
        "w" : 1.0,
        "h" : 0.2,
        }
