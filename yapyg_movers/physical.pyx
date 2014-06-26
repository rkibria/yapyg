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
Simulate physical movement
"""

cimport yapyg.fixpoint
cimport yapyg.movers
cimport yapyg.entities
cimport yapyg.collisions

cdef int IDX_MOVERS_PHYSICAL_ENTITY_NAME = 2
cdef int IDX_MOVERS_PHYSICAL_MASS = 3
cdef int IDX_MOVERS_PHYSICAL_VX = 4
cdef int IDX_MOVERS_PHYSICAL_VY = 5
cdef int IDX_MOVERS_PHYSICAL_AX = 6
cdef int IDX_MOVERS_PHYSICAL_AY = 7
cdef int IDX_MOVERS_PHYSICAL_FRICTION = 8
cdef int IDX_MOVERS_PHYSICAL_INELASTICITY = 9
cdef int IDX_MOVERS_PHYSICAL_ON_END_FUNCTION = 10

cpdef add(list state,
                str entity_name,
                int mass,
                int vx,
                int vy,
                int ax,
                int ay,
                int friction,
                int inelasticity,
                int do_replace=False):
        """
        TODO
        """
        yapyg.movers.add(state,
                entity_name,
                c_create(entity_name,
                        mass,
                        vx, vy,
                        ax, ay,
                        friction,
                        inelasticity,
                        ),
                        do_replace
                )

cdef list c_create(str entity_name,
                int mass,
                int vx,
                int vy,
                int ax,
                int ay,
                int friction,
                int inelasticity,
                ):
        """
        TODO
        """
        return ["physics",
                run,
                entity_name,
                mass,
                vx,
                vy,
                ax,
                ay,
                friction,
                inelasticity,
                ]

FIXP_1000 = yapyg.fixpoint.int2fix(1000)

cpdef run(list state, str entity_name, list mover, int frame_time_delta, list movers_to_delete):
        """
        TODO
        """
        cdef int v_x
        cdef int v_y
        v_x = mover[IDX_MOVERS_PHYSICAL_VX]
        v_y = mover[IDX_MOVERS_PHYSICAL_VY]

        cdef int delta_x
        cdef int delta_y
        delta_x = yapyg.fixpoint.div(yapyg.fixpoint.mul(v_x, frame_time_delta), FIXP_1000)
        delta_y = yapyg.fixpoint.div(yapyg.fixpoint.mul(v_y, frame_time_delta), FIXP_1000)

        yapyg.entities.add_pos(state, entity_name, delta_x, delta_y)

        cdef int a_x
        cdef int a_y
        a_x = mover[IDX_MOVERS_PHYSICAL_AX]
        a_y = mover[IDX_MOVERS_PHYSICAL_AY]

        v_x += a_x
        v_y += a_y

        cdef int friction
        friction = mover[IDX_MOVERS_PHYSICAL_FRICTION]

        mover[IDX_MOVERS_PHYSICAL_VX] = yapyg.fixpoint.mul(v_x, friction)
        mover[IDX_MOVERS_PHYSICAL_VY] = yapyg.fixpoint.mul(v_y, friction)

        cdef tuple collision_result
        collision_result = yapyg.collisions.c_run(state, entity_name)
        if collision_result:
                collision_handler(*collision_result)

FIXP_2 = yapyg.fixpoint.int2fix(2)

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

        cdef int circle_x
        cdef int circle_y
        cdef int circle_r
        circle_x = abs_circle_shape[1]
        circle_y = abs_circle_shape[2]
        circle_r = abs_circle_shape[3]

        cdef int rect_x
        cdef int rect_y
        cdef int rect_w
        cdef int rect_h
        cdef int rect_r
        rect_x = abs_rectangle_shape[1]
        rect_y = abs_rectangle_shape[2]
        rect_w = abs_rectangle_shape[3]
        rect_h = abs_rectangle_shape[4]
        rect_r = abs_rectangle_shape[5]

        cdef tuple circle_move_vector
        circle_move_vector = (circle_physical_mover[IDX_MOVERS_PHYSICAL_VX], circle_physical_mover[IDX_MOVERS_PHYSICAL_VY])

        cdef int inelasticity
        inelasticity = circle_physical_mover[IDX_MOVERS_PHYSICAL_INELASTICITY]

        cdef tuple rotated_circle
        cdef int v_total
        cdef int corner_x
        cdef int corner_y
        cdef int angle
        cdef int angle_dx
        cdef int angle_dy
        cdef int new_vx
        cdef int new_vy

        if rect_r != 0:
                rotated_circle = yapyg.fixpoint.rotated_point(
                        (rect_x + yapyg.fixpoint.div(rect_w, FIXP_2), rect_y + yapyg.fixpoint.div(rect_h, FIXP_2)),
                        (circle_x, circle_y),
                        -rect_r)
                circle_x = rotated_circle[0]
                circle_y = rotated_circle[1]

                circle_move_vector = yapyg.fixpoint.rotated_point((0, 0), circle_move_vector, -rect_r)

        if circle_y <= rect_y or circle_y >= rect_y + rect_h:
                # circle centre below or above rectangle
                if circle_x > rect_x and circle_x < rect_x + rect_w:
                        # lower/upper quadrant
                        if circle_y <= rect_y:
                                # lower quadrant
                                if circle_physical_mover:
                                        circle_move_vector = (circle_move_vector[0],
                                                yapyg.fixpoint.mul(-abs(circle_move_vector[1]), inelasticity))
                        else:
                                # upper quadrant
                                if circle_physical_mover:
                                        circle_move_vector = (circle_move_vector[0],
                                                yapyg.fixpoint.mul(abs(circle_move_vector[1]), inelasticity))
                else:
                        # lower/upper left/right quadrant
                        v_total = yapyg.fixpoint.length(circle_move_vector)
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
                        angle = yapyg.fixpoint.atan2(angle_dy, angle_dx)

                        new_vy = yapyg.fixpoint.mul(yapyg.fixpoint.sin(angle), v_total)
                        new_vx = yapyg.fixpoint.mul(yapyg.fixpoint.cos(angle), v_total)
                        if circle_physical_mover:
                                circle_move_vector = (
                                        yapyg.fixpoint.mul(new_vx, inelasticity),
                                        yapyg.fixpoint.mul(new_vy, inelasticity))
        else:
                # circle same height as rectangle
                if circle_x < rect_x:
                        # left quadrant
                        if circle_physical_mover:
                                circle_move_vector = (
                                        yapyg.fixpoint.mul(-abs(circle_move_vector[0]), inelasticity),
                                        circle_move_vector[1])
                elif circle_x > rect_x + rect_w:
                        # right quadrant
                        if circle_physical_mover:
                                circle_move_vector = (
                                        yapyg.fixpoint.mul(abs(circle_move_vector[0]), inelasticity),
                                        circle_move_vector[1])
                else:
                        # inside rectangle
                        circle_move_vector = (
                                yapyg.fixpoint.mul(-circle_move_vector[0], inelasticity),
                                yapyg.fixpoint.mul(-circle_move_vector[1], inelasticity))

        if circle_physical_mover:
                circle_move_vector = yapyg.fixpoint.rotated_point((0, 0), circle_move_vector, rect_r)
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

        cdef tuple abs_pos_1
        cdef tuple abs_pos_2
        abs_pos_1 = (abs_circle_shape_1[1], abs_circle_shape_1[2])
        abs_pos_2 = (abs_circle_shape_2[1], abs_circle_shape_2[2])

        cdef tuple unit_vector_1_to_2
        unit_vector_1_to_2 = yapyg.fixpoint.unit_vector(abs_pos_1, abs_pos_2)

        cdef tuple speed_vector_1
        cdef tuple speed_vector_2
        speed_vector_1 = (circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VX], circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VY])
        speed_vector_2 = (circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VX], circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VY])

        cdef int new_vx1
        cdef int new_vx2
        cdef int new_vy1
        cdef int new_vy2
        new_vx1, new_vy1, new_vx2, new_vy2 = c_reflect_speeds(
                unit_vector_1_to_2,
                speed_vector_1,
                speed_vector_2,
                circle_physical_mover_1[IDX_MOVERS_PHYSICAL_MASS],
                circle_physical_mover_2[IDX_MOVERS_PHYSICAL_MASS])

        cdef int inelasticity_1
        inelasticity_1 = circle_physical_mover_1[IDX_MOVERS_PHYSICAL_INELASTICITY]
        circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VX] = yapyg.fixpoint.mul(new_vx1, inelasticity_1)
        circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VY] = yapyg.fixpoint.mul(new_vy1, inelasticity_1)

        cdef int inelasticity_2
        inelasticity_2 = circle_physical_mover_2[IDX_MOVERS_PHYSICAL_INELASTICITY]
        circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VX] = yapyg.fixpoint.mul(new_vx2, inelasticity_2)
        circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VY] = yapyg.fixpoint.mul(new_vy2, inelasticity_2)

cpdef collision_handler(list state,
                str entity_name_1,
                str entity_name_2,
                list collision_def_1,
                list collision_def_2,
                tuple absolute_shape_1,
                tuple absolute_shape_2):
        """
        TODO
        """
        cdef list entity_mover_1
        cdef list entity_mover_2
        entity_mover_1 = yapyg.movers.get_active(state, entity_name_1)
        entity_mover_2 = yapyg.movers.get_active(state, entity_name_2)

        cdef list physics_mover_1
        cdef list physics_mover_2
        physics_mover_1 = None
        physics_mover_2 = None
        if (entity_mover_1 and entity_mover_1[0] == "physics"):
                physics_mover_1 = entity_mover_1
        if (entity_mover_2 and entity_mover_2[0] == "physics"):
                physics_mover_2 = entity_mover_2

        if (physics_mover_1 or physics_mover_2):
                if absolute_shape_1[0] == "rectangle":
                        if absolute_shape_2[0] == "rectangle":
                                pass # TODO
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

cdef tuple c_elastic_collision(int v_1, int v_2, int m_1, int m_2):
        """
        TODO
        """
        cdef int mass_sum
        mass_sum = m_1 + m_2

        cdef int diff_1
        diff_1 = m_1 - m_2
        return (yapyg.fixpoint.div(yapyg.fixpoint.mul(v_1, diff_1) + yapyg.fixpoint.mul(FIXP_2, yapyg.fixpoint.mul(m_2, v_2)), mass_sum),
                yapyg.fixpoint.div(yapyg.fixpoint.mul(v_2, -diff_1) + yapyg.fixpoint.mul(FIXP_2, yapyg.fixpoint.mul(m_1, v_1)), mass_sum),
                )

cdef tuple c_reflect_speeds(tuple unit_vector, tuple v1_vector, tuple v2_vector, int m_1, int m_2):
        """
        TODO
        """
        cdef int v1_eff
        cdef int v2_eff
        v1_eff = yapyg.fixpoint.dot_product(unit_vector, v1_vector)
        v2_eff = yapyg.fixpoint.dot_product(unit_vector, v2_vector)

        cdef int new_v1_eff
        cdef int new_v2_eff
        new_v1_eff, new_v2_eff = c_elastic_collision(v1_eff, -v2_eff, m_1, m_2)

        cdef tuple new_v1_eff_vector
        cdef tuple new_v2_eff_vector
        new_v1_eff_vector = yapyg.fixpoint.vector_product(unit_vector, new_v1_eff)
        new_v2_eff_vector = yapyg.fixpoint.vector_product(unit_vector, new_v2_eff)

        cdef tuple v1_perpendicular
        cdef tuple v2_perpendicular
        v1_perpendicular = yapyg.fixpoint.components(unit_vector, v1_vector)[1]
        v2_perpendicular = yapyg.fixpoint.components(unit_vector, v2_vector)[1]

        cdef tuple new_v1_vector
        cdef tuple new_v2_vector
        new_v1_vector = yapyg.fixpoint.vector_diff(v1_perpendicular, new_v1_eff_vector)
        new_v2_vector = yapyg.fixpoint.vector_sum(v2_perpendicular, new_v2_eff_vector)

        return (new_v1_vector[0], new_v1_vector[1],
                new_v2_vector[0], new_v2_vector[1])
