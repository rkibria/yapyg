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

import globals
import texture_db
import tiles
import view
import text
import screen

IDX_SPRITES_TABLE = 0
IDX_SPRITES_RECTS_ROTS = 1
IDX_SPRITES_SIZES = 2
IDX_SPRITES_DRAW_ORDER = 3

IDX_SPRITE_ENABLE = 0
IDX_SPRITE_POS = 1
IDX_SPRITE_ROT = 2
IDX_SPRITE_TEXTURES = 3
IDX_SPRITE_SPEED = 4
IDX_SPRITE_SCALE = 5
IDX_SPRITE_POS_OFFSET = 6
IDX_SPRITE_TIME_SUM = 7
IDX_SPRITE_PHASE = 8

def initialize(list state):
        """
        TODO
        """
        state[globals.IDX_STATE_SPRITES] = [
                {},
                {},
                {},
                []]

def destroy(state):
        """
        TODO
        """
        state[globals.IDX_STATE_SPRITES] = None

def insert(state, sprite_name, textures, speed=0, pos_offset=(0, 0),
                scale=None, enable=True, pos=(0, 0), rot_list=(0,)):
        """
        TODO
        """
        if not scale:
                scale = (fixpoint.c_int2fix(1), fixpoint.c_int2fix(1))

        sprite = [
                enable,
                pos,
                rot_list,
                textures,
                speed,
                [scale[0], scale[1]],
                [pos_offset[0], pos_offset[1]],
                0,
                0,]
        state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE][sprite_name] = sprite
        for texture_part in textures:
                if type(texture_part) == tuple:
                        if texture_part[0] == "rectangle":
                                texture_db.insert_color_rect(state, texture_part[1], texture_part[2], texture_part, texture_part[3], texture_part[4], texture_part[5])
                        elif texture_part[0] == "ellipse":
                                texture_db.insert_color_ellipse(state, texture_part[1], texture_part[2], texture_part, texture_part[3], texture_part[4], texture_part[5])
                        elif texture_part[0] == "text":
                                texture_db.insert(state, texture_part, text.create_texture(state, texture_part[1], texture_part[2]))
                elif type(texture_part) == str:
                        texture_db.load(state, texture_part, texture_part)
        state[globals.IDX_STATE_SPRITES][IDX_SPRITES_DRAW_ORDER].append(sprite_name)
        state[globals.IDX_STATE_SPRITES][IDX_SPRITES_DRAW_ORDER].sort()

def delete(state, sprite_name):
        """
        TODO
        """
        if state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE].has_key(sprite_name):
                del state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE][sprite_name]
                state[globals.IDX_STATE_SPRITES][IDX_SPRITES_DRAW_ORDER].remove(sprite_name)

def get(state, sprite_name):
        """
        TODO
        """
        if state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE].has_key(sprite_name):
                return state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE][sprite_name]
        else:
                return None

def get_pos(state, sprite_name):
        """
        TODO
        """
        return get(state, sprite_name)[IDX_SPRITE_POS]

def get_rot(state, sprite_name):
        """
        TODO
        """
        return get(state, sprite_name)[IDX_SPRITE_ROT]

def set_enable(state, sprite_name, enable):
        """
        TODO
        """
        if enable == False:
                if state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE].has_key(sprite_name) and state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE][sprite_name][IDX_SPRITE_ENABLE] == True:
                        state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE][sprite_name][IDX_SPRITE_ENABLE] = False
                        if state[globals.IDX_STATE_SPRITES][IDX_SPRITES_RECTS_ROTS].has_key(sprite_name):
                                rect, rot = state[globals.IDX_STATE_SPRITES][IDX_SPRITES_RECTS_ROTS][sprite_name]
                                state[globals.IDX_STATE_SPRITES][IDX_SPRITES_SIZES][sprite_name] = rect.size
                                rect.size = (0, 0)
        else:
                if state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE].has_key(sprite_name) and state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE][sprite_name][IDX_SPRITE_ENABLE] == False:
                        state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE][sprite_name][IDX_SPRITE_ENABLE] = True
                        if state[globals.IDX_STATE_SPRITES][IDX_SPRITES_RECTS_ROTS].has_key(sprite_name):
                                rect, rot = state[globals.IDX_STATE_SPRITES][IDX_SPRITES_RECTS_ROTS][sprite_name]
                                if state[globals.IDX_STATE_SPRITES][IDX_SPRITES_SIZES].has_key(sprite_name):
                                        rect.size = state[globals.IDX_STATE_SPRITES][IDX_SPRITES_SIZES][sprite_name]

