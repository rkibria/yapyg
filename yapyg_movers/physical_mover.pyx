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
from yapyg_widgets.display_widget import yapyg

"""
Simulate physical movement
"""

import math
import time

cimport yapyg.math_2d
cimport yapyg.movers
cimport yapyg.entities
cimport yapyg.collisions

IDX_MOVERS_PHYSICAL_MASS = yapyg.movers.IDX_MOVER_FIRST_PARAMETER
IDX_MOVERS_PHYSICAL_VX = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 1
IDX_MOVERS_PHYSICAL_VY = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 2
IDX_MOVERS_PHYSICAL_AX = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 3
IDX_MOVERS_PHYSICAL_AY = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 4
IDX_MOVERS_PHYSICAL_FRICTION = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 5
IDX_MOVERS_PHYSICAL_INELASTICITY = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 6
IDX_MOVERS_PHYSICAL_VR = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 7
IDX_MOVERS_PHYSICAL_ROT_FRICTION = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 8
IDX_MOVERS_PHYSICAL_ROT_DECAY = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 9
IDX_MOVERS_PHYSICAL_STICKYNESS = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 10

cdef str PHYSICS_MOVER_NAME = "physics"

cpdef add(list state,
                str entity_name,
                float mass,
                float vx,
                float vy,
                float ax,
                float ay,
                float friction,
                float inelasticity,
                float vr,
                float rot_friction,
                float rot_decay,
                float stickyness,
                int do_replace=False):
        """
        vr > 0: counter-clockwise
        """
        yapyg.movers.add(state,
                entity_name,
                c_create(entity_name,
                        mass,
                        vx, vy,
                        ax, ay,
                        friction,
                        inelasticity,
                        vr,
                        rot_friction,
                        rot_decay,
                        stickyness
                        ),
                        do_replace
                )

cdef list c_create(str entity_name,
                float mass,
                float vx,
                float vy,
                float ax,
                float ay,
                float friction,
                float inelasticity,
                float vr,
                float rot_friction,
                float rot_decay,
                float stickyness
                ):
        """
        TODO
        """
        return [PHYSICS_MOVER_NAME,
                run,
                entity_name,
                collision_handler,
                mass,
                vx,
                vy,
                ax,
                ay,
                friction,
                inelasticity,
                vr,
                rot_friction,
                rot_decay,
                stickyness,
                ]

cpdef run(list state, str entity_name, list mover, float frame_time_delta, list movers_to_delete):
        """
        TODO
        """
        cdef float v_x = mover[IDX_MOVERS_PHYSICAL_VX]
        cdef float v_y = mover[IDX_MOVERS_PHYSICAL_VY]

        cdef float a_x = mover[IDX_MOVERS_PHYSICAL_AX]
        cdef float a_y = mover[IDX_MOVERS_PHYSICAL_AY]

        cdef float a_x_halfed = (a_x / 2.0)
        cdef float a_y_halfed = (a_y / 2.0)
        cdef float time_squared = (frame_time_delta / 1000.0)
        time_squared = (time_squared * time_squared)

        # s = 0.5 a t^2 + v t
        cdef float delta_x = (((a_x_halfed * time_squared)) / 1000.0)
        cdef float delta_y = (((a_y_halfed * time_squared)) / 1000.0)

        delta_x += (((v_x * frame_time_delta)) / 1000.0)
        delta_y += (((v_y * frame_time_delta)) / 1000.0)

        # v = a t
        cdef float delta_vx = (((a_x * frame_time_delta)) / 1000.0)
        cdef float delta_vy = (((a_y * frame_time_delta)) / 1000.0)

        v_x += delta_vx
        v_y += delta_vy

        cdef float v_r = mover[IDX_MOVERS_PHYSICAL_VR]
        cdef float delta_rot = (v_r * frame_time_delta)

        cdef float stickyness = mover[IDX_MOVERS_PHYSICAL_STICKYNESS]
        if yapyg.math_2d.length((v_x, v_y,)) < stickyness:
                delta_x = 0
                delta_y = 0
                delta_rot = 0

        cdef float friction = mover[IDX_MOVERS_PHYSICAL_FRICTION]
        mover[IDX_MOVERS_PHYSICAL_VX] = (v_x * friction)
        mover[IDX_MOVERS_PHYSICAL_VY] = (v_y * friction)

        cdef float rot_decay = mover[IDX_MOVERS_PHYSICAL_ROT_DECAY]
        mover[IDX_MOVERS_PHYSICAL_VR] = (v_r * rot_decay)

        yapyg.entities.add_pos(state, entity_name, delta_x, delta_y, delta_rot)

        cdef tuple collision_result = yapyg.collisions.run(state, entity_name)
        if collision_result:
                collision_handler(*collision_result)

