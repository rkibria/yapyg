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
cimport view
cimport screen

import text

cdef int FIXP_1 = fixpoint.int2fix(1)

cdef int IDX_STATE_SPRITES

cdef int IDX_SPRITES_TABLE = 0
cdef int IDX_SPRITES_RECTS_ROTS = 1
cdef int IDX_SPRITES_SIZES = 2
cdef int IDX_SPRITES_DRAW_ORDER = 3
cdef int IDX_SPRITES_VIEW_SCALE = 4

cdef int IDX_SPRITE_ENABLE = 0
cdef int IDX_SPRITE_POS = 1
cdef int IDX_SPRITE_TEXTURES = 2
cdef int IDX_SPRITE_SPEED = 3
cdef int IDX_SPRITE_SCALE = 4
cdef int IDX_SPRITE_POS_OFFSET = 5
cdef int IDX_SPRITE_TIME_SUM = 6
cdef int IDX_SPRITE_PHASE = 7
cdef int IDX_SPRITE_SCREEN_RELATIVE = 8

cpdef initialize(int state_idx, list state):
        """
        TODO
        """
        global IDX_STATE_SPRITES
        IDX_STATE_SPRITES = state_idx
        state[IDX_STATE_SPRITES] = [
                {},
                {},
                {},
                [],
                FIXP_1,
                ]

cpdef destroy(list state):
        """
        TODO
        """
        state[IDX_STATE_SPRITES] = None

cpdef insert(list state, str sprite_name, tuple textures, int speed, list pos_offset,
             tuple scale, int enable, list pos, int screen_relative=False):
        """
        TODO
        """
        cdef list sprite_db = state[IDX_STATE_SPRITES]
        cdef dict sprites_table = sprite_db[IDX_SPRITES_TABLE]

        if not scale:
                scale = (fixpoint.int2fix(1), fixpoint.int2fix(1))

        cdef list text_textures = []
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

        cdef list sprite = [
                enable,
                pos,
                tuple(text_textures),
                speed,
                [scale[0], scale[1]],
                pos_offset,
                0,
                0,
                screen_relative,
                ]

        sprites_table[sprite_name] = sprite
        cdef list sprite_draw_order = sprite_db[IDX_SPRITES_DRAW_ORDER]

        sprite_draw_order.append(sprite_name)
        sprite_draw_order.sort()

cpdef delete(list state, str sprite_name):
        """
        TODO
        """
        cdef list sprite_db = state[IDX_STATE_SPRITES]
        cdef dict sprites_table = sprite_db[IDX_SPRITES_TABLE]
        if sprites_table.has_key(sprite_name):
                del sprites_table[sprite_name]
                sprite_db[IDX_SPRITES_DRAW_ORDER].remove(sprite_name)

cpdef list get(list state, str sprite_name):
        """
        TODO
        """
        cdef list sprite_db = state[IDX_STATE_SPRITES]
        cdef dict sprites_table = sprite_db[IDX_SPRITES_TABLE]
        if sprites_table.has_key(sprite_name):
                return sprites_table[sprite_name]
        else:
                return None

cpdef tuple get_pos(list state, str sprite_name):
        """
        TODO
        """
        return get(state, sprite_name)[IDX_SPRITE_POS]

cpdef set_enable(list state, str sprite_name, int enable):
        """
        TODO
        """
        cdef list sprite_db = state[IDX_STATE_SPRITES]
        cdef dict sprites_table = sprite_db[IDX_SPRITES_TABLE]
        cdef dict sprites_rects_rots = sprite_db[IDX_SPRITES_RECTS_ROTS]
        cdef dict sprite_sizes = sprite_db[IDX_SPRITES_SIZES]

        cdef list sprite
        cdef tuple offset_pos
        cdef tuple origin_xy
        cdef tuple view_pos
        cdef tuple sprite_size

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
                                                origin_xy = screen.get_origin(state)
                                                view_pos = view.get_view_pos(state)
                                                offset_pos = _get_screen_coords(state,
                                                                                view_pos,
                                                                                sprite_db[IDX_SPRITES_VIEW_SCALE],
                                                                                sprite[IDX_SPRITE_POS],
                                                                                origin_xy,
                                                                                sprite[IDX_SPRITE_SCREEN_RELATIVE]
                                                                                )
                                                sprite_size = sprite_sizes[sprite_name]
                                                rect_rot_attributes = _get_rect_rot_attributes(int(sprite_size[0]),
                                                                                               int(sprite_size[1]),
                                                                                               sprite_db[IDX_SPRITES_VIEW_SCALE],
                                                                                               sprite[IDX_SPRITE_SCALE],
                                                                                               offset_pos,
                                                                                               sprite[IDX_SPRITE_POS][2])
                                                rot.origin = rect_rot_attributes[1]
                                                rot.angle = rect_rot_attributes[2]
                                                rect.pos = rect_rot_attributes[0]
                                                rect.size = sprite_sizes[sprite_name]

