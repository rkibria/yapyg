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
2D Sprites
"""

from kivy.graphics import PushMatrix, Rectangle, Rotate, PopMatrix

cimport fixpoint
cimport tiles
cimport texture_db

import globals
import view
import text
import screen

cdef int IDX_SPRITES_TABLE
cdef int IDX_SPRITES_RECTS_ROT
cdef int IDX_SPRITES_SIZES
cdef int IDX_SPRITES_DRAW_ORDER

IDX_SPRITES_TABLE = 0
IDX_SPRITES_RECTS_ROTS = 1
IDX_SPRITES_SIZES = 2
IDX_SPRITES_DRAW_ORDER = 3

cdef int IDX_SPRITE_ENABLE
cdef int IDX_SPRITE_POS
cdef int IDX_SPRITE_ROT
cdef int IDX_SPRITE_TEXTURES
cdef int IDX_SPRITE_SPEED
cdef int IDX_SPRITE_SCALE
cdef int IDX_SPRITE_POS_OFFSET
cdef int IDX_SPRITE_TIME_SUM
cdef int IDX_SPRITE_PHASE
cdef int IDX_SPRITE_SCREEN_RELATIVE

IDX_SPRITE_ENABLE = 0
IDX_SPRITE_POS = 1
IDX_SPRITE_ROT = 2
IDX_SPRITE_TEXTURES = 3
IDX_SPRITE_SPEED = 4
IDX_SPRITE_SCALE = 5
IDX_SPRITE_POS_OFFSET = 6
IDX_SPRITE_TIME_SUM = 7
IDX_SPRITE_PHASE = 8
IDX_SPRITE_SCREEN_RELATIVE = 9

cpdef initialize(list state):
        """
        TODO
        """
        state[globals.IDX_STATE_SPRITES] = [
                {},
                {},
                {},
                []]

cpdef destroy(list state):
        """
        TODO
        """
        state[globals.IDX_STATE_SPRITES] = None

cpdef insert(list state, str sprite_name, tuple textures, int speed, list pos_offset, tuple scale, int enable, list pos, list rot_list, int screen_relative=False):
        """
        TODO
        """
        cdef list sprite_db
        sprite_db = state[globals.IDX_STATE_SPRITES]

        cdef dict sprites_table
        sprites_table = sprite_db[IDX_SPRITES_TABLE]

        if not scale:
                scale = (fixpoint.int2fix(1), fixpoint.int2fix(1))

        cdef list text_textures
        text_textures = []
        for texture_part in textures:
                texture_name = str(texture_part)
                text_textures.append(texture_name)

                if type(texture_part) == tuple:
                        if texture_part[0] == "rectangle":
                                texture_db.insert_color_rect(state, texture_part[1], texture_part[2], texture_name, texture_part[3], texture_part[4], texture_part[5])
                        elif texture_part[0] == "ellipse":
                                texture_db.insert_color_ellipse(state, texture_part[1], texture_part[2], texture_name, texture_part[3], texture_part[4], texture_part[5])
                        elif texture_part[0] == "text":
                                texture_db.insert(state, texture_name, text.create_texture(state, texture_part[1], texture_part[2]))
                        else:
                                print "unknown texture type", texture_part[0]
                elif type(texture_part) == str:
                        texture_db.load(state, texture_part, texture_part)

        cdef list sprite
        sprite = [
                enable,
                pos,
                rot_list,
                tuple(text_textures),
                speed,
                [scale[0], scale[1]],
                pos_offset,
                0,
                0,
                screen_relative,
                ]

        sprites_table[sprite_name] = sprite

        cdef list sprite_draw_order
        sprite_draw_order = sprite_db[IDX_SPRITES_DRAW_ORDER]

        sprite_draw_order.append(sprite_name)
        sprite_draw_order.sort()

cpdef delete(list state, str sprite_name):
        """
        TODO
        """
        if state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE].has_key(sprite_name):
                del state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE][sprite_name]
                state[globals.IDX_STATE_SPRITES][IDX_SPRITES_DRAW_ORDER].remove(sprite_name)

cpdef list get(list state, str sprite_name):
        """
        TODO
        """
        if state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE].has_key(sprite_name):
                return state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE][sprite_name]
        else:
                return None

cpdef tuple get_pos(list state, str sprite_name):
        """
        TODO
        """
        return get(state, sprite_name)[IDX_SPRITE_POS]

cpdef int get_rot(list state, str sprite_name):
        """
        TODO
        """
        return get(state, sprite_name)[IDX_SPRITE_ROT]

cpdef set_enable(list state, str sprite_name, int enable):
        """
        TODO
        """
        cdef list sprite_db
        sprite_db = state[globals.IDX_STATE_SPRITES]

        cdef dict sprites_table
        sprites_table = sprite_db[IDX_SPRITES_TABLE]

        cdef dict sprites_rects_rots
        sprites_rects_rots = sprite_db[IDX_SPRITES_RECTS_ROTS]

        cdef dict sprite_sizes
        sprite_sizes = sprite_db[IDX_SPRITES_SIZES]

        cdef list sprite
        if sprites_table.has_key(sprite_name):
                sprite = sprites_table[sprite_name]

                if enable == False:
                        if sprite[IDX_SPRITE_ENABLE] == True:
                                sprite[IDX_SPRITE_ENABLE] = False
                                if sprites_rects_rots.has_key(sprite_name):
                                        rect, rot = sprites_rects_rots[sprite_name]
                                        sprite_sizes[sprite_name] = rect.size
                                        rect.size = (0, 0)
                else:
                        if sprite[IDX_SPRITE_ENABLE] == False:
                                sprite[IDX_SPRITE_ENABLE] = True
                                if sprites_rects_rots.has_key(sprite_name):
                                        rect, rot = sprites_rects_rots[sprite_name]
                                        if sprite_sizes.has_key(sprite_name):
                                                rect.size = sprite_sizes[sprite_name]

cdef void c_draw(list state, canvas, int frame_time_delta, int view_scale):
        """
        TODO
        """
        cdef tuple origin_xy
        origin_xy = screen.get_origin(state)

        cdef tuple view_pos
        view_pos = view.get_view_pos(state)

        cdef list sprite_db
        sprite_db = state[globals.IDX_STATE_SPRITES]

        cdef dict sprites_table
        sprites_table = sprite_db[IDX_SPRITES_TABLE]

        cdef list draw_order
        draw_order = sprite_db[IDX_SPRITES_DRAW_ORDER]

        cdef str sprite_name
        cdef list sprite
        cdef list pos
        cdef list scale
        cdef int rotate
        cdef int phase
        cdef int speed
        cdef int time_sum
        cdef int phase_increment
        cdef str texture_name
        cdef tuple textures
        cdef int screen_relative

        for sprite_name in draw_order:
                sprite = sprites_table[sprite_name]

                if not sprite[IDX_SPRITE_ENABLE]:
                        continue

                textures = sprite[IDX_SPRITE_TEXTURES]
                pos = [sprite[IDX_SPRITE_POS][0], sprite[IDX_SPRITE_POS][1]]
                scale = sprite[IDX_SPRITE_SCALE]
                rotate = sprite[IDX_SPRITE_ROT][0]
                phase = 0

                pos[0] += sprite[IDX_SPRITE_POS_OFFSET][0]
                pos[1] += sprite[IDX_SPRITE_POS_OFFSET][1]

                phase = sprite[IDX_SPRITE_PHASE]
                speed = sprite[IDX_SPRITE_SPEED]
                screen_relative = sprite[IDX_SPRITE_SCREEN_RELATIVE]

                if speed > 0:
                        time_sum = sprite[IDX_SPRITE_TIME_SUM]
                        time_sum += frame_time_delta
                        phase_increment = fixpoint.fix2int(fixpoint.div(time_sum, speed)) # int
                        if phase_increment < 1:
                                sprite[IDX_SPRITE_TIME_SUM] = time_sum
                                phase = sprite[IDX_SPRITE_PHASE]
                        else:
                                phase = (phase + phase_increment)
                                phase = phase % len(textures)
                                time_sum = time_sum % speed
                                sprite[IDX_SPRITE_TIME_SUM] = time_sum
                                sprite[IDX_SPRITE_PHASE] = phase

                texture_name = textures[phase]
                c_draw_sprite(state, canvas, view_pos, view_scale, sprite_name,
                        texture_db.get(state, texture_name), pos, scale, rotate, origin_xy, screen_relative)

cdef void c_draw_sprite(list state, canvas, tuple view_pos, int view_scale, str sprite_name,
                texture, list pos, list scale, int rotate, tuple origin_xy, int screen_relative):
        """
        TODO
        """
        cdef list sprite_db
        sprite_db = state[globals.IDX_STATE_SPRITES]

        cdef dict rectangles_rotates_dict
        rectangles_rotates_dict = sprite_db[IDX_SPRITES_RECTS_ROTS]

        cdef int col
        cdef int row
        cdef int scaled_tile_size
        col = fixpoint.floor(pos[0])
        row = fixpoint.floor(pos[1])
        scaled_tile_size = fixpoint.mul(tiles.get_tile_size(state), view_scale)

        cdef int tile_x
        cdef int tile_y
        tile_x = fixpoint.mul(col, scaled_tile_size)
        tile_y = fixpoint.mul(row, scaled_tile_size)

        cdef int draw_x
        cdef int draw_y
        if not screen_relative:
                draw_x = tile_x - fixpoint.mul(view_pos[0], scaled_tile_size)
                draw_y = tile_y - fixpoint.mul(view_pos[1], scaled_tile_size)
        else:
                draw_x = tile_x
                draw_y = tile_y

        cdef tuple draw_pos
        draw_pos = (draw_x, draw_y)

        cdef tuple offset
        offset = (pos[0] - col, pos[1] - row,)

        cdef tuple offset_pos
        offset_pos = (draw_pos[0] + fixpoint.mul(scaled_tile_size, offset[0]) + origin_xy[0],
                        draw_pos[1] + fixpoint.mul(scaled_tile_size, offset[1]) + origin_xy[1])

        cdef int int_d_x
        cdef int int_d_y
        cdef int pos_changed
        cdef int rot_changed
        cdef int x
        cdef int y
        cdef int w
        cdef int h

        if rectangles_rotates_dict.has_key(sprite_name):
                rect, rot = rectangles_rotates_dict[sprite_name]
                if not rect.texture is texture:
                        rect.texture = texture

                int_d_x = abs(int(rect.pos[0]) - fixpoint.fix2int(offset_pos[0]))
                int_d_y = abs(int(rect.pos[1]) - fixpoint.fix2int(offset_pos[1]))
                pos_changed = (int_d_x > 0 or int_d_y > 0)

                rot_changed = (abs(rot.angle - fixpoint.fix2int(rotate)) > 0)

                if pos_changed or rot_changed:
                        x = fixpoint.fix2int(offset_pos[0])
                        y = fixpoint.fix2int(offset_pos[1])

                        rect.pos = (x, y)

                        rot.angle = fixpoint.fix2int(rotate)

                        w = fixpoint.mul(fixpoint.int2fix(texture.size[0]), fixpoint.mul(view_scale, scale[0]))
                        h = fixpoint.mul(fixpoint.int2fix(texture.size[1]), fixpoint.mul(view_scale, scale[1]))
                        w = fixpoint.fix2int(w)
                        h = fixpoint.fix2int(h)

                        rot.origin = (x + w / 2, y + h / 2)
        else:
                with canvas:
                        PushMatrix()

                        w = fixpoint.mul(fixpoint.float2fix(float(texture.size[0])), fixpoint.mul(view_scale, scale[0]))
                        h = fixpoint.mul(fixpoint.float2fix(float(texture.size[1])), fixpoint.mul(view_scale, scale[1]))
                        w = fixpoint.fix2int(w)
                        h = fixpoint.fix2int(h)

                        x = fixpoint.fix2int(offset_pos[0])
                        y = fixpoint.fix2int(offset_pos[1])

                        rot = Rotate()
                        rot.angle = fixpoint.fix2int(rotate)
                        rot.axis = (0, 0, 1)
                        rot.origin = (x + w / 2, y + h / 2)

                        rect = Rectangle(
                                texture=texture,
                                pos=(x, y),
                                size=(w, h)
                                )

                        rectangles_rotates_dict[sprite_name] = (rect, rot,)

                        PopMatrix()
