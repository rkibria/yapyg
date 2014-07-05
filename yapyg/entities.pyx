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

cimport sprites
cimport collisions
cimport fixpoint

import globals

IDX_ENTITIES_TABLE = 0

IDX_ENTITY_POS = 0
IDX_ENTITY_POS_OFFSET = 1
IDX_ENTITY_ENABLED_SPRITE = 2
IDX_ENTITY_LAST_POS = 3
IDX_ENTITY_SPRITES = 4
IDX_ENTITY_COLLISION = 5

cpdef initialize(list state):
        """
        TODO
        """
        state[globals.IDX_STATE_ENTITIES] = [
                {},
                ]

cpdef destroy(list state):
        """
        TODO
        """
        state[globals.IDX_STATE_ENTITIES] = None

cpdef insert(list state, str entity_name, dict sprite_defs, tuple pos, tuple pos_offset=(0, 0), tuple collision=None, int screen_relative=False):
        """
        TODO
        """
        cdef list entities_db
        entities_db = state[globals.IDX_STATE_ENTITIES]

        cdef dict entities_table
        entities_table = entities_db[IDX_ENTITIES_TABLE]

        cdef list entity
        entity = [
                [pos[0], pos[1], pos[2]],
                [pos_offset[0], pos_offset[1]],
                None,
                None,
                [],
                True if collision else None,
                ]
        entities_table[entity_name] = entity

        if collision:
                collisions.add(state, entity_name, collision)

        cdef str default_sprite
        default_sprite = None

        cdef str sprite_name
        cdef dict sprite_def
        for sprite_name, sprite_def in sprite_defs.iteritems():

                entity[IDX_ENTITY_SPRITES].append(sprite_name)

                if sprite_name[0] == "*":
                        default_sprite = sprite_name

                set_sprite(state, entity_name, sprite_name, sprite_def, False, screen_relative)

        if default_sprite:
                set_active_sprite(state, entity_name, default_sprite)

cpdef set_sprite(list state, str entity_name, str sprite_name, dict sprite_def, int enable=False, int screen_relative=False):
        """
        TODO
        """
        cdef list entity
        entity = get(state, entity_name)

        cdef str full_sprite_name
        cdef tuple sprite_textures
        cdef int sprite_speed
        cdef list sprite_pos_offset
        cdef tuple sprite_scale
        cdef int sprite_enable
        cdef list sprite_pos
        cdef list sprite_rot_list

        cdef str enabled_sprite_name

        if entity:
                full_sprite_name = c_get_full_sprite_name(entity_name, sprite_name)

                sprite_textures = sprite_def["textures"]

                sprite_speed = 0
                if sprite_def.has_key("speed"):
                        sprite_speed = sprite_def["speed"]

                sprite_pos_offset = entity[IDX_ENTITY_POS_OFFSET]

                sprite_scale = (fixpoint.int2fix(1), fixpoint.int2fix(1))

                sprite_enable = enable

                sprite_pos = entity[IDX_ENTITY_POS]

                enabled_sprite_name = entity[IDX_ENTITY_ENABLED_SPRITE]
                if enabled_sprite_name == sprite_name:
                        sprites.set_enable(state, full_sprite_name, False)

                sprites.delete(state, full_sprite_name)

                sprites.insert(state,
                        full_sprite_name,
                        sprite_textures,
                        sprite_speed,
                        sprite_pos_offset,
                        sprite_scale,
                        sprite_enable,
                        sprite_pos,
                        screen_relative,
                        )

                if enabled_sprite_name == sprite_name:
                        sprites.set_enable(state, full_sprite_name, True)

cpdef set_active_sprite(list state, str entity_name, str sprite_name):
        """
        TODO
        """
        cdef list entity
        entity = get(state, entity_name)
        if entity:
                if entity[IDX_ENTITY_ENABLED_SPRITE]:
                        sprites.set_enable(state, c_get_full_sprite_name(entity_name, entity[IDX_ENTITY_ENABLED_SPRITE]), False)
                sprites.set_enable(state, c_get_full_sprite_name(entity_name, sprite_name), True)
                entity[IDX_ENTITY_ENABLED_SPRITE] = sprite_name