cdef float CONST_2PI = (2 * 3.14159265359)

cdef tuple c_compute_circle_torque(list state, float v_r, float v_x, float rot_friction, float circle_r, int clockw_right):
        """
        TODO
        """
        cdef float circle_circumference = ((CONST_2PI) * circle_r)

        cdef float v_p = (v_r * circle_circumference)

        if not clockw_right:
                v_p = -v_p

        cdef float delta = v_p + v_x
        delta = (rot_friction * delta)

        v_x = v_x - delta
        v_p = v_p - delta

        if not clockw_right:
                v_p = -v_p

        v_r = (v_p / circle_circumference)

        return (v_r, v_x)

cdef c_rectangle_circle_collision(list state,
                str rectangle_entity_name,
                str circle_entity_name,
                tuple abs_rectangle_shape,
                tuple abs_circle_shape,
                list rectangle_physical_mover,
                list circle_physical_mover):
        """
        TODO
        """
        yapyg.entities.undo_last_move(state, circle_entity_name)

        cdef float circle_x = abs_circle_shape[1]
        cdef float circle_y = abs_circle_shape[2]
        cdef float circle_r = abs_circle_shape[3]

        cdef float rect_x = abs_rectangle_shape[1]
        cdef float rect_y = abs_rectangle_shape[2]
        cdef float rect_w = abs_rectangle_shape[3]
        cdef float rect_h = abs_rectangle_shape[4]
        cdef float rect_r = abs_rectangle_shape[5]

        cdef tuple circle_move_vector
        cdef float inelasticity
        cdef tuple rotated_circle
        cdef float v_total
        cdef float corner_x
        cdef float corner_y
        cdef float angle
        cdef float angle_dx
        cdef float angle_dy
        cdef float new_vx
        cdef float new_vy

        cdef float v_r
        cdef float v_x
        cdef float v_y
        cdef float rot_friction

        if circle_physical_mover:
                circle_move_vector = (circle_physical_mover[IDX_MOVERS_PHYSICAL_VX], circle_physical_mover[IDX_MOVERS_PHYSICAL_VY])

                inelasticity = circle_physical_mover[IDX_MOVERS_PHYSICAL_INELASTICITY]

                # rotate coordinate system so that rectangle is not rotated
                if rect_r != 0:
                        rotated_circle = yapyg.math_2d.rotated_point(
                                (rect_x + (rect_w / 2.0), rect_y + (rect_h / 2.0)),
                                (circle_x, circle_y),
                                -rect_r)
                        circle_x = rotated_circle[0]
                        circle_y = rotated_circle[1]

                        circle_move_vector = yapyg.math_2d.rotated_point((0, 0), circle_move_vector, -rect_r)

                v_r = circle_physical_mover[IDX_MOVERS_PHYSICAL_VR]
                v_x = circle_move_vector[0]
                v_y = circle_move_vector[1]
                rot_friction = circle_physical_mover[IDX_MOVERS_PHYSICAL_ROT_FRICTION]

                if circle_y <= rect_y or circle_y >= rect_y + rect_h:
                        # circle centre below or above rectangle
                        if circle_x > rect_x and circle_x < rect_x + rect_w:
                                # lower/upper quadrant
                                if circle_y <= rect_y:
                                        # lower quadrant
                                        v_r, v_x = c_compute_circle_torque(state, v_r, v_x, rot_friction, circle_r, False)
                                        circle_move_vector = (v_x, circle_move_vector[1])
                                        circle_physical_mover[IDX_MOVERS_PHYSICAL_VR] = v_r

                                        circle_move_vector = (circle_move_vector[0],
                                                -abs(circle_move_vector[1]) * inelasticity)
                                else:
                                        # upper quadrant
                                        v_r, v_x = c_compute_circle_torque(state, v_r, v_x, rot_friction, circle_r, True)
                                        circle_move_vector = (v_x, circle_move_vector[1])
                                        circle_physical_mover[IDX_MOVERS_PHYSICAL_VR] = v_r

                                        circle_move_vector = (circle_move_vector[0],
                                                abs(circle_move_vector[1]) * inelasticity)
                        else:
                                # lower/upper left/right quadrant
                                v_total = yapyg.math_2d.length(circle_move_vector)
                                corner_y = 0
                                corner_x = 0
                                if circle_y <= rect_y:
                                        corner_y = rect_y
                                else:
                                        corner_y = rect_y + rect_h
                                if circle_x <= rect_x:
                                        corner_x = rect_x
                                else:
                                        corner_x = rect_x + rect_w
                                angle_dx = circle_x - corner_x
                                angle_dy = circle_y - corner_y
                                angle = math.atan2(angle_dy, angle_dx)

                                new_vy = math.sin(angle) * v_total
                                new_vx = math.cos(angle) * v_total
                                circle_move_vector = (
                                        (new_vx * inelasticity),
                                        (new_vy * inelasticity))
                else:
                        # circle same height as rectangle
                        if circle_x < rect_x:
                                # left quadrant
                                v_r, v_y = c_compute_circle_torque(state, v_r, v_y, rot_friction, circle_r, True)
                                circle_move_vector = (circle_move_vector[0], v_y)
                                circle_physical_mover[IDX_MOVERS_PHYSICAL_VR] = v_r

                                circle_move_vector = (
                                        -abs(circle_move_vector[0]) * inelasticity,
                                        circle_move_vector[1])
                        elif circle_x > rect_x + rect_w:
                                # right quadrant
                                v_r, v_y = c_compute_circle_torque(state, v_r, v_y, rot_friction, circle_r, False)
                                circle_move_vector = (circle_move_vector[0], v_y)
                                circle_physical_mover[IDX_MOVERS_PHYSICAL_VR] = v_r

                                circle_move_vector = (
                                        abs(circle_move_vector[0]) * inelasticity,
                                        circle_move_vector[1])
                        else:
                                # inside rectangle
                                # print "WARNING: physical mover circle inside a rectangle"
                                circle_move_vector = (-circle_move_vector[0], -circle_move_vector[1])

                # rotate back to original coordinate system
                circle_move_vector = yapyg.math_2d.rotated_point((0, 0), circle_move_vector, rect_r)
                circle_physical_mover[IDX_MOVERS_PHYSICAL_VX] = circle_move_vector[0]
                circle_physical_mover[IDX_MOVERS_PHYSICAL_VY] = circle_move_vector[1]

