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
Controls
"""

cdef int IDX_STATE_CONTROLS

cdef int IDX_CONTROLS_JOYSTICK = 0
cdef int IDX_CONTROLS_JOYSTICK_DIRECTION = 1
cdef int IDX_CONTROLS_BUTTONS = 2

IDX_CONTROL_BUTTON_LABEL = 0
IDX_CONTROL_BUTTON_CALLBACK = 1
IDX_CONTROL_BUTTON_STATE = 2
IDX_CONTROL_BUTTON_POS = 3
IDX_CONTROL_BUTTON_SIZE = 4

cpdef initialize(int state_idx, list state):
        """
        TODO
        """
        global IDX_STATE_CONTROLS
        IDX_STATE_CONTROLS = state_idx
        state[IDX_STATE_CONTROLS] = [
                False,
                [0, 0],
                []
                ]

cpdef destroy(list state):
        """
        TODO
        """
        state[IDX_STATE_CONTROLS] = None

cpdef add_buttons(list state, tuple button_defs):
        """
        button definition = (button label, callback, position, size)
        position can be "left", "center", "right"
        size can be "small", "big"
        """
        state_button_defs = state[IDX_STATE_CONTROLS][IDX_CONTROLS_BUTTONS]
        for button_def in button_defs:
                state_button_defs.append([
                        button_def[0],
                        button_def[1],
                        False,
                        button_def[2],
                        button_def[3],
                        ])

cpdef list get_buttons(list state):
        """
        TODO
        """
        return state[IDX_STATE_CONTROLS][IDX_CONTROLS_BUTTONS]

cpdef set_button_state(list state, int button_index, int button_pressed):
        """
        TODO
        """
        button_state = state[IDX_STATE_CONTROLS][IDX_CONTROLS_BUTTONS][button_index]
        button_state[IDX_CONTROL_BUTTON_STATE] = button_pressed
        (button_state[IDX_CONTROL_BUTTON_CALLBACK])(state, button_pressed)

cpdef int get_button_is_down(list state, int button_index):
        """
        TODO
        """
        return state[IDX_STATE_CONTROLS][IDX_CONTROLS_BUTTONS][button_index][IDX_CONTROL_BUTTON_STATE]

cpdef add_joystick(list state):
        """
        TODO
        """
        state[IDX_STATE_CONTROLS][IDX_CONTROLS_JOYSTICK] = True

cpdef int need_joystick(list state):
        """
        TODO
        """
        return state[IDX_STATE_CONTROLS][IDX_CONTROLS_JOYSTICK]

cpdef int need_buttons(list state):
        """
        TODO
        """
        return len(state[IDX_STATE_CONTROLS][IDX_CONTROLS_BUTTONS]) > 0

cpdef set_joystick(list state, directions):
        """
        TODO
        """
        if state[IDX_STATE_CONTROLS]:
                state[IDX_STATE_CONTROLS][IDX_CONTROLS_JOYSTICK_DIRECTION][0] = (float(directions[0]))
                state[IDX_STATE_CONTROLS][IDX_CONTROLS_JOYSTICK_DIRECTION][1] = (float(directions[1]))

cpdef get_joystick(list state):
        """
        TODO
        """
        return state[IDX_STATE_CONTROLS][IDX_CONTROLS_JOYSTICK_DIRECTION]

cpdef dict get_joystick_properties():
        """
        TODO
        """
        return {
                "x" : 0.0,
                "y" : 0.0,
                "w" : 1.0,
                "h" : 0.25,
                }