cpdef delete(list state, str entity_name):
        """
        TODO
        """
        cdef list entity
        entity = get(state, entity_name)
        if entity:
                sprites.set_enable(state, c_get_full_sprite_name(entity_name, entity[IDX_ENTITY_ENABLED_SPRITE]), False)
                for sprite_name in entity[IDX_ENTITY_SPRITES]:
                        sprites.delete(state, c_get_full_sprite_name(entity_name, sprite_name))

                if entity[IDX_ENTITY_COLLISION]:
                        collisions.delete(state, entity_name)

                del state[globals.IDX_STATE_ENTITIES][IDX_ENTITIES_TABLE][entity_name]

cdef c_call_pos_listeners(list state, str entity_name, tuple pos):
        """
        TODO
        """
        collisions.entity_pos_listener(state, entity_name, pos)

cdef str c_get_full_sprite_name(str entity_name, str sprite_name):
        """
        TODO
        """
        return entity_name + "_" + sprite_name

cpdef list get(list state, str entity_name):
        """
        TODO
        """
        cdef list entities_db
        entities_db = state[globals.IDX_STATE_ENTITIES]

        cdef dict entities_table
        entities_table = entities_db[IDX_ENTITIES_TABLE]

        if entities_table.has_key(entity_name):
                return entities_table[entity_name]
        else:
                return None

cpdef tuple get_pos(list state, str entity_name):
        """
        TODO
        """
        cdef list entity
        entity = get(state, entity_name)

        cdef list pos
        if entity:
                pos = entity[IDX_ENTITY_POS]
                return tuple(pos)
        else:
                return None

cpdef tuple get_last_pos(list state, str entity_name):
        """
        TODO
        """
        cdef list entity
        entity = get(state, entity_name)

        cdef tuple last_pos
        if entity:
                last_pos = entity[IDX_ENTITY_LAST_POS]
                return last_pos
        else:
                return None

cpdef tuple get_pos_offset(list state, str entity_name):
        """
        TODO
        """
        cdef list entity
        entity = get(state, entity_name)

        cdef list pos_offset
        if entity:
                pos_offset = entity[IDX_ENTITY_POS_OFFSET]
                return tuple(pos_offset)
        else:
                return None

cdef int FIXP_360 = fixpoint.int2fix(360)

cdef void normalize_rotation(entity):
        cdef int old_rot = entity[IDX_ENTITY_POS][2]
        cdef int modulo_rot = fixpoint.modulo(old_rot, FIXP_360)
        entity[IDX_ENTITY_POS][2] = modulo_rot

cpdef set_pos(list state, str entity_name, int x_pos, int y_pos, int rot):
        """
        TODO
        """
        cdef list entity
        entity = get(state, entity_name)

        cdef tuple old_pos
        if entity:
                old_pos = tuple(entity[IDX_ENTITY_POS])

                entity[IDX_ENTITY_LAST_POS] = tuple(entity[IDX_ENTITY_POS])

                if (x_pos, y_pos, rot) == old_pos:
                        return

                entity[IDX_ENTITY_POS][0] = x_pos
                entity[IDX_ENTITY_POS][1] = y_pos
                entity[IDX_ENTITY_POS][2] = rot
                
                normalize_rotation(entity)

                c_call_pos_listeners(state, entity_name, tuple(entity[IDX_ENTITY_POS]))

cpdef add_pos(list state, str entity_name, int x_pos, int y_pos, int rot):
        """
        TODO
        """
        cdef list entity
        entity = get(state, entity_name)

        if entity:
                entity[IDX_ENTITY_LAST_POS] = tuple(entity[IDX_ENTITY_POS])

                if (x_pos, y_pos, rot) == (0, 0, 0):
                        return

                entity[IDX_ENTITY_POS][0] += x_pos
                entity[IDX_ENTITY_POS][1] += y_pos
                entity[IDX_ENTITY_POS][2] += rot
                
                normalize_rotation(entity)

                c_call_pos_listeners(state, entity_name, tuple(entity[IDX_ENTITY_POS]))

cpdef undo_last_move(list state, str entity_name):
        """
        TODO
        """
        cdef list entity
        entity = get(state, entity_name)

        cdef tuple last_pos
        if entity:
                if entity[IDX_ENTITY_LAST_POS]:
                        last_pos = entity[IDX_ENTITY_LAST_POS]

                        entity[IDX_ENTITY_POS][0] = last_pos[0]
                        entity[IDX_ENTITY_POS][1] = last_pos[1]
                        entity[IDX_ENTITY_POS][2] = last_pos[2]

                        entity[IDX_ENTITY_LAST_POS] = None

                        c_call_pos_listeners(state, entity_name, last_pos)