cdef void c_circle_circle_collision(list state,
                str circle_entity_name_1,
                str circle_entity_name_2,
                tuple abs_circle_shape_1,
                tuple abs_circle_shape_2,
                list circle_physical_mover_1,
                list circle_physical_mover_2):
        """
        TODO
        """
        yapyg.entities.undo_last_move(state, circle_entity_name_1)

        cdef tuple abs_pos_1 = (abs_circle_shape_1[1], abs_circle_shape_1[2])
        cdef tuple abs_pos_2 = (abs_circle_shape_2[1], abs_circle_shape_2[2])

        cdef tuple speed_vector_1 = (circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VX], circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VY])
        cdef tuple speed_vector_2 = (circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VX], circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VY])

        # torque creation
        cdef tuple centre_to_centre_vector = yapyg.math_2d.vector_diff(abs_pos_2, abs_pos_1)

        cdef float centre_to_centre_vector_angle = math.atan2(centre_to_centre_vector[1], centre_to_centre_vector[0])
        cdef float speed_vector_angle = math.atan2(speed_vector_1[1], speed_vector_1[0])

        cdef float angle_delta = centre_to_centre_vector_angle - speed_vector_angle

        cdef float torque_creation_factor = math.sin(angle_delta)

        cdef float circle_r_1 = abs_circle_shape_1[3]
        cdef float circle_r_2 = abs_circle_shape_2[3]

        cdef float v_r_1 = circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VR]
        cdef float rot_friction_1 = circle_physical_mover_1[IDX_MOVERS_PHYSICAL_ROT_FRICTION]
        cdef float m_1 = circle_physical_mover_1[IDX_MOVERS_PHYSICAL_MASS]

        cdef float v_r_2 = circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VR]
        cdef float rot_friction_2 = circle_physical_mover_2[IDX_MOVERS_PHYSICAL_ROT_FRICTION]
        cdef float m_2 = circle_physical_mover_2[IDX_MOVERS_PHYSICAL_MASS]

        cdef float created_v_p = torque_creation_factor * yapyg.math_2d.length(speed_vector_1)

        cdef float torque_transfer_factor = min(rot_friction_1, rot_friction_2)

        cdef float created_v_r_1 = (created_v_p / (circle_r_1))
        created_v_r_1 = ((created_v_r_1) / (CONST_2PI))
        created_v_r_1 = ((created_v_r_1) * torque_transfer_factor)
        circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VR] += created_v_r_1

        cdef float created_v_r_2 = (created_v_p / (circle_r_2))
        created_v_r_2 = ((created_v_r_2) / (CONST_2PI))
        created_v_r_2 = ((created_v_r_2) * torque_transfer_factor)
        circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VR] += created_v_r_2

        # ellastic collision
        cdef tuple unit_vector_1_to_2 = yapyg.math_2d.unit_vector(abs_pos_1, abs_pos_2)
        cdef float new_vx1
        cdef float new_vx2
        cdef float new_vy1
        cdef float new_vy2
        new_vx1, new_vy1, new_vx2, new_vy2 = reflect_speeds(
                unit_vector_1_to_2,
                speed_vector_1,
                speed_vector_2,
                circle_physical_mover_1[IDX_MOVERS_PHYSICAL_MASS],
                circle_physical_mover_2[IDX_MOVERS_PHYSICAL_MASS])

        cdef float inelasticity_1
        inelasticity_1 = circle_physical_mover_1[IDX_MOVERS_PHYSICAL_INELASTICITY]
        circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VX] = ((new_vx1) * (inelasticity_1))
        circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VY] = ((new_vy1) * (inelasticity_1))

        cdef float inelasticity_2
        inelasticity_2 = circle_physical_mover_2[IDX_MOVERS_PHYSICAL_INELASTICITY]
        circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VX] = ((new_vx2) * (inelasticity_2))
        circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VY] = ((new_vy2) * (inelasticity_2))

        # torque tranmission
        v_r_1 = circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VR]
        v_r_2 = circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VR]

        cdef float v_p_1 = ((v_r_1) * (circle_r_1))
        v_p_1 = ((v_p_1) * (CONST_2PI))

        cdef float v_p_2 = ((v_r_2) * (circle_r_2))
        v_p_2 = ((v_p_2) * (CONST_2PI))

        cdef float delta_v = v_p_1 + v_p_2

        cdef float mass_factor_1 = ((m_2) / (m_1 + m_2))
        cdef float mass_factor_2 = ((m_1) / (m_1 + m_2))

        cdef float torque_transfer_factor_1 = (torque_transfer_factor * (mass_factor_1))
        cdef float torque_transfer_factor_2 = (torque_transfer_factor * (mass_factor_2))

        v_p_1 = v_p_1 - ((torque_transfer_factor_1) * delta_v)
        v_p_2 = v_p_2 - ((torque_transfer_factor_2) * delta_v)

        v_r_1 = ((v_p_1) / (circle_r_1))
        v_r_1 = ((v_r_1) / (CONST_2PI))

        v_r_2 = ((v_p_2) / (circle_r_2))
        v_r_2 = ((v_r_2) / (CONST_2PI))

        circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VR] = v_r_1
        circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VR] = v_r_2

