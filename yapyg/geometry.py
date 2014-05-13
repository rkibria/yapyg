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
Pure geometry operations
"""

import math

def is_point_in_circle(point, circ):
    """
    point = (x, y)
    circ = (x, y, r)
    """
    c_x = circ[0]
    c_y = circ[1]
    c_r = circ[2]
    p_x = point[0]
    p_y = point[1]

    y_d = p_y - c_y
    y_d *= y_d
    x_d = p_x - c_x
    x_d *= x_d
    dist = y_d + x_d

    return dist <= (c_r * c_r)

def is_point_in_rect(pos, rect):
    """
    rect = (row, col, w, h)
    """
    pos_x = pos[0]
    pos_y = pos[1]

    rect_x1 = rect[0]
    rect_y1 = rect[1]
    rect_x2 = rect_x1 + rect[2]
    rect_y2 = rect_y1 + rect[3]

    return ((pos_y >= rect_y1 and pos_y <= rect_y2)
        and (pos_x >= rect_x1 and pos_x <= rect_x2))

def is_rect_circle_collision(circ, rect, exact_check = False):
    """
    circ = (y, x, r)
    rect = (y, x, h, w)
    """
    c_y = circ[0]
    c_x = circ[1]
    c_r = circ[2]
    r_y1 = rect[0]
    r_x1 = rect[1]
    r_h = rect[2]
    r_w = rect[3]
    r_x2 = r_x1 + r_w
    r_y3 = r_y1 + r_h

    circle_outside = True

    if not exact_check:
        circle_outside = (c_x < r_x1 - c_r or c_x > r_x2 + c_r
            or c_y < r_y1 - c_r or c_y > r_y3 + c_r)
    else:
        corner_circles = (
            (r_y1, r_x1, c_r),
            (r_y1, r_x2, c_r),
            (r_y3, r_x1, c_r),
            (r_y3, r_x2, c_r),
        )
        circle_point = (c_y, c_x)
        for corner_circle in corner_circles:
            circle_outside = not is_point_in_circle(circle_point, corner_circle)
            if not circle_outside:
                break
        if circle_outside:
            if ((c_x >= r_x1 and c_x <= r_x2)
                or
                (c_y >= r_y1 and c_y <= r_y3)
                ):
                circle_outside = (c_x < r_x1 - c_r or c_x > r_x2 + c_r
                    or c_y < r_y1 - c_r or c_y > r_y3 + c_r)

    is_collision = not circle_outside
    return is_collision

def is_circle_circle_collision(c_1, c_2):
    """
    circ = (x, y, r): x/y = center, r = radius

    Test if distance between circle centers is smaller
    than the sum of circle radii.
    """
    sq_1 = (c_2[0] - c_1[0])
    sq_1 *= sq_1

    sq_2 = (c_2[1] - c_1[1])
    sq_2 *= sq_2

    sq_3 = (c_2[2] + c_1[2])
    sq_3 *= sq_3

    return sq_3 >= (sq_1 + sq_2)

def get_distance(pos1, pos2):
    """
    TODO
    """
    return math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1])

def get_rotation(pos1, pos2):
    """
    TODO
    """
    return math.degrees(math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0]))

def normal_vector(pos_1, pos_2):
    """
    TODO
    """
    distance = get_distance(pos_1, pos_2)
    return [((pos_2[x] - pos_1[x]) / distance) for x in xrange(0, len(pos_1))]

def dot_product(v_1, v_2):
    """
    TODO
    """
    return v_1[0] * v_2[0] + v_1[1] * v_2[1]

def vector_prod(vec, factor):
    """
    TODO
    """
    return [(vec[x] * factor) for x in xrange(0, len(vec))]

def vector_diff(v_1, v_2):
    """
    TODO
    """
    return [(v_1[x] - v_2[x]) for x in xrange(0, len(v_1))]

def vector_sum(v_1, v_2):
    """
    TODO
    """
    return [(v_1[x] + v_2[x]) for x in xrange(0, len(v_1))]

def components(normal_vector, v_vector):
    """
    TODO
    """
    parallel_vector = vector_prod(normal_vector,
        dot_product(normal_vector, v_vector))
    perpendicular_vector = vector_diff(v_vector, parallel_vector)
    return (parallel_vector, perpendicular_vector)

def get_vector_size(vec):
    """
    TODO
    """
    return math.hypot(vec[0], vec[1])
