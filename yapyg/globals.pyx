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
Globals
"""

cpdef int IDX_STATE_SCREEN = 0
cpdef int IDX_STATE_TILES = 1
cpdef int IDX_STATE_TEXTURE_DB = 2
cpdef int IDX_STATE_SPRITES = 3
cpdef int IDX_STATE_MOVERS = 4
cpdef int IDX_STATE_ENTITIES = 5
cpdef int IDX_STATE_VIEW = 6
cpdef int IDX_STATE_CONTROLS = 7
cpdef int IDX_STATE_COLLISIONS = 8
cpdef int IDX_STATE_TEXT = 9
cpdef int IDX_STATE_TIMER = 10
cpdef int IDX_STATE_DEBUG = 11
cpdef int IDX_STATE_USER = 12

IDX_STATE_LAST = 13

# Import of global constants from Python does not seem to work
text_same_as_above = """cpdef int IDX_STATE_SCREEN = 0
cpdef int IDX_STATE_TILES = 1
cpdef int IDX_STATE_TEXTURE_DB = 2
cpdef int IDX_STATE_SPRITES = 3
cpdef int IDX_STATE_MOVERS = 4
cpdef int IDX_STATE_ENTITIES = 5
cpdef int IDX_STATE_VIEW = 6
cpdef int IDX_STATE_CONTROLS = 7
cpdef int IDX_STATE_COLLISIONS = 8
cpdef int IDX_STATE_TEXT = 9
cpdef int IDX_STATE_TIMER = 10
cpdef int IDX_STATE_DEBUG = 11
cpdef int IDX_STATE_USER = 12
"""

cpdef int get_module_index(str name):
        index = 0
        for line in text_same_as_above.splitlines():
                if name in line:
                        return index
                index += 1
        return None
