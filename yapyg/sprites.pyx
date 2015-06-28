# Copyright (c) 2015 Raihan Kibria
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

from libc.math cimport fmod, floor

from kivy.graphics import PushMatrix, Rectangle, Rotate, PopMatrix

cimport tiles
cimport texture_db
cimport view
cimport screen

import text

cdef int IDX_STATE_SPRITES

cdef int IDX_SPRITES_DICT = 0
cdef int IDX_SPRITES_RECTS_ROTS = 1
cdef int IDX_SPRITES_SIZES = 2
cdef int IDX_SPRITES_VIEW_SCALE = 3
cdef int IDX_SPRITES_DRAW_ORDER = 4

cdef int IDX_SPRITE_ENABLE = 0
cdef int IDX_SPRITE_POS = 1
cdef int IDX_SPRITE_TEXTURES = 2
cdef int IDX_SPRITE_SPEED = 3
cdef int IDX_SPRITE_SCALE = 4
cdef int IDX_SPRITE_POS_OFFSET = 5
cdef int IDX_SPRITE_TIME_SUM = 6
cdef int IDX_SPRITE_PHASE = 7
cdef int IDX_SPRITE_SCREEN_RELATIVE = 8
cdef int IDX_SPRITE_PLAYONCE = 9

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
                1.0,
                []
                ]

cpdef destroy(list state):
        """
        TODO
        """
        state[IDX_STATE_SPRITES] = None

cpdef insert(list state, str sprite_name, tuple textures, float speed, list pos_offset,
             tuple scale, int enable, list pos, int screen_relative=False, int play_once=False):
        """
        TODO
        """
        cdef list sprite_db = state[IDX_STATE_SPRITES]
        cdef dict sprites_dict = sprite_db[IDX_SPRITES_DICT]
        cdef dict sprites_rects_rots = sprite_db[IDX_SPRITES_RECTS_ROTS]
        cdef dict sprite_sizes = sprite_db[IDX_SPRITES_SIZES]
        cdef list sprite_draw_order = sprite_db[IDX_SPRITES_DRAW_ORDER]

        if not scale:
                scale = (1, 1)

        cdef list text_textures = []
        cdef str texture_name
        for texture_part in textures:
                texture_name = str(texture_part)
                text_textures.append(texture_name)

                if type(texture_part) == tuple:
                        if texture_part[0] == "rectangle":
                                texture_db.insert_color_rect(state, texture_part[1], texture_part[2],
                                                             texture_name, texture_part[3], texture_part[4],
                                                             texture_part[5])
                        elif texture_part[0] == "ellipse":
                                texture_db.insert_color_ellipse(state, texture_part[1], texture_part[2],
                                                                texture_name, texture_part[3], texture_part[4],
                                                                texture_part[5])
                        elif texture_part[0] == "text":
                                new_texture = text.create_texture(state, texture_part[1], texture_part[2])
                                texture_db.insert(state, texture_name, new_texture)
                                if sprites_rects_rots.has_key(sprite_name):
                                        rect, rot = sprites_rects_rots[sprite_name]
                                        rect.size = (new_texture.size[0] * scale[0], new_texture.size[1] * scale[1])
                                        sprite_sizes[sprite_name] = rect.size
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
                [pos_offset[0], pos_offset[1]],
                0,
                0,
                screen_relative,
                play_once,
                ]

        sprites_dict[sprite_name] = sprite
        if not sprite_name in sprite_draw_order:
                sprite_draw_order.append(sprite_name)

cpdef delete(list state, str sprite_name):
        """
        TODO
        """
        cdef list sprite_db = state[IDX_STATE_SPRITES]
        cdef dict sprites_dict = sprite_db[IDX_SPRITES_DICT]
        cdef list sprite_draw_order = sprite_db[IDX_SPRITES_DRAW_ORDER]
        if sprites_dict.has_key(sprite_name):
                del sprites_dict[sprite_name]
                sprite_draw_order.remove(sprite_name)