cdef void c_draw(list state, canvas, int frame_time_delta, int view_scale):
        """
        TODO
        """
        cdef tuple origin_xy = screen.get_origin(state)
        cdef tuple view_pos = view.get_view_pos(state)
        cdef list sprite_db = state[IDX_STATE_SPRITES]
        cdef dict sprites_table = sprite_db[IDX_SPRITES_TABLE]
        cdef list draw_order = sprite_db[IDX_SPRITES_DRAW_ORDER]

        sprite_db[IDX_SPRITES_VIEW_SCALE] = view_scale

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
                pos = [sprite[IDX_SPRITE_POS][0], sprite[IDX_SPRITE_POS][1], sprite[IDX_SPRITE_POS][2]]
                scale = sprite[IDX_SPRITE_SCALE]
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
                        texture_db.get(state, texture_name), pos, scale, origin_xy, screen_relative)

cdef tuple _get_screen_coords(list state, tuple view_pos, int view_scale, list pos, tuple origin_xy, int screen_relative):
        """
        TODO
        """
        cdef int col = fixpoint.floor(pos[0])
        cdef int row = fixpoint.floor(pos[1])
        cdef int scaled_tile_size = fixpoint.mul(tiles.get_tile_size(state), view_scale)

        cdef int tile_x = fixpoint.mul(col, scaled_tile_size)
        cdef int tile_y = fixpoint.mul(row, scaled_tile_size)

        cdef int draw_x
        cdef int draw_y
        if not screen_relative:
                draw_x = tile_x - fixpoint.mul(view_pos[0], scaled_tile_size)
                draw_y = tile_y - fixpoint.mul(view_pos[1], scaled_tile_size)
        else:
                draw_x = tile_x
                draw_y = tile_y

        cdef tuple draw_pos = (draw_x, draw_y)
        cdef tuple offset = (pos[0] - col, pos[1] - row,)
        cdef int rotate = pos[2]
        cdef tuple offset_pos = (draw_pos[0] + fixpoint.mul(scaled_tile_size, offset[0]) + origin_xy[0],
                        draw_pos[1] + fixpoint.mul(scaled_tile_size, offset[1]) + origin_xy[1])
        return offset_pos

cdef tuple _get_rect_rot_attributes(int texture_w, int texture_h, int view_scale, list scale, tuple offset_pos, int rotate):
        """
        TODO
        """
        cdef int w = fixpoint.mul(fixpoint.int2fix(texture_w), fixpoint.mul(view_scale, scale[0]))
        cdef int h = fixpoint.mul(fixpoint.int2fix(texture_h), fixpoint.mul(view_scale, scale[1]))
        w = fixpoint.fix2int(w)
        h = fixpoint.fix2int(h)

        cdef int x = fixpoint.fix2int(offset_pos[0])
        cdef int y = fixpoint.fix2int(offset_pos[1])

        return ((x, y),
                (x + w / 2, y + h / 2),
                fixpoint.fix2int(rotate),
                (w, h),
                )

cdef void c_draw_sprite(list state, canvas, tuple view_pos, int view_scale, str sprite_name,
                texture, list pos, list scale, tuple origin_xy, int screen_relative):
        """
        TODO
        """
        cdef list sprite_db = state[IDX_STATE_SPRITES]
        cdef dict rectangles_rotates_dict = sprite_db[IDX_SPRITES_RECTS_ROTS]

        cdef int rotate = pos[2]
        cdef tuple offset_pos = _get_screen_coords(state, view_pos, view_scale, pos, origin_xy, screen_relative)

        cdef int int_d_x
        cdef int int_d_y
        cdef int pos_changed
        cdef int rot_changed
        cdef tuple rect_rot_attributes

        if rectangles_rotates_dict.has_key(sprite_name):
                rect, rot = rectangles_rotates_dict[sprite_name]
                if not rect.texture is texture:
                        rect.texture = texture

                int_d_x = abs(int(rect.pos[0]) - fixpoint.fix2int(offset_pos[0]))
                int_d_y = abs(int(rect.pos[1]) - fixpoint.fix2int(offset_pos[1]))
                pos_changed = (int_d_x > 0 or int_d_y > 0)

                rot_changed = (abs(rot.angle - fixpoint.fix2int(rotate)) > 0)

                if pos_changed or rot_changed:
                        rect_rot_attributes = _get_rect_rot_attributes(int(texture.size[0]), int(texture.size[1]),
                                                                       view_scale,scale, offset_pos, rotate)
                        rect.pos = rect_rot_attributes[0]
                        rot.origin = rect_rot_attributes[1]
                        rot.angle = rect_rot_attributes[2]
        else:
                with canvas:
                        rect_rot_attributes = _get_rect_rot_attributes(int(texture.size[0]), int(texture.size[1]), view_scale, scale, offset_pos, rotate)

                        PushMatrix()
                        rot = Rotate(angle=rect_rot_attributes[2],
                                     origin=rect_rot_attributes[1],
                                     axis=(0, 0, 1),
                                     )
                        rect = Rectangle(
                                texture=texture,
                                pos=rect_rot_attributes[0],
                                size=rect_rot_attributes[3],
                                )
                        PopMatrix()

                        rectangles_rotates_dict[sprite_name] = (rect, rot,)
