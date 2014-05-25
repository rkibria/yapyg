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
import collisions

def initialize(state):
    """
    TODO
    """
    state["entities"] = {
        "entities": {},
        "pos_listeners": [],
    }

def add_pos_listener(state, callback):
    """
    TODO
    """
    state["entities"]["pos_listeners"].append(callback)

def _call_pos_listeners(state, entity_name, pos):
    """
    TODO
    """
    for callback in state["entities"]["pos_listeners"]:
        (callback)(state, entity_name, pos)

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
    if state["entities"]["entities"].has_key(entity_name):
        return state["entities"]["entities"][entity_name]
    else:
        return None

def get_pos(state, entity_name):
    """
    TODO
    """
    entity = get(state, entity_name)
    return (entity["pos"][0], entity["pos"][1])

def set_pos(state, entity_name, x_pos, y_pos):
    """
    TODO
    """
    entity = get(state, entity_name)
    if not entity["last_pos"]:
        entity["last_pos"] = [
            0,
            0,
            entity["rot"][0]]
    entity["last_pos"][0] = entity["pos"][0]
    entity["last_pos"][1] = entity["pos"][1]

    entity["pos"][0] = x_pos
    entity["pos"][1] = y_pos

    _call_pos_listeners(state, entity_name, get_pos(state, entity_name))

def add_pos(state, entity_name, x_pos, y_pos):
    """
    TODO
    """
    entity = get(state, entity_name)
    if not entity["last_pos"]:
        entity["last_pos"] = [
            0,
            0,
            entity["rot"][0]]
    entity["last_pos"][0] = entity["pos"][0]
    entity["last_pos"][1] = entity["pos"][1]

    entity["pos"][0] += x_pos
    entity["pos"][1] += y_pos

    _call_pos_listeners(state, entity_name, get_pos(state, entity_name))

def get_last_pos(state, entity_name):
    """
    TODO
    """
    return get(state, entity_name)["last_pos"]

def get_pos_offset(state, entity_name):
    """
    TODO
    """
    entity = get(state, entity_name)
    return (entity["pos_offset"][0], entity["pos_offset"][1])

def get_rot(state, entity_name):
    """
    TODO
    """
    return get(state, entity_name)["rot"][0]

def set_rot(state, entity_name, rot):
    """
    TODO
    """
    entity = get(state, entity_name)
    if not entity["last_pos"]:
        entity["last_pos"] = [
            entity["pos"][0],
            entity["pos"][1],
            0]
    entity["last_pos"][2] = entity["rot"][0]

    entity["rot"][0] = rot

def undo_last_move(state, entity_name):
    """
    TODO
    """
    entity = get(state, entity_name)
    if entity["last_pos"]:
        entity["pos"][0] = entity["last_pos"][0]
        entity["pos"][1] = entity["last_pos"][1]
        entity["rot"][0] = entity["last_pos"][2]
        entity["last_pos"] = None
        _call_pos_listeners(state, entity_name, get_pos(state, entity_name))

def insert(state, entity_name, sprite_defs, pos, rot=0, pos_offset=[0, 0], collision=None):
    """
    TODO
    """
    state["entities"]["entities"][entity_name] = {
        "pos": [pos[0], pos[1]],
        "rot": [rot],
        "pos_offset": pos_offset,
        "enabled_sprite": None,
        "last_pos": None,
        "sprites": [],
        "collision": True if collision else None,
        }

    if collision:
        collisions.add(state, entity_name, collision[0], collision[1])

    entity = get(state, entity_name)
    default_sprite = None
    for sprite_name, sprite_def in sprite_defs.iteritems():
        entity["sprites"].append(sprite_name)

        if sprite_name[0] == "*":
            default_sprite = sprite_name

        set_sprite(state, entity_name, sprite_name, sprite_def)

    if default_sprite:
        set_active_sprite(state, entity_name, default_sprite)

def set_sprite(state, entity_name, sprite_name, sprite_def, enable=False):
    if not sprite_def.has_key("speed"):
        sprite_def["speed"] = 0

    entity = get(state, entity_name)
    full_sprite_name = _get_full_sprite_name(entity_name, sprite_name)
    enabled_sprite_name = entity["enabled_sprite"]

    if enabled_sprite_name == sprite_name:
        sprites.set_enable(state, full_sprite_name, False)

    sprites.delete(state, full_sprite_name)

    sprites.insert(state, full_sprite_name,
        sprite_def["textures"],
        speed=sprite_def["speed"],
        pos=entity["pos"],
        rot_list=entity["rot"],
        pos_offset=entity["pos_offset"],
        enable=enable,)

    if enabled_sprite_name == sprite_name:
        sprites.set_enable(state, full_sprite_name, True)

def delete(state, entity_name):
    """
    TODO
    """
    entity = get(state, entity_name)
    if entity:
        sprites.set_enable(state, _get_full_sprite_name(entity_name, entity["enabled_sprite"]), False)
        for sprite_name in entity["sprites"]:
            sprites.delete(state, _get_full_sprite_name(entity_name, sprite_name))

        if entity["collision"]:
            collisions.delete(state, entity_name)

        del state["entities"]["entities"][entity_name]

def set_active_sprite(state, entity_name, sprite_name):
    """
    TODO
    """
    entity = get(state, entity_name)
    if entity["enabled_sprite"]:
        sprites.set_enable(state, _get_full_sprite_name(entity_name, entity["enabled_sprite"]), False)
    sprites.set_enable(state, _get_full_sprite_name(entity_name, sprite_name), True)
    entity["enabled_sprite"] = sprite_name
