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

        cdef tuple rect_1_rotated_points = get_rect_points(rect_1)
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
        sq_1 = ((sq_1) * (sq_1))

        cdef float sq_2 = c2_y - c1_y
        sq_2 = ((sq_2) * (sq_2))

        cdef float sq_3 = c1_r + c2_r
        sq_3 = ((sq_3) * (sq_3))

        return sq_3 >= (sq_1 + sq_2)

cpdef int is_rect_circle_collision(tuple circ, tuple rect, list contact_points):
        """
        circ = ("circle", x, y, r)
        rect = ("rectangle", x, y, w, h, rot)
        """
        cdef float c_x = circ[1]
        cdef float c_y = circ[2]
        cdef float c_r = circ[3]

        cdef float r_x1 = rect[1]
        cdef float r_y1 = rect[2]
        cdef float r_w = rect[3]
        cdef float r_h = rect[4]
        cdef float r_rot = rect[5]

        cdef float r_x2 = r_x1 + r_w
        cdef float r_y3 = r_y1 + r_h

        cdef tuple rotated_circle
        if r_rot != 0:
                rotated_circle = math_2d.rotated_point((r_x1 + (r_w / 2.0), r_y1 + (r_h / 2.0)), (c_x, c_y), -r_rot)
                c_x = rotated_circle[0]
                c_y = rotated_circle[1]

        cdef int circle_outside = True

        cdef tuple corner_circles = (
                (r_y1, r_x1, c_r),
                (r_y1, r_x2, c_r),
                (r_y3, r_x1, c_r),
                (r_y3, r_x2, c_r),
        )

        cdef tuple circle_point = (c_y, c_x)

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

        return not circle_outside

cpdef int is_point_in_circle(tuple point, tuple circ):
        """
        TODO
        """
        cdef float c_x = circ[0]
        cdef float c_y = circ[1]
        cdef float c_r = circ[2]
        cdef float p_x = point[0]
        cdef float p_y = point[1]

        cdef float y_d = p_y - c_y
        y_d = (y_d * y_d)

        cdef float x_d = p_x - c_x
        x_d = (x_d * x_d)

        cdef float dist = y_d + x_d

        return dist <= (c_r * c_r)
