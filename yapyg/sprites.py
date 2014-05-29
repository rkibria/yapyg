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

import globals
import texture_db
import tiles
import view
import text
import screen

IDX_SPRITES_TABLE = 0
IDX_SPRITES_RECTS_ROTS = 1
IDX_SPRITES_SIZES = 2

IDX_SPRITE_ENABLE = 0
IDX_SPRITE_POS = 1
IDX_SPRITE_ROT = 2
IDX_SPRITE_TEXTURES = 3
IDX_SPRITE_SPEED = 4
IDX_SPRITE_SCALE = 5
IDX_SPRITE_POS_OFFSET = 6
IDX_SPRITE_TIME_SUM = 7
IDX_SPRITE_PHASE = 8

def initialize(state):
        """
        TODO
        """
        state[globals.IDX_STATE_SPRITES] = [
                {},
                {},
                {},]

def destroy(state):
        """
        TODO
        """
        del state[globals.IDX_STATE_SPRITES]

def insert(state, sprite_name, textures, speed=0, pos_offset=(0, 0),
                scale=[1.0, 1.0], enable=True, pos=[0,0], rot_list=[0]):
        """
        TODO
        """
        sprite = [
                enable,
                pos,
                rot_list,
                textures,
                speed,
                scale,
                pos_offset,
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

def delete(state, sprite_name):
        """
        TODO
        """
        if state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE].has_key(sprite_name):
                del state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE][sprite_name]

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

def draw(state, canvas, frame_time_delta, view_scale):
        """
        TODO
        """
        origin_xy = screen.get_origin(state)
        view_pos = view.get_view_pos(state)
        for sprite_name, sprite in sorted(state[globals.IDX_STATE_SPRITES][IDX_SPRITES_TABLE].iteritems()):
                if not sprite[IDX_SPRITE_ENABLE]:
                        continue
                textures = sprite[IDX_SPRITE_TEXTURES]
                pos = [sprite[IDX_SPRITE_POS][0], sprite[IDX_SPRITE_POS][1]]
                scale = sprite[IDX_SPRITE_SCALE]
                rotate = sprite[IDX_SPRITE_ROT][0]
                phase = None

                pos[0] += sprite[IDX_SPRITE_POS_OFFSET][0]
                pos[1] += sprite[IDX_SPRITE_POS_OFFSET][1]

                phase = sprite[IDX_SPRITE_PHASE]
                speed = sprite[IDX_SPRITE_SPEED]
                if speed > 0:
                        time_sum = sprite[IDX_SPRITE_TIME_SUM]
                        time_sum += int(frame_time_delta)
                        phase_increment = int(time_sum / speed)
                        if phase_increment < 1:
                                sprite[IDX_SPRITE_TIME_SUM] = time_sum
                                phase = sprite[IDX_SPRITE_PHASE]
                        else:
                                phase = (phase + phase_increment)
                                phase = phase % len(textures)
                                time_sum = time_sum % speed
                                sprite[IDX_SPRITE_TIME_SUM] = time_sum
                                sprite[IDX_SPRITE_PHASE] = phase
                _draw_sprite(state, canvas, view_pos, view_scale, sprite_name,
                        texture_db.get(state, sprite[IDX_SPRITE_TEXTURES][phase]), pos, scale, rotate, origin_xy)

def _draw_sprite(state, canvas, view_pos, view_scale, sprite_name, texture, pos, scale, rotate, origin_xy):
        """
        TODO
        """
        rectangles_rotates_dict = state[globals.IDX_STATE_SPRITES][IDX_SPRITES_RECTS_ROTS]
        col = int(pos[0])
        row = int(pos[1])
        scaled_tile_size = tiles.get_tile_size(state) * view_scale

        tile_x = col * scaled_tile_size
        tile_y = row * scaled_tile_size

        draw_x = tile_x - view_pos[0] * scaled_tile_size
        draw_y = tile_y - view_pos[1] * scaled_tile_size

        draw_pos = (draw_x, draw_y)
        offset = (pos[0] - col, pos[1] - row,)
        offset_pos = (int(draw_pos[0] + scaled_tile_size * offset[0] + origin_xy[0]),
                                 int(draw_pos[1] + scaled_tile_size * offset[1] + origin_xy[1]))

        if rectangles_rotates_dict.has_key(sprite_name):
                rect, rot = rectangles_rotates_dict[sprite_name]
                if not rect.texture is texture:
                        rect.texture = texture

                pos_changed = (abs(rect.pos[0] - offset_pos[0]) > 1) or (abs(rect.pos[1] - offset_pos[1]) > 1)
                rot_changed = abs(rot.angle - rotate) > 1

                if pos_changed or rot_changed:
                        rect.pos = offset_pos
                        rot.angle = rotate
                        x = offset_pos[0]
                        y = offset_pos[1]
                        w = texture.size[0] * view_scale * scale[0]
                        h = texture.size[1] * view_scale * scale[1]
                        rot.origin = (x + w/2, y + h/2)
        else:
                with canvas:
                        PushMatrix()
                        x = offset_pos[0]
                        y = offset_pos[1]
                        w = texture.size[0] * view_scale * scale[0]
                        h = texture.size[1] * view_scale * scale[1]
                        rot = Rotate()
                        rot.angle = rotate
                        rot.axis = (0, 0, 1)
                        rot.origin = (x + w/2, y + h/2)
                        rect = Rectangle(
                                texture=texture,
                                pos=offset_pos,
                                size=(w, h)
                                )
                        rectangles_rotates_dict[sprite_name] = (rect, rot,)
                        PopMatrix()
