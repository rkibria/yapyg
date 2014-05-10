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
Entities
"""

import copy

import sprites

def initialize(state):
    """
    TODO
    """
    state["entities"] = {}

def _get_full_sprite_name(entity_name, sprite_name):
    """
    TODO
    """
    return entity_name + "_" + sprite_name

def get(state, entity_name):
    """
    TODO
    """
    return state["entities"][entity_name]

def get_pos(state, entity_name):
    """
    TODO
    """
    return state["entities"][entity_name]["pos"]

def get_rot(state, entity_name):
    """
    TODO
    """
    return state["entities"][entity_name]["rot"]

def insert(state, entity_name, sprite_defs, pos, rot=0, pos_offset=[0, 0]):
    """
    TODO
    """
    state["entities"][entity_name] = {
        "pos": [pos[0], pos[1]],
        "rot": [rot],
        "pos_offset": pos_offset,
        "enabled_sprite": None,
        }

    for sprite_name, sprite_def in sprite_defs.iteritems():
        sprites.insert(state, _get_full_sprite_name(entity_name, sprite_name),
            sprite_def["textures"],
            speed=sprite_def["speed"],
            pos=state["entities"][entity_name]["pos"],
            rot_list=state["entities"][entity_name]["rot"],
            pos_offset=state["entities"][entity_name]["pos_offset"],
            enable=False,
            )

def set_sprite(state, entity_name, sprite_name):
    """
    TODO
    """
    if state["entities"][entity_name]["enabled_sprite"]:
        sprites.set_enable(state, _get_full_sprite_name(entity_name, state["entities"][entity_name]["enabled_sprite"]), False)
    sprites.set_enable(state, _get_full_sprite_name(entity_name, sprite_name), True)
    state["entities"][entity_name]["enabled_sprite"] = sprite_name
