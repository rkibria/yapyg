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
Entity state setting mover
"""

import yapyg.movers
import yapyg.entities

IDX_MOVER_SET_PROPERTY_PROPERTY = yapyg.movers.IDX_MOVER_FIRST_PARAMETER
IDX_MOVER_SET_PROPERTY_NEW_VALUE = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 1
IDX_MOVER_SET_PROPERTY_ON_END_FUNCTION = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 2

class YapygMoverSetPropertyException(Exception):
        """
        TODO
        """
        def __init__(self, value):
                """
                TODO
                """
                self.value = value

        def __str__(self):
                """
                TODO
                """
                return repr(self.value)

def add(state, entity_name, property, new_value, on_end_function=None, do_replace=False):
        """
        TODO
        """
        yapyg.movers.add(state, entity_name, create(entity_name, property, new_value, on_end_function), do_replace)

def create(entity_name, property, new_value, on_end_function=None):
        """
        TODO
        """
        return ["set_property",
                run,
                entity_name,
                None,
                property,
                new_value,
                on_end_function,]

def run(state, entity_name, mover, frame_time_delta, movers_to_delete):
        """
        TODO
        """
        property = mover[IDX_MOVER_SET_PROPERTY_PROPERTY]
        new_value = mover[IDX_MOVER_SET_PROPERTY_NEW_VALUE]

        if property == "set_active_sprite":
                yapyg.entities.set_active_sprite(state, entity_name, new_value)
        else:
                raise YapygMoverSetPropertyException("Unknown property %s" % property)

        movers_to_delete.append((entity_name, mover[IDX_MOVER_SET_PROPERTY_ON_END_FUNCTION]))
