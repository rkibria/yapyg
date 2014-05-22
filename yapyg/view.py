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
View setter
"""

def initialize(state):
    """
    TODO
    """
    state["view"] = {
        "view_pos": [0, 0],
        "view_setter": None,
    }

def destroy(state):
    """
    TODO
    """
    del state["view"]

def get_view_pos(state):
    """
    TODO
    """
    return state["view"]["view_pos"]

def set_view_pos(state, view_pos):
    """
    TODO
    """
    state["view"]["view_pos"][0] = view_pos[0]
    state["view"]["view_pos"][1] = view_pos[1]

def set_viewer(state, viewer):
    """
    TODO
    """
    state["view"]["view_setter"] = viewer

def run(state):
    """
    TODO
    """
    setter = state["view"]["view_setter"]
    if setter:
        return (setter["run"])(state, setter)
    else:
        return False
