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

import globals
import sprites
import collisions

IDX_ENTITY_POS = 0
IDX_ENTITY_ROT = 1
IDX_ENTITY_POS_OFFSET = 2
IDX_ENTITY_ENABLED_SPRITE = 3
IDX_ENTITY_LAST_POS = 4
IDX_ENTITY_SPRITES = 5
IDX_ENTITY_COLLISION = 6

IDX_ENTITIES_TABLE = 0
IDX_ENTITIES_POS_LISTENERS = 1

def initialize(state):
        """
        TODO
        """
        state[globals.IDX_STATE_ENTITIES] = [
                {},
                [],]

def add_pos_listener(state, callback):
        """
        TODO
        """
        state[globals.IDX_STATE_ENTITIES][IDX_ENTITIES_POS_LISTENERS].append(callback)

def _call_pos_listeners(state, entity_name, pos):
        """
        TODO
        """
        for callback in state[globals.IDX_STATE_ENTITIES][IDX_ENTITIES_POS_LISTENERS]:
                (callback)(state, entity_name, pos)

def destroy(state):
        """
        TODO
        """
        del state[globals.IDX_STATE_ENTITIES]

def _get_full_sprite_name(entity_name, sprite_name):
        """
        TODO
        """
        return entity_name + "_" + sprite_name

def get(state, entity_name):
        """
        TODO
        """
        if state[globals.IDX_STATE_ENTITIES][IDX_ENTITIES_TABLE].has_key(entity_name):
                return state[globals.IDX_STATE_ENTITIES][IDX_ENTITIES_TABLE][entity_name]
        else:
                return None

def get_pos(state, entity_name):
        """
        TODO
        """
        entity = get(state, entity_name)
        return (entity[IDX_ENTITY_POS][0], entity[IDX_ENTITY_POS][1])

def set_pos(state, entity_name, x_pos, y_pos):
        """
        TODO
        """
        entity = get(state, entity_name)
        if not entity[IDX_ENTITY_LAST_POS]:
                entity[IDX_ENTITY_LAST_POS] = [
                        0,
                        0,
                        entity[IDX_ENTITY_ROT][0]]
        entity[IDX_ENTITY_LAST_POS][0] = entity[IDX_ENTITY_POS][0]
        entity[IDX_ENTITY_LAST_POS][1] = entity[IDX_ENTITY_POS][1]

        entity[IDX_ENTITY_POS][0] = x_pos
        entity[IDX_ENTITY_POS][1] = y_pos

        _call_pos_listeners(state, entity_name, get_pos(state, entity_name))

def add_pos(state, entity_name, x_pos, y_pos):
        """
        TODO
        """
        entity = get(state, entity_name)
        if not entity[IDX_ENTITY_LAST_POS]:
                entity[IDX_ENTITY_LAST_POS] = [
                        0,
                        0,
                        entity[IDX_ENTITY_ROT][0]]
        entity[IDX_ENTITY_LAST_POS][0] = entity[IDX_ENTITY_POS][0]
        entity[IDX_ENTITY_LAST_POS][1] = entity[IDX_ENTITY_POS][1]

        entity[IDX_ENTITY_POS][0] += x_pos
        entity[IDX_ENTITY_POS][1] += y_pos

        _call_pos_listeners(state, entity_name, get_pos(state, entity_name))

def get_last_pos(state, entity_name):
        """
        TODO
        """
        return get(state, entity_name)[IDX_ENTITY_LAST_POS]

def get_pos_offset(state, entity_name):
        """
        TODO
        """
        entity = get(state, entity_name)
        return (entity[IDX_ENTITY_POS_OFFSET][0], entity[IDX_ENTITY_POS_OFFSET][1])

def get_rot(state, entity_name):
        """
        TODO
        """
        return get(state, entity_name)[IDX_ENTITY_ROT][0]

def set_rot(state, entity_name, rot):
        """
        TODO
        """
        entity = get(state, entity_name)
        if not entity[IDX_ENTITY_LAST_POS]:
                entity[IDX_ENTITY_LAST_POS] = [
                        entity[IDX_ENTITY_POS][0],
                        entity[IDX_ENTITY_POS][1],
                        0]
        entity[IDX_ENTITY_LAST_POS][2] = entity[IDX_ENTITY_ROT][0]

        entity[IDX_ENTITY_ROT][0] = rot

def undo_last_move(state, entity_name):
        """
        TODO
        """
        entity = get(state, entity_name)
        if entity[IDX_ENTITY_LAST_POS]:
                entity[IDX_ENTITY_POS][0] = entity[IDX_ENTITY_LAST_POS][0]
                entity[IDX_ENTITY_POS][1] = entity[IDX_ENTITY_LAST_POS][1]
                entity[IDX_ENTITY_ROT][0] = entity[IDX_ENTITY_LAST_POS][2]
                entity[IDX_ENTITY_LAST_POS] = None
                _call_pos_listeners(state, entity_name, get_pos(state, entity_name))

def insert(state, entity_name, sprite_defs, pos, rot=0, pos_offset=[0, 0], collision=None):
        """
        TODO
        """
        state[globals.IDX_STATE_ENTITIES][IDX_ENTITIES_TABLE][entity_name] = [
                [pos[0], pos[1]],
                [rot],
                pos_offset,
                None,
                None,
                [],
                True if collision else None,]

        if collision:
                collisions.add(state, entity_name, collision[0], collision[1])

        entity = get(state, entity_name)
        default_sprite = None
        for sprite_name, sprite_def in sprite_defs.iteritems():
                entity[IDX_ENTITY_SPRITES].append(sprite_name)

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
        enabled_sprite_name = entity[IDX_ENTITY_ENABLED_SPRITE]

        if enabled_sprite_name == sprite_name:
                sprites.set_enable(state, full_sprite_name, False)

        sprites.delete(state, full_sprite_name)

        sprites.insert(state, full_sprite_name,
                sprite_def["textures"],
                speed=sprite_def["speed"],
                pos=entity[IDX_ENTITY_POS],
                rot_list=entity[IDX_ENTITY_ROT],
                pos_offset=entity[IDX_ENTITY_POS_OFFSET],
                enable=enable,)

        if enabled_sprite_name == sprite_name:
                sprites.set_enable(state, full_sprite_name, True)

def delete(state, entity_name):
        """
        TODO
        """
        entity = get(state, entity_name)
        if entity:
                sprites.set_enable(state, _get_full_sprite_name(entity_name, entity[IDX_ENTITY_ENABLED_SPRITE]), False)
                for sprite_name in entity[IDX_ENTITY_SPRITES]:
                        sprites.delete(state, _get_full_sprite_name(entity_name, sprite_name))

                if entity[IDX_ENTITY_COLLISION]:
                        collisions.delete(state, entity_name)

                del state[globals.IDX_STATE_ENTITIES][IDX_ENTITIES_TABLE][entity_name]

def set_active_sprite(state, entity_name, sprite_name):
        """
        TODO
        """
        entity = get(state, entity_name)
        if entity[IDX_ENTITY_ENABLED_SPRITE]:
                sprites.set_enable(state, _get_full_sprite_name(entity_name, entity[IDX_ENTITY_ENABLED_SPRITE]), False)
        sprites.set_enable(state, _get_full_sprite_name(entity_name, sprite_name), True)
        entity[IDX_ENTITY_ENABLED_SPRITE] = sprite_name