cdef c_rectangle_rectangle_collision(list state,
                str rectangle_entity_name_1,
                str rectangle_entity_name_2,
                tuple abs_rectangle_shape_1,
                tuple abs_rectangle_shape_2,
                list rectangle_physical_mover_1,
                list rectangle_physical_mover_2,
                list contact_points):
        """
        TODO
        """
        yapyg.entities.undo_last_move(state, rectangle_entity_name_1)

        cdef tuple abs_pos_1 = (abs_rectangle_shape_1[1], abs_rectangle_shape_1[2])
        cdef float v_r_1 = rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_VR]
        cdef float rot_friction_1 = rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_ROT_FRICTION]
        cdef float m_1 = rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_MASS]
        cdef tuple speed_vector_1 = (rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_VX], rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_VY])
        cdef float inelasticity_1 = rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_INELASTICITY]

        cdef tuple abs_pos_2 = (abs_rectangle_shape_2[1], abs_rectangle_shape_2[2])
        cdef float v_r_2 = 0
        cdef float rot_friction_2 = 1
        cdef float m_2 = -1
        cdef tuple speed_vector_2 = (0, 0)
        cdef float inelasticity_2

        cdef float rect_rot_2 = abs_rectangle_shape_2[5]

        cdef tuple rectangle_center_1 = (abs_rectangle_shape_1[1] + ((abs_rectangle_shape_1[3]) / 2.0),
                abs_rectangle_shape_1[2] + ((abs_rectangle_shape_1[4]) / 2.0))

        cdef tuple rectangle_center_2 = (abs_rectangle_shape_2[1] + ((abs_rectangle_shape_2[3]) / 2.0),
                abs_rectangle_shape_2[2] + ((abs_rectangle_shape_2[4]) / 2.0))

        cdef tuple contact_point
        cdef tuple contact_sum_vector

        cdef tuple rotated_point
        cdef float contact_x
        cdef float contact_y
        cdef tuple rect_move_vector
        cdef float rect_x_1
        cdef float rect_y_1
        cdef float rect_x_2
        cdef float rect_y_2
        cdef float rect_w_2
        cdef float rect_h_2
        cdef float rect_left_2
        cdef float rect_right_2
        cdef float rect_top_2
        cdef float rect_bottom_2

        cdef tuple rotation_vector = (0, -1)
        cdef tuple vector_center_to_contact
        # cdef tuple max_positive_torque_vector
        # cdef tuple rotated_vector
        cdef float resulting_torque
        cdef float torque_factor = 0.25

        if rectangle_physical_mover_2:
                print "TODO: 2 physics rectangles collision"
        else:
                # print "physics rectangle 1 with static rectangle collision 2"
                contact_sum_vector = (0, 0)
                resulting_torque = 0
                for contact_point in contact_points:
                        contact_sum_vector = yapyg.math_2d.vector_sum(contact_sum_vector,
                                yapyg.math_2d.vector_diff(contact_point, rectangle_center_1))
                        vector_center_to_contact = yapyg.math_2d.vector_diff(contact_point, rectangle_center_1)
                        rotated_vector = yapyg.math_2d.complex_multiply(rotation_vector, vector_center_to_contact)
                        resulting_torque += yapyg.math_2d.dot_product(rotated_vector, speed_vector_1)

                resulting_torque = (resulting_torque * torque_factor)
                # Seems to fix rectangles getting stuck sometimes
                if resulting_torque != rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_VR]:
                        rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_VR] = resulting_torque
                else:
                        rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_VR] = 0

                contact_sum_vector = (contact_sum_vector[0] + rectangle_center_1[0], contact_sum_vector[1] + rectangle_center_1[1])
                contact_x,contact_y = contact_sum_vector

                # rotate coordinate system so that static rectangle 2 is not rotated
                rect_move_vector = speed_vector_1

                rect_x_1 = rectangle_center_1[0]
                rect_y_1 = rectangle_center_1[1]

                rect_x_2 = rectangle_center_2[0]
                rect_y_2 = rectangle_center_2[1]
                rect_w_2 = ((abs_rectangle_shape_2[3]) / 2.0)
                rect_h_2 = ((abs_rectangle_shape_2[4]) / 2.0)

                rect_left_2 = rect_x_2 - rect_w_2
                rect_right_2 = rect_x_2 + rect_w_2
                rect_top_2 = rect_y_2 + rect_h_2
                rect_bottom_2 = rect_y_2 - rect_h_2

                if rect_rot_2 != 0:
                        rotated_point = yapyg.math_2d.rotated_point(rectangle_center_2, contact_sum_vector, -rect_rot_2)
                        contact_x,contact_y = rotated_point

                        rect_move_vector = yapyg.math_2d.rotated_point((0, 0), rect_move_vector, -rect_rot_2)

                        rotated_point = yapyg.math_2d.rotated_point(rectangle_center_2, rectangle_center_1, -rect_rot_2)
                        rect_x_1,rect_y_1 = rotated_point

                if contact_x < rect_x_2:
                        if contact_y < rect_y_2:
                                # lower left
                                if rect_x_1 < rect_left_2:
                                        rect_move_vector = (-rect_move_vector[0], rect_move_vector[1])
                                if rect_y_1 < rect_bottom_2:
                                        rect_move_vector = (rect_move_vector[0], -rect_move_vector[1])
                        else:
                                # upper left
                                if rect_x_1 < rect_left_2:
                                        rect_move_vector = (-rect_move_vector[0], rect_move_vector[1])
                                if rect_y_1 > rect_top_2:
                                        rect_move_vector = (rect_move_vector[0], -rect_move_vector[1])
                else:
                        if contact_y < rect_y_2:
                                # lower right
                                if rect_x_1 > rect_right_2:
                                        rect_move_vector = (-rect_move_vector[0], rect_move_vector[1])
                                if rect_y_1 < rect_bottom_2:
                                        rect_move_vector = (rect_move_vector[0], -rect_move_vector[1])
                        else:
                                # upper right
                                if rect_x_1 > rect_right_2:
                                        rect_move_vector = (-rect_move_vector[0], rect_move_vector[1])
                                if rect_y_1 > rect_top_2:
                                        rect_move_vector = (rect_move_vector[0], -rect_move_vector[1])

                # rotate back to original coordinate system
                rect_move_vector = yapyg.math_2d.rotated_point((0, 0), rect_move_vector, rect_rot_2)
                rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_VX] = rect_move_vector[0]
                rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_VY] = rect_move_vector[1]

