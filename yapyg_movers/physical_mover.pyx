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
Simulate physical movement
"""

from libc.math cimport atan2, sin, cos

import yapyg
cimport yapyg.math_2d
cimport yapyg.movers
cimport yapyg.entities
cimport yapyg.collisions

cdef int IDX_MOVERS_PHYSICAL_MASS = yapyg.movers.IDX_MOVER_FIRST_PARAMETER
cdef int IDX_MOVERS_PHYSICAL_VX = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 1
cdef int IDX_MOVERS_PHYSICAL_VY = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 2
cdef int IDX_MOVERS_PHYSICAL_AX = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 3
cdef int IDX_MOVERS_PHYSICAL_AY = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 4
cdef int IDX_MOVERS_PHYSICAL_FRICTION = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 5
cdef int IDX_MOVERS_PHYSICAL_INELASTICITY = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 6
cdef int IDX_MOVERS_PHYSICAL_VR = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 7
cdef int IDX_MOVERS_PHYSICAL_ROT_FRICTION = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 8
cdef int IDX_MOVERS_PHYSICAL_ROT_DECAY = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 9
cdef int IDX_MOVERS_PHYSICAL_STICKYNESS = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 10
cdef int IDX_MOVERS_PHYSICAL_NO_ROTATE = yapyg.movers.IDX_MOVER_FIRST_PARAMETER + 11
IDX_MOVERS_PHYSICAL_LAST_PARAMETER = IDX_MOVERS_PHYSICAL_NO_ROTATE

cpdef str PHYSICS_MOVER_NAME = "physics"

cdef float CONST_2PI = 2 * yapyg.math_2d.CONST_PI
cdef float CONST_TORQUE_DAMPENING = 0.5

# sys.float_info.max leads to overflow, just choose a very high number instead
cdef float CONST_INF_MASS = 999999999.9

cpdef tuple get_acceleration(list mover):
        return (mover[IDX_MOVERS_PHYSICAL_AX], mover[IDX_MOVERS_PHYSICAL_AY])

cpdef set_acceleration(list mover, tuple new_acc):
        mover[IDX_MOVERS_PHYSICAL_AX] = new_acc[0]
        mover[IDX_MOVERS_PHYSICAL_AY] = new_acc[1]

cpdef tuple get_velocity(list mover):
        return (mover[IDX_MOVERS_PHYSICAL_VX],
                mover[IDX_MOVERS_PHYSICAL_VY],
                mover[IDX_MOVERS_PHYSICAL_VR]
                )

cpdef set_velocity(list mover, tuple new_vel):
        mover[IDX_MOVERS_PHYSICAL_VX] = new_vel[0]
        mover[IDX_MOVERS_PHYSICAL_VY] = new_vel[1]
        mover[IDX_MOVERS_PHYSICAL_VR] = new_vel[2]

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
          int do_replace=False
          ):
        """
        vr > 0: counter-clockwise
        """
        yapyg.movers.add(state,
                entity_name,
                create(entity_name,
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

cpdef list create(str entity_name,
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
                False
                ]

cpdef run(list state, str entity_name, list mover, float frame_time_delta, list movers_to_delete):
        """
        TODO
        """
        cdef tuple accel_vector = (mover[IDX_MOVERS_PHYSICAL_AX], mover[IDX_MOVERS_PHYSICAL_AY])
        cdef tuple velocity_vector = (mover[IDX_MOVERS_PHYSICAL_VX], mover[IDX_MOVERS_PHYSICAL_VY])
        cdef float v_r = mover[IDX_MOVERS_PHYSICAL_VR]

        cdef float delta_time
        cdef tuple delta_dist_vector
        cdef tuple delta_velocity_vector
        cdef float delta_rot
        if not (accel_vector == (0.0, 0.0) and velocity_vector == (0.0, 0.0) and v_r == 0.0):
                delta_time = frame_time_delta / 1000.0

                # s = 0.5 a t^2
                delta_dist_vector = yapyg.math_2d.vector_mul(accel_vector, 0.5 * delta_time * delta_time / 1000.0)

                # s = v t
                delta_dist_vector = yapyg.math_2d.vector_add(delta_dist_vector, yapyg.math_2d.vector_mul(velocity_vector, delta_time))

                # v = a t
                delta_velocity_vector = yapyg.math_2d.vector_mul(accel_vector, delta_time)

                # translation friction
                velocity_vector = yapyg.math_2d.vector_add(velocity_vector, delta_velocity_vector)
                velocity_vector = yapyg.math_2d.vector_mul(velocity_vector, mover[IDX_MOVERS_PHYSICAL_FRICTION])

                # rotation amount and velocity decay
                delta_rot = 0.0
                if not mover[IDX_MOVERS_PHYSICAL_NO_ROTATE]:
                        delta_rot = v_r * frame_time_delta
                        mover[IDX_MOVERS_PHYSICAL_VR] = v_r * mover[IDX_MOVERS_PHYSICAL_ROT_DECAY]
                else:
                        mover[IDX_MOVERS_PHYSICAL_NO_ROTATE] = False

                if abs(mover[IDX_MOVERS_PHYSICAL_VR]) < 0.001:
                        mover[IDX_MOVERS_PHYSICAL_VR] = 0.0

                if yapyg.math_2d.length(velocity_vector) < mover[IDX_MOVERS_PHYSICAL_STICKYNESS]:
                        delta_dist_vector = (0, 0)
                        delta_rot = 0
                        velocity_vector = (0.0, 0.0)

                mover[IDX_MOVERS_PHYSICAL_VX] = velocity_vector[0]
                mover[IDX_MOVERS_PHYSICAL_VY] = velocity_vector[1]

                yapyg.entities.add_pos(state, entity_name, delta_dist_vector[0], delta_dist_vector[1], delta_rot)

        cdef tuple collision_result = yapyg.collisions.run(state, entity_name)
        if collision_result:
                collision_handler(*collision_result)

cdef tuple compute_circle_torque(float v_r, float v_x, float rot_friction, float circle_r, int clockw_right):
        """
        Get new revolution velocity and translation velocity after circle hits a surface.
        Depending on friction more or less of the revolution v is transformed into trans v
        and vice versa. The velocities will attempt to be equal (leading to rolling).
        Needs indication if clockwise revolution means translation to the right.
        Returns tuple of new revolution v and translation v.
        """
        cdef float circle_circumference = CONST_2PI * circle_r
        cdef float v_p = v_r * circle_circumference

        if not clockw_right:
                v_p = -v_p

        # Difference between the two surfaces
        cdef float delta = (v_p + v_x) * rot_friction

        v_x -= delta
        v_p -= delta

        if not clockw_right:
                v_p = -v_p

        v_r = v_p / circle_circumference

        return (v_r, v_x)

cdef rectangle_circle_collision(list state,
                str rectangle_entity_name,
                str circle_entity_name,
                tuple abs_rectangle_shape,
                tuple abs_circle_shape,
                list rectangle_physical_mover,
                list circle_physical_mover,
                list contact_points):
        """
        TODO
        """
        cdef float circle_x = abs_circle_shape[1]
        cdef float circle_y = abs_circle_shape[2]
        cdef float circle_r = abs_circle_shape[3]
        cdef tuple circle_centre_vector = (circle_x, circle_y)

        cdef tuple contact_point_vector = contact_points[0]

        cdef float rect_x = abs_rectangle_shape[1]
        cdef float rect_y = abs_rectangle_shape[2]
        cdef float rect_w = abs_rectangle_shape[3]
        cdef float rect_h = abs_rectangle_shape[4]
        cdef float rect_r = abs_rectangle_shape[5]

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

        # If two physical objects, compute relative velocities
        cdef tuple circle_velocity_vector
        cdef tuple old_circle_velocity_vector
        if circle_physical_mover:
                yapyg.entities.undo_last_move(state, circle_entity_name)
                circle_velocity_vector = (circle_physical_mover[IDX_MOVERS_PHYSICAL_VX], circle_physical_mover[IDX_MOVERS_PHYSICAL_VY])
                old_circle_velocity_vector = (circle_physical_mover[IDX_MOVERS_PHYSICAL_VX], circle_physical_mover[IDX_MOVERS_PHYSICAL_VY])

        cdef tuple rectangle_velocity_vector
        cdef tuple old_rectangle_velocity_vector
        if rectangle_physical_mover:
                yapyg.entities.undo_last_move(state, rectangle_entity_name)
                rectangle_velocity_vector = (rectangle_physical_mover[IDX_MOVERS_PHYSICAL_VX], rectangle_physical_mover[IDX_MOVERS_PHYSICAL_VY])
                old_rectangle_velocity_vector = (rectangle_physical_mover[IDX_MOVERS_PHYSICAL_VX], rectangle_physical_mover[IDX_MOVERS_PHYSICAL_VY])

        if circle_physical_mover and rectangle_physical_mover:
                circle_velocity_vector = yapyg.math_2d.vector_sub(circle_velocity_vector, old_rectangle_velocity_vector)
                rectangle_velocity_vector = yapyg.math_2d.vector_sub(rectangle_velocity_vector, old_circle_velocity_vector)

        if circle_physical_mover:
                inelasticity = circle_physical_mover[IDX_MOVERS_PHYSICAL_INELASTICITY]

                # rotate coordinate system so that rectangle is not rotated
                if rect_r != 0:
                        rotated_circle = yapyg.math_2d.rotated_point(
                                (rect_x + (rect_w / 2.0), rect_y + (rect_h / 2.0)),
                                (circle_x, circle_y),
                                -rect_r)
                        circle_x = rotated_circle[0]
                        circle_y = rotated_circle[1]
                        circle_velocity_vector = yapyg.math_2d.rotated_point((0, 0), circle_velocity_vector, -rect_r)

                v_r = circle_physical_mover[IDX_MOVERS_PHYSICAL_VR]
                v_x = circle_velocity_vector[0]
                v_y = circle_velocity_vector[1]
                rot_friction = circle_physical_mover[IDX_MOVERS_PHYSICAL_ROT_FRICTION]

                if circle_y <= rect_y or circle_y >= rect_y + rect_h:
                        # circle centre below or above rectangle
                        if circle_x > rect_x and circle_x < rect_x + rect_w:
                                # lower/upper quadrant
                                if circle_y <= rect_y:
                                        # lower quadrant
                                        v_r, v_x = compute_circle_torque(v_r, v_x, rot_friction, circle_r, False)
                                        circle_velocity_vector = (v_x, circle_velocity_vector[1])
                                        circle_physical_mover[IDX_MOVERS_PHYSICAL_VR] = v_r
                                        circle_velocity_vector = (circle_velocity_vector[0], -abs(circle_velocity_vector[1]) * inelasticity)
                                else:
                                        # upper quadrant
                                        v_r, v_x = compute_circle_torque(v_r, v_x, rot_friction, circle_r, True)
                                        circle_velocity_vector = (v_x, circle_velocity_vector[1])
                                        circle_physical_mover[IDX_MOVERS_PHYSICAL_VR] = v_r
                                        circle_velocity_vector = (circle_velocity_vector[0], abs(circle_velocity_vector[1]) * inelasticity)
                        else:
                                # lower/upper left/right quadrant
                                v_total = yapyg.math_2d.length(circle_velocity_vector)
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
                                angle = atan2(angle_dy, angle_dx)

                                new_vy = sin(angle) * v_total
                                new_vx = cos(angle) * v_total
                                circle_velocity_vector = (new_vx * inelasticity, new_vy * inelasticity)
                else:
                        # circle same height as rectangle
                        if circle_x < rect_x:
                                # left quadrant
                                v_r, v_y = compute_circle_torque(v_r, v_y, rot_friction, circle_r, True)
                                circle_velocity_vector = (circle_velocity_vector[0], v_y)
                                circle_physical_mover[IDX_MOVERS_PHYSICAL_VR] = v_r
                                circle_velocity_vector = (-abs(circle_velocity_vector[0]) * inelasticity, circle_velocity_vector[1])
                        elif circle_x > rect_x + rect_w:
                                # right quadrant
                                v_r, v_y = compute_circle_torque(v_r, v_y, rot_friction, circle_r, False)
                                circle_velocity_vector = (circle_velocity_vector[0], v_y)
                                circle_physical_mover[IDX_MOVERS_PHYSICAL_VR] = v_r
                                circle_velocity_vector = (abs(circle_velocity_vector[0]) * inelasticity, circle_velocity_vector[1])
                        else:
                                # inside rectangle
                                # print "WARNING: physical mover circle inside a rectangle"
                                circle_velocity_vector = (-circle_velocity_vector[0], -circle_velocity_vector[1])

                # rotate back to original coordinate system
                circle_velocity_vector = yapyg.math_2d.rotated_point((0, 0), circle_velocity_vector, rect_r)
                circle_physical_mover[IDX_MOVERS_PHYSICAL_VX] = circle_velocity_vector[0]
                circle_physical_mover[IDX_MOVERS_PHYSICAL_VY] = circle_velocity_vector[1]

        cdef tuple contact_to_circle_unit_vector
        cdef tuple parallel_rectangle_velocity_vector
        cdef float parallel_velocity_component
        cdef tuple new_rectangle_velocity_vector
        cdef tuple rel_contact_point_vector
        cdef float resulting_torque
        if rectangle_physical_mover:
                rectangle_physical_mover[IDX_MOVERS_PHYSICAL_NO_ROTATE] = True
                contact_to_circle_unit_vector = yapyg.math_2d.get_direction_unit_vector(contact_point_vector, circle_centre_vector)
                parallel_velocity_component = yapyg.math_2d.dot_product(contact_to_circle_unit_vector, rectangle_velocity_vector)
                parallel_rectangle_velocity_vector = yapyg.math_2d.vector_mul(contact_to_circle_unit_vector, parallel_velocity_component)
                new_rectangle_velocity_vector = yapyg.math_2d.vector_sub(
                        rectangle_velocity_vector,
                        yapyg.math_2d.vector_mul(parallel_rectangle_velocity_vector, 2.0)
                        )
                rel_contact_point_vector, resulting_torque = get_post_rectangle_collision_torque(
                        contact_points,
                        get_abs_rectangle_center(abs_rectangle_shape),
                        rectangle_velocity_vector
                        )
                rectangle_physical_mover[IDX_MOVERS_PHYSICAL_VX] = new_rectangle_velocity_vector[0]
                rectangle_physical_mover[IDX_MOVERS_PHYSICAL_VY] = new_rectangle_velocity_vector[1]
                rectangle_physical_mover[IDX_MOVERS_PHYSICAL_VR] = resulting_torque * 1.0 * CONST_TORQUE_DAMPENING

        cdef float m_rectangle
        if rectangle_physical_mover:
                m_rectangle = rectangle_physical_mover[IDX_MOVERS_PHYSICAL_MASS]
        else:
                m_rectangle = CONST_INF_MASS

        cdef float m_circle
        if circle_physical_mover:
                m_circle = circle_physical_mover[IDX_MOVERS_PHYSICAL_MASS]
        else:
                m_circle = CONST_INF_MASS

        cdef float mass_factor_rectangle = m_circle / (m_rectangle + m_circle)
        cdef float mass_factor_circle = m_rectangle / (m_rectangle + m_circle)

        if rectangle_physical_mover:
                rectangle_physical_mover[IDX_MOVERS_PHYSICAL_VX] *= mass_factor_rectangle
                rectangle_physical_mover[IDX_MOVERS_PHYSICAL_VY] *= mass_factor_rectangle
                rectangle_physical_mover[IDX_MOVERS_PHYSICAL_VR] *= mass_factor_rectangle

        if circle_physical_mover:
                circle_physical_mover[IDX_MOVERS_PHYSICAL_VX] *= mass_factor_circle
                circle_physical_mover[IDX_MOVERS_PHYSICAL_VY] *= mass_factor_circle
                circle_physical_mover[IDX_MOVERS_PHYSICAL_VR] *= mass_factor_circle

cdef void circle_circle_collision(
                list state,
                str circle_entity_name_1,
                str circle_entity_name_2,
                tuple abs_circle_shape_1,
                tuple abs_circle_shape_2,
                list circle_physical_mover_1,
                list circle_physical_mover_2
                ):
        """
        TODO
        """
        yapyg.entities.undo_last_move(state, circle_entity_name_1)

        # torque creation
        cdef tuple abs_pos_1 = (abs_circle_shape_1[1], abs_circle_shape_1[2])
        cdef tuple abs_pos_2 = (abs_circle_shape_2[1], abs_circle_shape_2[2])
        cdef tuple velocity_vector_1 = (circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VX], circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VY])
        cdef tuple centre_to_centre_vector = yapyg.math_2d.vector_sub(abs_pos_2, abs_pos_1)
        cdef float centre_to_centre_vector_angle = atan2(centre_to_centre_vector[1], centre_to_centre_vector[0])
        cdef float velocity_vector_angle = atan2(velocity_vector_1[1], velocity_vector_1[0])
        cdef float angle_delta = centre_to_centre_vector_angle - velocity_vector_angle
        cdef float torque_creation_factor = sin(angle_delta)
        cdef float created_v_p = torque_creation_factor * yapyg.math_2d.length(velocity_vector_1)

        cdef float rot_friction_1 = circle_physical_mover_1[IDX_MOVERS_PHYSICAL_ROT_FRICTION]
        cdef float rot_friction_2
        if circle_physical_mover_2:
                rot_friction_2 = circle_physical_mover_2[IDX_MOVERS_PHYSICAL_ROT_FRICTION]
        else:
                rot_friction_2 = 0.0
        cdef float torque_transfer_factor = min(rot_friction_1, rot_friction_2)

        cdef float circle_r_1 = abs_circle_shape_1[3]
        cdef float created_v_r_1 = created_v_p / circle_r_1
        created_v_r_1 = created_v_r_1 / CONST_2PI
        created_v_r_1 = created_v_r_1 * torque_transfer_factor
        circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VR] += created_v_r_1

        cdef float circle_r_2 = abs_circle_shape_2[3]
        cdef float created_v_r_2
        if circle_physical_mover_2:
                created_v_r_2 = created_v_p / circle_r_2
                created_v_r_2 = created_v_r_2 / CONST_2PI
                created_v_r_2 = created_v_r_2 * torque_transfer_factor
                circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VR] += created_v_r_2

        # ellastic collision
        cdef float m_1 = circle_physical_mover_1[IDX_MOVERS_PHYSICAL_MASS]
        cdef float m_2
        cdef tuple velocity_vector_2
        if circle_physical_mover_2:
                velocity_vector_2 = (circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VX], circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VY])
                m_2 = circle_physical_mover_2[IDX_MOVERS_PHYSICAL_MASS]
        else:
                velocity_vector_2 = (0, 0)
                m_2 = CONST_INF_MASS
        cdef tuple unit_vector_1_to_2 = yapyg.math_2d.get_direction_unit_vector(abs_pos_1, abs_pos_2)
        cdef float new_vx1
        cdef float new_vx2
        cdef float new_vy1
        cdef float new_vy2
        new_vx1, new_vy1, new_vx2, new_vy2 = reflect_velocities(
                unit_vector_1_to_2,
                velocity_vector_1,
                velocity_vector_2,
                m_1,
                m_2)

        cdef float inelasticity_1 = circle_physical_mover_1[IDX_MOVERS_PHYSICAL_INELASTICITY]
        circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VX] = new_vx1 * inelasticity_1
        circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VY] = new_vy1 * inelasticity_1

        cdef float inelasticity_2
        if circle_physical_mover_2:
                inelasticity_2 = circle_physical_mover_2[IDX_MOVERS_PHYSICAL_INELASTICITY]
                circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VX] = new_vx2 * inelasticity_2
                circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VY] = new_vy2 * inelasticity_2

        # torque tranmission
        cdef float v_r_1 = circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VR]
        cdef float v_r_2
        if circle_physical_mover_2:
                v_r_2 = circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VR]
        else:
                v_r_2 = 0.0
        cdef float v_p_1 = v_r_1 * circle_r_1 * CONST_2PI
        cdef float v_p_2 = v_r_2 * circle_r_2 * CONST_2PI

        cdef float delta_v = v_p_1 + v_p_2
        cdef float mass_factor_1 = m_2 / (m_1 + m_2)
        cdef float torque_transfer_factor_1 = torque_transfer_factor * mass_factor_1
        v_p_1 -= torque_transfer_factor_1 * delta_v
        v_r_1 = (v_p_1 / circle_r_1) / CONST_2PI
        circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VR] = v_r_1

        cdef float mass_factor_2
        cdef float torque_transfer_factor_2
        if circle_physical_mover_2:
                mass_factor_2 = m_1 / (m_1 + m_2)
                torque_transfer_factor_2 = torque_transfer_factor * mass_factor_2
                v_p_2 -= torque_transfer_factor_2 * delta_v
                v_r_2 = (v_p_2 / circle_r_2) / CONST_2PI
                circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VR] = v_r_2

cdef tuple get_post_rectangle_collision_torque(
                list contact_points,
                tuple rectangle_centre,
                tuple velocity_vector
                ):
        """
        Compute a single representative contact point between the rectangles,
        and the total torque applied on the rectangle by collision with a certain velocity.
        * Contact points are points of the rectangle that are
          inside the bounds of the other rectangle.
        """
        cdef tuple contact_sum_vector = (0.0, 0.0)
        cdef float resulting_torque = 0.0
        cdef tuple contact_point_vector
        for contact_point_vector in contact_points:
                contact_sum_vector = yapyg.math_2d.vector_add(
                        contact_sum_vector,
                        yapyg.math_2d.vector_sub(contact_point_vector, rectangle_centre)
                        )
                resulting_torque += yapyg.math_2d.dot_product(
                        yapyg.math_2d.complex_mul(
                                (0.0, -1.0),
                                yapyg.math_2d.vector_sub(contact_point_vector, rectangle_centre)
                                ),
                        velocity_vector)
        return (yapyg.math_2d.vector_mul(contact_sum_vector, 1.0 / len(contact_points)), resulting_torque)

cdef tuple get_abs_rectangle_center(tuple abs_rectangle_shape):
        """
        TODO
        """
        return (
                abs_rectangle_shape[1] + (abs_rectangle_shape[3] / 2.0),
                abs_rectangle_shape[2] + (abs_rectangle_shape[4] / 2.0)
                )

cdef tuple get_rect_rect_central_collision_velocity(tuple velocity_vector,
                                                    tuple rel_contact_point_vector,
                                                    float mass_factor):
        return yapyg.math_2d.vector_mul(
                                        yapyg.math_2d.get_unit_vector(rel_contact_point_vector),
                                        -1.0 * yapyg.math_2d.length(velocity_vector) * mass_factor
                                        )

cdef tuple get_rect_rect_reflect_collision_velocity(tuple rectangle_center_A,
                                                    tuple rectangle_center_B,
                                                    tuple abs_rectangle_shape_B,
                                                    tuple rel_contact_point_vector_A,
                                                    tuple velocity_vector_A,
                                                    float mass_factor_A
                                                    ):
        cdef tuple contact_point_vector = yapyg.math_2d.vector_add(rectangle_center_A, rel_contact_point_vector_A)
        cdef tuple rect_B_to_contact_vector = yapyg.math_2d.vector_sub(contact_point_vector, rectangle_center_B)
        cdef float rect_B_contact_angle = yapyg.math_2d.get_angle((0.0, 0.0), rect_B_to_contact_vector)
        cdef float rect_B_angle = abs_rectangle_shape_B[5]
        cdef float rect_B_diag_angle = yapyg.math_2d.get_angle((0.0, 0.0), (abs_rectangle_shape_B[3], abs_rectangle_shape_B[4]))
        cdef float contact_angle_delta = rect_B_contact_angle - rect_B_angle
        # Adjust angle if contact point is on the left or right side of the rectangle
        #        ________
        #       |    ___/| rect_B_diag_angle
        #       |   /....|
        #       |________|
        #
        cdef int contact_on_right_side = (contact_angle_delta <= (rect_B_diag_angle - 1.0) and contact_angle_delta >= 0) or (contact_angle_delta >= (361.0 - rect_B_diag_angle) and contact_angle_delta <= 360.0)
        cdef int contact_on_left_side = (contact_angle_delta >= (181.0 - rect_B_diag_angle)) and contact_angle_delta < (179.0 + rect_B_diag_angle)
        if contact_on_left_side or contact_on_right_side:
                rect_B_angle += 90.0
        cdef tuple rect_B_unit_axis_vector = yapyg.math_2d.create_unit_vector(rect_B_angle)
        cdef tuple parallel_v
        cdef tuple perpend_v
        parallel_v,perpend_v = yapyg.math_2d.get_projection_vectors(rect_B_unit_axis_vector, velocity_vector_A)
        return yapyg.math_2d.vector_mul(yapyg.math_2d.vector_sub(velocity_vector_A, yapyg.math_2d.vector_mul(perpend_v, 2.0)), mass_factor_A)

cdef tuple get_rect_rect_post_collision_velocity(tuple rectangle_center_A,
                                                 tuple rectangle_center_B,
                                                 tuple abs_rectangle_shape_B,
                                                 tuple rel_contact_point_vector_A,
                                                 tuple velocity_vector_A,
                                                 float mass_factor_A
                                                 ):
        cdef tuple new_velocity_vector_A_central = get_rect_rect_central_collision_velocity(velocity_vector_A,
                                                                                            rel_contact_point_vector_A,
                                                                                            mass_factor_A
                                                                                            )
        cdef tuple new_velocity_vector_A_reflect = get_rect_rect_reflect_collision_velocity(rectangle_center_A,
                                                                                            rectangle_center_B,
                                                                                            abs_rectangle_shape_B,
                                                                                            rel_contact_point_vector_A,
                                                                                            velocity_vector_A,
                                                                                            mass_factor_A
                                                                                            )
        cdef float reflect_weight = 0.6
        return yapyg.math_2d.vector_add(yapyg.math_2d.vector_mul(new_velocity_vector_A_reflect, reflect_weight),
                                        yapyg.math_2d.vector_mul(new_velocity_vector_A_central, 1.0 - reflect_weight)
                                        )

cdef rectangle_rectangle_collision(list state,
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
        rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_NO_ROTATE] = True

        # Get new torque of rectangles after collision
        cdef tuple velocity_vector_1 = (rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_VX], rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_VY])
        cdef tuple old_velocity_vector_1 = (velocity_vector_1[0], velocity_vector_1[1])
        cdef tuple rectangle_center_1 = get_abs_rectangle_center(abs_rectangle_shape_1)

        # If two physical vectors, compute relative velocities
        cdef tuple velocity_vector_2
        cdef tuple old_velocity_vector_2
        if rectangle_physical_mover_2:
                velocity_vector_2 = (rectangle_physical_mover_2[IDX_MOVERS_PHYSICAL_VX], rectangle_physical_mover_2[IDX_MOVERS_PHYSICAL_VY])
                old_velocity_vector_2 = (velocity_vector_2[0], velocity_vector_2[1])
                velocity_vector_1 = yapyg.math_2d.vector_sub(velocity_vector_1, old_velocity_vector_2)
                velocity_vector_2 = yapyg.math_2d.vector_sub(velocity_vector_2, old_velocity_vector_1)
        else:
                velocity_vector_2 = (0, 0)
                old_velocity_vector_2 = (0, 0)

        cdef tuple rel_contact_point_vector_1
        cdef float resulting_torque_1
        rel_contact_point_vector_1, resulting_torque_1 = get_post_rectangle_collision_torque(contact_points, rectangle_center_1, velocity_vector_1)

        cdef tuple rectangle_center_2 = get_abs_rectangle_center(abs_rectangle_shape_2)
        cdef tuple rel_contact_point_vector_2
        cdef float resulting_torque_2
        if rectangle_physical_mover_2:
                rel_contact_point_vector_2, resulting_torque_2 = get_post_rectangle_collision_torque(contact_points, rectangle_center_2, velocity_vector_2)

        cdef float m_1 = rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_MASS]
        cdef float m_2
        if rectangle_physical_mover_2:
                m_2 = rectangle_physical_mover_2[IDX_MOVERS_PHYSICAL_MASS]
        else:
                velocity_vector_2 = (0, 0)
                m_2 = CONST_INF_MASS
        cdef float mass_factor_1 = m_2 / (m_1 + m_2)

        # TODO This wipes out any previous torque!
        rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_VR] = resulting_torque_1 * mass_factor_1 * CONST_TORQUE_DAMPENING / m_1
        cdef float mass_factor_2
        if rectangle_physical_mover_2:
                mass_factor_2 = m_1 / (m_1 + m_2)
                rectangle_physical_mover_2[IDX_MOVERS_PHYSICAL_VR] = resulting_torque_2 * mass_factor_2 * CONST_TORQUE_DAMPENING / m_2

        # Post-collision velocities
        cdef tuple new_velocity_vector_1 = get_rect_rect_post_collision_velocity(rectangle_center_1,
                                                                                 rectangle_center_2,
                                                                                 abs_rectangle_shape_2,
                                                                                 rel_contact_point_vector_1,
                                                                                 velocity_vector_1,
                                                                                 mass_factor_1
                                                                                 )
        rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_VX] = new_velocity_vector_1[0]
        rectangle_physical_mover_1[IDX_MOVERS_PHYSICAL_VY] = new_velocity_vector_1[1]

        cdef tuple new_velocity_vector_2
        if rectangle_physical_mover_2:
                new_velocity_vector_2 = get_rect_rect_post_collision_velocity(rectangle_center_2,
                                                                              rectangle_center_1,
                                                                              abs_rectangle_shape_1,
                                                                              rel_contact_point_vector_2,
                                                                              velocity_vector_2,
                                                                              mass_factor_2
                                                                              )
                rectangle_physical_mover_2[IDX_MOVERS_PHYSICAL_VX] = new_velocity_vector_2[0]
                rectangle_physical_mover_2[IDX_MOVERS_PHYSICAL_VY] = new_velocity_vector_2[1]

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
        cdef list entity_mover_1 = yapyg.movers.get_active(state, entity_name_1)
        cdef list entity_mover_2 = yapyg.movers.get_active(state, entity_name_2)

        cdef list physics_mover_2 = None
        if (entity_mover_2 and entity_mover_2[0] == PHYSICS_MOVER_NAME):
                physics_mover_2 = entity_mover_2

        if absolute_shape_1[0] == "rectangle":
                if absolute_shape_2[0] == "rectangle":
                        rectangle_rectangle_collision(state, entity_name_1, entity_name_2,
                                absolute_shape_1, absolute_shape_2,
                                entity_mover_1, physics_mover_2,
                                contact_points)
                elif absolute_shape_2[0] == "circle":
                        rectangle_circle_collision(state, entity_name_1, entity_name_2,
                                absolute_shape_1, absolute_shape_2,
                                entity_mover_1, physics_mover_2,
                                contact_points)
        elif absolute_shape_1[0] == "circle":
                if absolute_shape_2[0] == "rectangle":
                        rectangle_circle_collision(state, entity_name_2, entity_name_1,
                                absolute_shape_2, absolute_shape_1,
                                physics_mover_2, entity_mover_1,
                                contact_points)
                elif absolute_shape_2[0] == "circle":
                        circle_circle_collision(state, entity_name_1, entity_name_2,
                                absolute_shape_1, absolute_shape_2,
                                entity_mover_1, physics_mover_2)

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

cpdef tuple reflect_velocities(tuple unit_vector, tuple v1_vector, tuple v2_vector, float m_1, float m_2):
        """
        TODO
        """
        cdef float v1_eff = yapyg.math_2d.dot_product(unit_vector, v1_vector)
        cdef float v2_eff = yapyg.math_2d.dot_product(unit_vector, v2_vector)

        cdef tuple v1_eff_vector = yapyg.math_2d.vector_mul(unit_vector, v1_eff)
        cdef tuple v2_eff_vector = yapyg.math_2d.vector_mul(unit_vector, v2_eff)

        cdef tuple v1_tangent_vector = yapyg.math_2d.vector_sub(v1_vector, v1_eff_vector)
        cdef tuple v2_tangent_vector = yapyg.math_2d.vector_sub(v2_vector, v2_eff_vector)

        cdef float new_v1_eff
        cdef float new_v2_eff
        new_v1_eff, new_v2_eff = elastic_collision(v1_eff, v2_eff, m_1, m_2)

        cdef tuple new_v1_eff_vector = yapyg.math_2d.vector_mul(unit_vector, new_v1_eff)
        cdef tuple new_v2_eff_vector = yapyg.math_2d.vector_mul(unit_vector, new_v2_eff)

        cdef tuple new_v1_vector = yapyg.math_2d.vector_add(new_v1_eff_vector, v1_tangent_vector)
        cdef tuple new_v2_vector = yapyg.math_2d.vector_add(new_v2_eff_vector, v2_tangent_vector)

        return (new_v1_vector[0], new_v1_vector[1],
                new_v2_vector[0], new_v2_vector[1])