cdef void c_draw(list state, canvas, int frame_time_delta, int view_scale):
        """
        TODO
        """
        cdef tuple origin_xy
        origin_xy = screen.get_origin(state)

        cdef tuple view_pos
        view_pos = view.get_view_pos(state)

        cdef str sprite_name
        cdef list draw_order
        draw_order = state[globals.IDX_STATE_SPRITES][IDX_SPRITES_DRAW_ORDER]
        cdef list sprite
        cdef list pos
        cdef list scale
        cdef int rotate
        cdef int phase
        cdef int speed
        cdef int time_sum
        cdef int phase_increment

        for sprite_name in draw_order:
                sprite = state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE][sprite_name]

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
                if speed > 0:
                        time_sum = sprite[IDX_SPRITE_TIME_SUM]
                        time_sum += frame_time_delta
                        phase_increment = fixpoint.c_fix2int(fixpoint.c_div(time_sum, speed)) # int
                        if phase_increment < 1:
                                sprite[IDX_SPRITE_TIME_SUM] = time_sum
                                phase = sprite[IDX_SPRITE_PHASE]
                        else:
                                phase = (phase + phase_increment)
                                phase = phase % len(textures)
                                time_sum = time_sum % speed
                                sprite[IDX_SPRITE_TIME_SUM] = time_sum
                                sprite[IDX_SPRITE_PHASE] = phase

                c_draw_sprite(state, canvas, view_pos, view_scale, sprite_name,
                        texture_db.get(state, sprite[IDX_SPRITE_TEXTURES][phase]), pos, scale, rotate, origin_xy)

cdef void c_draw_sprite(list state, canvas, tuple view_pos, int view_scale, str sprite_name,
                texture, list pos, list scale, int rotate, tuple origin_xy):
        """
        TODO
        """
        cdef dict rectangles_rotates_dict
        rectangles_rotates_dict = state[globals.IDX_STATE_SPRITES][IDX_SPRITES_RECTS_ROTS]

        cdef int col
        cdef int row
        cdef int scaled_tile_size
        col = fixpoint.c_floor(pos[0])
        row = fixpoint.c_floor(pos[1])
        scaled_tile_size = fixpoint.c_mul(tiles.get_tile_size(state), view_scale)

        cdef int tile_x
        cdef int tile_y
        tile_x = fixpoint.c_mul(col, scaled_tile_size)
        tile_y = fixpoint.c_mul(row, scaled_tile_size)

        cdef int draw_x
        cdef int draw_y
        draw_x = tile_x - fixpoint.c_mul(view_pos[0], scaled_tile_size)
        draw_y = tile_y - fixpoint.c_mul(view_pos[1], scaled_tile_size)

        cdef tuple draw_pos
        draw_pos = (draw_x, draw_y)

        cdef tuple offset
        offset = (pos[0] - col, pos[1] - row,)

        cdef tuple offset_pos
        offset_pos = (draw_pos[0] + fixpoint.c_mul(scaled_tile_size, offset[0]) + origin_xy[0],
                        draw_pos[1] + fixpoint.c_mul(scaled_tile_size, offset[1]) + origin_xy[1])

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

                int_d_x = abs(int(rect.pos[0]) - fixpoint.c_fix2int(offset_pos[0]))
                int_d_y = abs(int(rect.pos[1]) - fixpoint.c_fix2int(offset_pos[1]))
                pos_changed = (int_d_x > 0 or int_d_y > 0)

                rot_changed = (abs(rot.angle - fixpoint.c_fix2int(rotate)) > 0)

                if pos_changed or rot_changed:
                        x = fixpoint.c_fix2int(offset_pos[0])
                        y = fixpoint.c_fix2int(offset_pos[1])

                        rect.pos = (x, y)

                        rot.angle = fixpoint.c_fix2int(rotate)

                        w = fixpoint.c_mul(fixpoint.c_int2fix(texture.size[0]), fixpoint.c_mul(view_scale, scale[0]))
                        h = fixpoint.c_mul(fixpoint.c_int2fix(texture.size[1]), fixpoint.c_mul(view_scale, scale[1]))
                        w = fixpoint.c_fix2int(w)
                        h = fixpoint.c_fix2int(h)

                        rot.origin = (x + w / 2, y + h / 2)
        else:
                with canvas:
                        PushMatrix()

                        w = fixpoint.c_mul(fixpoint.c_float2fix(float(texture.size[0])), fixpoint.c_mul(view_scale, scale[0]))
                        h = fixpoint.c_mul(fixpoint.c_float2fix(float(texture.size[1])), fixpoint.c_mul(view_scale, scale[1]))
                        w = fixpoint.c_fix2int(w)
                        h = fixpoint.c_fix2int(h)

                        x = fixpoint.c_fix2int(offset_pos[0])
                        y = fixpoint.c_fix2int(offset_pos[1])

                        rot = Rotate()
                        rot.angle = fixpoint.c_fix2int(rotate)
                        rot.axis = (0, 0, 1)
                        rot.origin = (x + w / 2, y + h / 2)

                        rect = Rectangle(
                                texture=texture,
                                pos=(x, y),
                                size=(w, h)
                                )

                        rectangles_rotates_dict[sprite_name] = (rect, rot,)

                        PopMatrix()