cpdef collision_handler(list state,
                str entity_name_1,
                str entity_name_2,
                list collision_def_1,
                list collision_def_2,
                tuple absolute_shape_1,
                tuple absolute_shape_2,
                list contact_points,
                ):
        """
        TODO
        """
        # print "physical collision_handler", entity_name_1, entity_name_2

        cdef list entity_mover_1
        cdef list entity_mover_2
        entity_mover_1 = yapyg.movers.get_active(state, entity_name_1)
        entity_mover_2 = yapyg.movers.get_active(state, entity_name_2)

        cdef list physics_mover_1
        cdef list physics_mover_2
        physics_mover_1 = None
        physics_mover_2 = None
        if (entity_mover_1 and entity_mover_1[0] == PHYSICS_MOVER_NAME):
                physics_mover_1 = entity_mover_1
        if (entity_mover_2 and entity_mover_2[0] == PHYSICS_MOVER_NAME):
                physics_mover_2 = entity_mover_2

        if (physics_mover_1 or physics_mover_2):
                if absolute_shape_1[0] == "rectangle":
                        if absolute_shape_2[0] == "rectangle":
                                c_rectangle_rectangle_collision(state, entity_name_1, entity_name_2,
                                        absolute_shape_1, absolute_shape_2,
                                        physics_mover_1, physics_mover_2,
                                        contact_points)
                        elif absolute_shape_2[0] == "circle":
                                c_rectangle_circle_collision(state, entity_name_1, entity_name_2,
                                        absolute_shape_1, absolute_shape_2,
                                        physics_mover_1, physics_mover_2)
                elif absolute_shape_1[0] == "circle":
                        if absolute_shape_2[0] == "rectangle":
                                c_rectangle_circle_collision(state, entity_name_2, entity_name_1,
                                        absolute_shape_2, absolute_shape_1,
                                        physics_mover_2, physics_mover_1)
                        elif absolute_shape_2[0] == "circle":
                                c_circle_circle_collision(state, entity_name_1, entity_name_2,
                                        absolute_shape_1, absolute_shape_2,
                                        physics_mover_1, physics_mover_2)

        if entity_mover_2 and entity_mover_2[0] != PHYSICS_MOVER_NAME:
                if (entity_mover_2[yapyg.movers.IDX_MOVER_COLLISION_HANDLER]):
                        (entity_mover_2[yapyg.movers.IDX_MOVER_COLLISION_HANDLER])(state,
                        entity_name_1,
                        entity_name_2,
                        collision_def_1,
                        collision_def_2,
                        absolute_shape_1,
                        absolute_shape_2,
                        contact_points)

