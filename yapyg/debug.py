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
Debugging
"""

import globals
import fixpoint

IDX_STATE_DEBUG = globals.get_module_index("IDX_STATE_DEBUG")

IDX_DEBUG_TEXTLINES = 0

NUM_DEBUG_LINES = 19

def initialize(state):
        """
        TODO
        """
        state[IDX_STATE_DEBUG] = [
                [("") for x in xrange(NUM_DEBUG_LINES)],
                ]

def destroy(state):
        """
        TODO
        """
        state[IDX_STATE_DEBUG] = None

def set_line(state, line_no, txt):
        """
        TODO
        """
        state[IDX_STATE_DEBUG][IDX_DEBUG_TEXTLINES][line_no] = txt

def get_line(state, line_no):
        """
        TODO
        """
        return state[IDX_STATE_DEBUG][IDX_DEBUG_TEXTLINES][line_no]