cpdef list get(list state, str sprite_name):
        """
        TODO
        """
        cdef list sprite_db = state[IDX_STATE_SPRITES]
        cdef dict sprites_dict = sprite_db[IDX_SPRITES_DICT]
        if sprites_dict.has_key(sprite_name):
                return sprites_dict[sprite_name]
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
        cdef dict sprites_dict = sprite_db[IDX_SPRITES_DICT]
        cdef dict sprites_rects_rots = sprite_db[IDX_SPRITES_RECTS_ROTS]
        cdef dict sprite_sizes = sprite_db[IDX_SPRITES_SIZES]

        cdef list sprite
        cdef tuple offset_pos
        cdef tuple origin_xy
        cdef tuple view_pos
        cdef tuple sprite_size
        cdef list sprite_pos
        cdef list sprite_total_pos
        cdef list sprite_offset

        if sprites_dict.has_key(sprite_name):
                sprite = sprites_dict[sprite_name]

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
                                                sprite_pos = sprite[IDX_SPRITE_POS]
                                                sprite_offset = sprite[IDX_SPRITE_POS_OFFSET]
                                                sprite_total_pos = [sprite_pos[0] + sprite_offset[0],
                                                                    sprite_pos[1] + sprite_offset[1],
                                                                    sprite_pos[2]
                                                                    ]
                                                offset_pos = _get_screen_coords(state,
                                                                                view_pos,
                                                                                sprite_db[IDX_SPRITES_VIEW_SCALE],
                                                                                sprite_total_pos,
                                                                                origin_xy,
                                                                                sprite[IDX_SPRITE_SCREEN_RELATIVE]
                                                                                )
                                                sprite_size = sprite_sizes[sprite_name]
                                                rect_rot_attributes = _get_rect_rot_attributes(int(sprite_size[0]),
                                                                                               int(sprite_size[1]),
                                                                                               sprite_db[IDX_SPRITES_VIEW_SCALE],
                                                                                               sprite[IDX_SPRITE_SCALE],
                                                                                               offset_pos,
                                                                                               sprite_pos[2])
                                                rot.origin = rect_rot_attributes[1]
                                                rot.angle = rect_rot_attributes[2]
                                                rect.pos = rect_rot_attributes[0]
                                                rect.size = sprite_size

cdef void draw(list state, canvas, float frame_time_delta, float view_scale):
        """
        TODO
        """
        cdef tuple origin_xy = screen.get_origin(state)
        cdef tuple view_pos = view.get_view_pos(state)
        cdef list sprite_db = state[IDX_STATE_SPRITES]
        cdef dict sprites_dict = sprite_db[IDX_SPRITES_DICT]
        cdef list sprite_draw_order = sprite_db[IDX_SPRITES_DRAW_ORDER]

        sprite_db[IDX_SPRITES_VIEW_SCALE] = view_scale

        cdef str sprite_name
        cdef list sprite
        cdef list pos
        cdef list scale
        cdef float rotate
        cdef int phase
        cdef int speed
        cdef float time_sum
        cdef int phase_increment
        cdef str texture_name
        cdef tuple textures
        cdef int screen_relative
        cdef list sprite_pos
        cdef list sprite_pos_offset
        cdef int play_once

        for sprite_name in sprite_draw_order:
                sprite = sprites_dict[sprite_name]

                if not sprite[IDX_SPRITE_ENABLE]:
                        continue

                sprite_pos = sprite[IDX_SPRITE_POS]

                textures = sprite[IDX_SPRITE_TEXTURES]
                pos = [sprite_pos[0], sprite_pos[1], sprite_pos[2]]
                scale = sprite[IDX_SPRITE_SCALE]
                phase = 0

                sprite_pos_offset = sprite[IDX_SPRITE_POS_OFFSET]
                pos[0] += sprite_pos_offset[0]
                pos[1] += sprite_pos_offset[1]

                phase = sprite[IDX_SPRITE_PHASE]
                speed = sprite[IDX_SPRITE_SPEED]
                screen_relative = sprite[IDX_SPRITE_SCREEN_RELATIVE]
                play_once = sprite[IDX_SPRITE_PLAYONCE]

                if speed > 0:
                        time_sum = sprite[IDX_SPRITE_TIME_SUM]
                        time_sum += frame_time_delta
                        phase_increment = int(time_sum / speed) # int
                        if phase_increment < 1:
                                sprite[IDX_SPRITE_TIME_SUM] = time_sum
                                phase = sprite[IDX_SPRITE_PHASE]
                        else:
                                phase = (phase + phase_increment)
                                if phase >= len(textures) and play_once:
                                        set_enable(state, sprite_name, False)
                                        continue
                                phase = phase % len(textures)
                                time_sum = fmod(time_sum, speed)
                                sprite[IDX_SPRITE_TIME_SUM] = time_sum
                                sprite[IDX_SPRITE_PHASE] = phase

                texture_name = textures[phase]
                draw_sprite(state, canvas, view_pos, view_scale, sprite_name,
                            texture_db.get(state, texture_name), pos, scale,
                            origin_xy, screen_relative)