cpdef tuple elastic_collision(float v_1, float v_2, float m_1, float m_2):
        """
        negative mass means infinite mass
        """
        cdef float mass_sum
        cdef float diff_1
        cdef float new_v_1
        cdef float new_v_2
        if m_1 < 0:
                return (v_1, -v_2)
        elif m_2 < 0:
                return (-v_1, v_2)
        else:
                mass_sum = m_1 + m_2
                diff_1 = m_1 - m_2
                new_v_1 =  ((v_1 * diff_1) + (2.0 * m_2 * v_2)) / mass_sum
                new_v_2 = ((v_2 * -diff_1) + (2.0 * m_1 * v_1)) / mass_sum
                return (new_v_1, new_v_2)

cpdef tuple reflect_speeds(tuple unit_vector, tuple v1_vector, tuple v2_vector, float m_1, float m_2):
        """
        TODO
        """
        cdef float v1_eff = yapyg.math_2d.dot_product(unit_vector, v1_vector)
        cdef float v2_eff = yapyg.math_2d.dot_product(unit_vector, v2_vector)

        cdef tuple v1_eff_vector = yapyg.math_2d.vector_product(unit_vector, v1_eff)
        cdef tuple v2_eff_vector = yapyg.math_2d.vector_product(unit_vector, v2_eff)

        cdef tuple v1_tangent_vector = yapyg.math_2d.vector_diff(v1_vector, v1_eff_vector)
        cdef tuple v2_tangent_vector = yapyg.math_2d.vector_diff(v2_vector, v2_eff_vector)

        cdef float new_v1_eff
        cdef float new_v2_eff
        new_v1_eff, new_v2_eff = elastic_collision(v1_eff, v2_eff, m_1, m_2)

        cdef tuple new_v1_eff_vector = yapyg.math_2d.vector_product(unit_vector, new_v1_eff)
        cdef tuple new_v2_eff_vector = yapyg.math_2d.vector_product(unit_vector, new_v2_eff)

        cdef tuple new_v1_vector = yapyg.math_2d.vector_sum(new_v1_eff_vector, v1_tangent_vector)
        cdef tuple new_v2_vector = yapyg.math_2d.vector_sum(new_v2_eff_vector, v2_tangent_vector)

        return (new_v1_vector[0], new_v1_vector[1],
                new_v2_vector[0], new_v2_vector[1])
