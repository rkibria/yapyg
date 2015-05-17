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
Collision algorithms
"""

cimport math_2d

cpdef int value_in_range(float value, float min_limit, float max_limit):
        """
        TODO
        """
        return (value >= min_limit) and (value <= max_limit)

cpdef int is_point_in_rect(tuple point, tuple rect):
        """
        rectangle = ("rectangle", x, y, w, h, rot)
        """
        cdef float r_x = rect[1]
        cdef float r_y = rect[2]
        cdef float r_w = rect[3]
        cdef float r_h = rect[4]
        cdef float r_rot = rect[5]

        cdef float p_x = point[0]
        cdef float p_y = point[1]

        cdef tuple rotation_origin
        if r_rot != 0:
                rotation_origin = (r_x + (r_w / 2.0), r_y + (r_h / 2.0))
                p_x, p_y = math_2d.rotated_point(rotation_origin, (p_x, p_y), -r_rot)

        return value_in_range(p_x, r_x, r_x + r_w) and value_in_range(p_y, r_y, r_y + r_h)

cpdef tuple get_rect_points(tuple rect):
        """
        rect = ("rectangle", x, y, w, h, rot)
        """
        cdef float r_x = rect[1]
        cdef float r_y = rect[2]
        cdef float r_w = rect[3]
        cdef float r_h = rect[4]
        cdef float r_rot = rect[5]

        cdef tuple rect_rotated_points = (
                (r_x, r_y),
                (r_x + r_w, r_y),
                (r_x, r_y + r_h),
                (r_x + r_w, r_y + r_h),
                )

        cdef tuple rect_rotation_origin
        if r_rot != 0:
                rect_rotation_origin = (r_x + (r_w / 2.0), r_y + (r_h / 2.0))
                rect_rotated_points = (
                                math_2d.rotated_point(rect_rotation_origin, rect_rotated_points[0], r_rot),
                                math_2d.rotated_point(rect_rotation_origin, rect_rotated_points[1], r_rot),
                                math_2d.rotated_point(rect_rotation_origin, rect_rotated_points[2], r_rot),
                                math_2d.rotated_point(rect_rotation_origin, rect_rotated_points[3], r_rot),
                        )

        return rect_rotated_points

cpdef int is_rect_rect_collision(tuple rect_1, tuple rect_2, list contact_points):
        """
        rect = ("rectangle", x, y, w, h, rot)
        """
        cdef float r_x_1 = rect_1[1]
        cdef float r_y_1 = rect_1[2]
        cdef float r_w_1 = rect_1[3]
        cdef float r_h_1 = rect_1[4]
        cdef float r_rot_1 = rect_1[5]

        cdef float r_x_2 = rect_2[1]
        cdef float r_y_2 = rect_2[2]
        cdef float r_w_2 = rect_2[3]
        cdef float r_h_2 = rect_2[4]
        cdef float r_rot_2 = rect_2[5]

        cdef tuple rect_2_rotated_points = get_rect_points(rect_2)
        for point in rect_2_rotated_points:
                if (is_point_in_rect(point, rect_1)):
                        contact_points.append(point)

        cdef tuple rect_1_rotated_points
        if not contact_points:
                rect_1_rotated_points = get_rect_points(rect_1)
                for point in rect_1_rotated_points:
                        if (is_point_in_rect(point, rect_2)):
                                contact_points.append(point)

        return len(contact_points) > 0

cpdef int is_circle_circle_collision(tuple c_1, tuple c_2, list contact_points):
        """
        TODO
        """
        cdef float c1_x = c_1[1]
        cdef float c1_y = c_1[2]
        cdef float c1_r = c_1[3]

        cdef float c2_x = c_2[1]
        cdef float c2_y = c_2[2]
        cdef float c2_r = c_2[3]

        cdef float sq_1 = c2_x - c1_x
        sq_1 *= sq_1

        cdef float sq_2 = c2_y - c1_y
        sq_2 *= sq_2

        cdef float sq_3 = c1_r + c2_r
        sq_3 *= sq_3

        return sq_3 >= (sq_1 + sq_2)

cpdef int is_rect_circle_collision(tuple circ, tuple rect, list contact_points):
        """
        circ = ("circle", x, y, r)
        rect = ("rectangle", x, y, w, h, rot)
        """
        cdef float c_x = circ[1]
        cdef float c_y = circ[2]
        cdef float c_r = circ[3]

        cdef float r_x_left = rect[1]
        cdef float r_y_bottom = rect[2]
        cdef float r_w = rect[3]
        cdef float r_h = rect[4]
        cdef float r_rot = rect[5]

        cdef float r_x_right = r_x_left + r_w
        cdef float r_y_top = r_y_bottom + r_h

        cdef tuple r_centre = (r_x_left + (r_w / 2.0), r_y_bottom + (r_h / 2.0))
        if r_rot != 0:
                c_x, c_y = math_2d.rotated_point(r_centre, (c_x, c_y), -r_rot)

        cdef tuple found_contact_point = None
        cdef tuple corner_circle = None

        if c_x <= r_x_left:
                if c_y < r_y_bottom:
                        corner_circle = (r_x_left, r_y_bottom, c_r)
                elif c_y > r_y_top:
                        corner_circle = (r_x_left, r_y_top, c_r)
                else:
                        if c_x + c_r >= r_x_left:
                                found_contact_point = (r_x_left, c_y)
        elif c_x >= r_x_right:
                if c_y < r_y_bottom:
                        corner_circle = (r_x_right, r_y_bottom, c_r)
                elif c_y > r_y_top:
                        corner_circle = (r_x_right, r_y_top, c_r)
                else:
                        if c_x - c_r <= r_x_right:
                                found_contact_point = (r_x_right, c_y)
        else:
                if c_y < r_y_bottom:
                        if c_y + c_r >= r_y_bottom:
                                found_contact_point = (c_x, r_y_bottom)
                elif c_y > r_y_top:
                        if c_y - c_r <= r_y_top:
                                found_contact_point = (c_x, r_y_top)
                else:
                        found_contact_point = (c_x, c_y)

        if corner_circle:
                if is_point_in_circle((c_x, c_y), corner_circle):
                        found_contact_point = corner_circle

        if found_contact_point:
                contact_points.append(math_2d.rotated_point(r_centre, found_contact_point, r_rot))

        return len(contact_points) > 0

cpdef int is_point_in_circle(tuple point, tuple circ):
        """
        TODO
        """
        cdef float c_x = circ[0]
        cdef float c_y = circ[1]
        cdef float c_r = circ[2]

        cdef float p_x = point[0]
        cdef float p_y = point[1]

        cdef float x_d = p_x - c_x
        x_d *= x_d

        cdef float y_d = p_y - c_y
        y_d *= y_d

        cdef float dist = y_d + x_d

        return dist <= (c_r * c_r)