cdef tuple _get_screen_coords(list state, tuple view_pos, float view_scale, list pos,
                              tuple origin_xy, int screen_relative):
        """
        TODO
        """
        cdef float col = floor(pos[0])
        cdef float row = floor(pos[1])
        cdef float scaled_tile_size = tiles.get_tile_size(state) * view_scale

        cdef float tile_x = col * scaled_tile_size
        cdef float tile_y = row * scaled_tile_size

        cdef float draw_x
        cdef float draw_y
        if not screen_relative:
                draw_x = tile_x - (view_pos[0] * scaled_tile_size)
                draw_y = tile_y - (view_pos[1] * scaled_tile_size)
        else:
                draw_x = tile_x
                draw_y = tile_y

        cdef tuple draw_pos = (draw_x, draw_y)
        cdef tuple offset = (pos[0] - col, pos[1] - row,)
        cdef tuple offset_pos = (draw_pos[0] + (scaled_tile_size * offset[0]) + origin_xy[0],
                                 draw_pos[1] + (scaled_tile_size * offset[1]) + origin_xy[1])
        return offset_pos

cdef tuple _get_rect_rot_attributes(int texture_w, int texture_h, float view_scale, list scale,
                                    tuple offset_pos, float rotate):
        """
        TODO
        """
        cdef int w = int(texture_w * view_scale * scale[0])
        cdef int h = int(texture_h * view_scale * scale[1])

        cdef int x = int(offset_pos[0])
        cdef int y = int(offset_pos[1])

        return ((x, y),
                (x + w / 2, y + h / 2),
                rotate,
                (w, h),
                )

cdef void draw_sprite(list state, canvas, tuple view_pos, float view_scale, str sprite_name,
                texture, list pos, list scale, tuple origin_xy, int screen_relative):
        """
        TODO
        """
        cdef list sprite_db = state[IDX_STATE_SPRITES]
        cdef dict rectangles_rotates_dict = sprite_db[IDX_SPRITES_RECTS_ROTS]

        cdef float rotate = pos[2]
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

                int_d_x = abs(int(rect.pos[0] - offset_pos[0]))
                int_d_y = abs(int(rect.pos[1] - offset_pos[1]))
                pos_changed = (int_d_x > 1 or int_d_y > 1)

                rot_changed = abs(rot.angle - rotate) >= 0.05

                if pos_changed or rot_changed:
                        rect_rot_attributes = _get_rect_rot_attributes(int(texture.size[0]), int(texture.size[1]),
                                                                       view_scale,scale, offset_pos, rotate)
                        rect.pos = rect_rot_attributes[0]
                        rot.origin = rect_rot_attributes[1]
                        rot.angle = rect_rot_attributes[2]
        else:
                with canvas:
                        rect_rot_attributes = _get_rect_rot_attributes(int(texture.size[0]), int(texture.size[1]),
                                                                       view_scale, scale, offset_pos, rotate)

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
