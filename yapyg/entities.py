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

def destroy(state):
    """
    TODO
    """
    del state["entities"]

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
    return (state["entities"][entity_name]["pos"][0], state["entities"][entity_name]["pos"][1])

def set_pos(state, entity_name, x_pos, y_pos):
    """
    TODO
    """
    if not state["entities"][entity_name]["last_pos"]:
        state["entities"][entity_name]["last_pos"] = [
            0,
            0,
            state["entities"][entity_name]["rot"][0]]
    state["entities"][entity_name]["last_pos"][0] = state["entities"][entity_name]["pos"][0]
    state["entities"][entity_name]["last_pos"][1] = state["entities"][entity_name]["pos"][1]

    state["entities"][entity_name]["pos"][0] = x_pos
    state["entities"][entity_name]["pos"][1] = y_pos

def add_pos(state, entity_name, x_pos, y_pos):
    """
    TODO
    """
    if not state["entities"][entity_name]["last_pos"]:
        state["entities"][entity_name]["last_pos"] = [
            0,
            0,
            state["entities"][entity_name]["rot"][0]]
    state["entities"][entity_name]["last_pos"][0] = state["entities"][entity_name]["pos"][0]
    state["entities"][entity_name]["last_pos"][1] = state["entities"][entity_name]["pos"][1]

    state["entities"][entity_name]["pos"][0] += x_pos
    state["entities"][entity_name]["pos"][1] += y_pos

def get_last_pos(state, entity_name):
    """
    TODO
    """
    return state["entities"][entity_name]["last_pos"]

def get_pos_offset(state, entity_name):
    """
    TODO
    """
    return (state["entities"][entity_name]["pos_offset"][0], state["entities"][entity_name]["pos_offset"][1])

def get_rot(state, entity_name):
    """
    TODO
    """
    return state["entities"][entity_name]["rot"][0]

def set_rot(state, entity_name, rot):
    """
    TODO
    """
    if not state["entities"][entity_name]["last_pos"]:
        state["entities"][entity_name]["last_pos"] = [
            state["entities"][entity_name]["pos"][0],
            state["entities"][entity_name]["pos"][1],
            0]
    state["entities"][entity_name]["last_pos"][2] = state["entities"][entity_name]["rot"][0]

    state["entities"][entity_name]["rot"][0] = rot

def undo_last_move(state, entity_name):
    """
    TODO
    """
    if state["entities"][entity_name]["last_pos"]:
        state["entities"][entity_name]["pos"][0] = state["entities"][entity_name]["last_pos"][0]
        state["entities"][entity_name]["pos"][1] = state["entities"][entity_name]["last_pos"][1]
        state["entities"][entity_name]["rot"][0] = state["entities"][entity_name]["last_pos"][2]
        state["entities"][entity_name]["last_pos"] = None

def insert(state, entity_name, sprite_defs, pos, rot=0, pos_offset=[0, 0]):
    """
    TODO
    """
    state["entities"][entity_name] = {
        "pos": [pos[0], pos[1]],
        "rot": [rot],
        "pos_offset": pos_offset,
        "enabled_sprite": None,
        "last_pos": None,
        "sprites": [],
        }

    default_sprite = None
    for sprite_name, sprite_def in sprite_defs.iteritems():
        state["entities"][entity_name]["sprites"].append(sprite_name)

        if sprite_name[0] == "*":
            default_sprite = sprite_name

        speed = 0
        if sprite_def.has_key("speed"):
            speed = sprite_def["speed"]

        sprites.insert(state, _get_full_sprite_name(entity_name, sprite_name),
            sprite_def["textures"],
            speed=speed,
            pos=state["entities"][entity_name]["pos"],
            rot_list=state["entities"][entity_name]["rot"],
            pos_offset=state["entities"][entity_name]["pos_offset"],
            enable=False,)

    if default_sprite:
        set_sprite(state, entity_name, default_sprite)

def delete(state, entity_name):
    """
    TODO
    """
    sprites.set_enable(state, _get_full_sprite_name(entity_name, state["entities"][entity_name]["enabled_sprite"]), False)
    for sprite_name in state["entities"][entity_name]["sprites"]:
        sprites.delete(state, _get_full_sprite_name(entity_name, sprite_name))
    del state["entities"][entity_name]

def set_sprite(state, entity_name, sprite_name):
    """
    TODO
    """
    if state["entities"][entity_name]["enabled_sprite"]:
        sprites.set_enable(state, _get_full_sprite_name(entity_name, state["entities"][entity_name]["enabled_sprite"]), False)
    sprites.set_enable(state, _get_full_sprite_name(entity_name, sprite_name), True)
    state["entities"][entity_name]["enabled_sprite"] = sprite_name
