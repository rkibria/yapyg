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

import texture_db
import tiles
import view
import text

def initialize(state):
    """
    TODO
    """
    state["sprites"] = {}
    state["sprites"]["sprites"] = {}
    state["sprites"]["rectangles_rotates_dict"] = {}
    state["sprites"]["sprite_sizes_dict"] = {}

def destroy(state):
    """
    TODO
    """
    del state["sprites"]

def insert(state, sprite_name, textures, speed=0, pos_offset=(0, 0),
        scale=[1.0, 1.0], enable=True, pos=[0,0], rot_list=[0]):
    """
    TODO
    """
    sprite = {
        "enable": enable,
        "pos" : pos,
        "rot": rot_list,
        "textures" : textures,
        "speed": speed,
        "scale": scale,
        "pos_offset": pos_offset,
    }
    state["sprites"]["sprites"][sprite_name] = sprite
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
    del state["sprites"]["sprites"][sprite_name]

def get(state, sprite_name):
    """
    TODO
    """
    return state["sprites"]["sprites"][sprite_name]

def get_pos(state, sprite_name):
    """
    TODO
    """
    return get(state, sprite_name)["pos"]

def get_rot(state, sprite_name):
    """
    TODO
    """
    return get(state, sprite_name)["rot"]

def set_enable(state, sprite_name, enable):
    """
    TODO
    """
    if enable == False:
        if state["sprites"]["sprites"].has_key(sprite_name) and state["sprites"]["sprites"][sprite_name]["enable"] == True:
            state["sprites"]["sprites"][sprite_name]["enable"] = False
            if state["sprites"]["rectangles_rotates_dict"].has_key(sprite_name):
                rect, rot = state["sprites"]["rectangles_rotates_dict"][sprite_name]
                state["sprites"]["sprite_sizes_dict"][sprite_name] = rect.size
                rect.size = (0, 0)
    else:
        if state["sprites"]["sprites"].has_key(sprite_name) and state["sprites"]["sprites"][sprite_name]["enable"] == False:
            state["sprites"]["sprites"][sprite_name]["enable"] = True
            if state["sprites"]["rectangles_rotates_dict"].has_key(sprite_name):
                rect, rot = state["sprites"]["rectangles_rotates_dict"][sprite_name]
                if state["sprites"]["sprite_sizes_dict"].has_key(sprite_name):
                    rect.size = state["sprites"]["sprite_sizes_dict"][sprite_name]

def draw(state, canvas, frame_time_delta, view_scale):
    """
    TODO
    """
    view_pos = view.get_view_pos(state)
    for sprite_name, sprite in sorted(state["sprites"]["sprites"].iteritems()):
        if not sprite["enable"]:
            continue
        textures = sprite["textures"]
        pos = [sprite["pos"][0], sprite["pos"][1]]
        scale = sprite["scale"]
        rotate = sprite["rot"][0]
        phase = None

        if sprite.has_key("pos_offset"):
            pos[0] += sprite["pos_offset"][0]
            pos[1] += sprite["pos_offset"][1]

        if sprite.has_key("phase"):
            phase = sprite["phase"]
            speed = sprite["speed"]
            if speed > 0:
                time_sum = sprite["time_sum"]
                time_sum += int(frame_time_delta)
                phase_increment = int(time_sum / speed)
                if phase_increment < 1:
                    sprite["time_sum"] = time_sum
                    phase = sprite["phase"]
                else:
                    phase = (phase + phase_increment)
                    phase = phase % len(textures)
                    time_sum = time_sum % speed
                    sprite["time_sum"] = time_sum
                    sprite["phase"] = phase
        else:
            sprite["time_sum"] = 0
            sprite["phase"] = 0
            phase = 0
        _draw_sprite(state, canvas, view_pos, view_scale, sprite_name,
            texture_db.get(state, sprite["textures"][phase]), pos, scale, rotate)

def _draw_sprite(state, canvas, view_pos, view_scale, sprite_name, texture, pos, scale, rotate):
    """
    TODO
    """
    rectangles_rotates_dict = state["sprites"]["rectangles_rotates_dict"]
    col = int(pos[0])
    row = int(pos[1])
    scaled_tile_size = tiles.get_tile_size(state) * view_scale

    tile_x = col * scaled_tile_size
    tile_y = row * scaled_tile_size

    draw_x = tile_x - view_pos[0] * scaled_tile_size
    draw_y = tile_y - view_pos[1] * scaled_tile_size

    draw_pos = (draw_x, draw_y)
    offset = (pos[0] - col, pos[1] - row,)
    offset_pos = (int(draw_pos[0] + scaled_tile_size * offset[0]),
                 int(draw_pos[1] + scaled_tile_size * offset[1]))

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
