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

import globals
import fixpoint

IDX_CONTROLS_JOYSTICK = 0
IDX_CONTROLS_JOYSTICK_DIRECTION = 1
IDX_CONTROLS_BUTTONS = 2

def initialize(state):
        """
        TODO
        """
        state[globals.IDX_STATE_CONTROLS] = [
                False,
                [0, 0],
                None
                ]

def destroy(state):
        """
        TODO
        """
        state[globals.IDX_STATE_CONTROLS] = None

def add_buttons(state, button_defs):
        """
        button definition = button label
        """
        state[globals.IDX_STATE_CONTROLS][IDX_CONTROLS_BUTTONS] = []
        state_bdefs = state[globals.IDX_STATE_CONTROLS][IDX_CONTROLS_BUTTONS]
        for b_def in button_defs:
                state_bdefs.append([
                        b_def,
                        False, # press state
                        ])

def get_buttons(state):
        """
        TODO
        """
        return state[globals.IDX_STATE_CONTROLS][IDX_CONTROLS_BUTTONS]

def set_button_state(state, button_index, button_pressed):
        """
        TODO
        """
        state[globals.IDX_STATE_CONTROLS][IDX_CONTROLS_BUTTONS][button_index][1] = button_pressed

def get_button_is_down(state, button_index):
        """
        TODO
        """
        return state[globals.IDX_STATE_CONTROLS][IDX_CONTROLS_BUTTONS][button_index][1]

def add_joystick(state):
        """
        TODO
        """
        state[globals.IDX_STATE_CONTROLS][IDX_CONTROLS_JOYSTICK] = True

def need_joystick(state):
        """
        TODO
        """
        return state[globals.IDX_STATE_CONTROLS][IDX_CONTROLS_JOYSTICK]

def set_joystick(state, directions):
        """
        TODO
        """
        if state[globals.IDX_STATE_CONTROLS]:
                state[globals.IDX_STATE_CONTROLS][IDX_CONTROLS_JOYSTICK_DIRECTION][0] = fixpoint.float2fix(float(directions[0]))
                state[globals.IDX_STATE_CONTROLS][IDX_CONTROLS_JOYSTICK_DIRECTION][1] = fixpoint.float2fix(float(directions[1]))

def get_joystick(state):
        """
        TODO
        """
        return state[globals.IDX_STATE_CONTROLS][IDX_CONTROLS_JOYSTICK_DIRECTION]

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
