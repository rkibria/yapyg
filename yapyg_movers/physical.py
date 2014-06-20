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

import yapyg.movers
import yapyg.entities
import yapyg.fixpoint

IDX_MOVERS_PHYSICAL_ENTITY_NAME = 2
IDX_MOVERS_PHYSICAL_MASS = 3
IDX_MOVERS_PHYSICAL_VX = 4
IDX_MOVERS_PHYSICAL_VY = 5
IDX_MOVERS_PHYSICAL_AX = 6
IDX_MOVERS_PHYSICAL_AY = 7
IDX_MOVERS_PHYSICAL_FRICTION = 8
IDX_MOVERS_PHYSICAL_INELASTICITY = 9
IDX_MOVERS_PHYSICAL_ON_END_FUNCTION = 10

def add(state, entity_name,
                mass=1.0,
                vx=0, vy=0,
                ax=0, ay=0,
                friction=1.0, inelasticity=1.0,
                on_end_function=None, do_replace=False):
        """
        TODO
        """
        yapyg.movers.add(state, entity_name, create(entity_name,
                mass,
                vx, vy,
                ax, ay,
                friction, inelasticity,
                on_end_function), do_replace)

def create(entity_name,
                mass,
                vx, vy,
                ax, ay,
                friction, inelasticity,
                on_end_function=None):
        """
        TODO
        """
        return ["physics",
                run,
                entity_name,
                yapyg.fixpoint.float2fix(mass),
                yapyg.fixpoint.float2fix(vx),
                yapyg.fixpoint.float2fix(vy),
                yapyg.fixpoint.float2fix(ax),
                yapyg.fixpoint.float2fix(ay),
                yapyg.fixpoint.float2fix(friction),
                yapyg.fixpoint.float2fix(inelasticity),
                on_end_function,]

def run(state, entity_name, mover, frame_time_delta, movers_to_delete):
        """
        TODO
        """
        mul = yapyg.fixpoint.mul
        div = yapyg.fixpoint.div

        v_x = mover[IDX_MOVERS_PHYSICAL_VX]
        v_y = mover[IDX_MOVERS_PHYSICAL_VY]

        FIXP_1000 = yapyg.fixpoint.int2fix(1000)
        delta_x = div(mul(v_x, frame_time_delta), FIXP_1000)
        delta_y = div(mul(v_y, frame_time_delta), FIXP_1000)

        yapyg.entities.add_pos(state, entity_name, delta_x, delta_y)

        v_x += mover[IDX_MOVERS_PHYSICAL_AX]
        v_y += mover[IDX_MOVERS_PHYSICAL_AY]

        friction = mover[IDX_MOVERS_PHYSICAL_FRICTION]
        mover[IDX_MOVERS_PHYSICAL_VX] = mul(v_x, friction)
        mover[IDX_MOVERS_PHYSICAL_VY] = mul(v_y, friction)

def _rectangle_circle_collision(state, rectangle_entity_name, circle_entity_name,
                abs_rectangle_shape, abs_circle_shape,
                rectangle_physical_mover, circle_physical_mover):
        """
        TODO
        """
        yapyg.entities.undo_last_move(state, circle_entity_name)

        circle_x = (abs_circle_shape[1])
        circle_y = (abs_circle_shape[2])
        circle_r = (abs_circle_shape[3])

        rect_x = (abs_rectangle_shape[1])
        rect_y = (abs_rectangle_shape[2])
        rect_w = (abs_rectangle_shape[3])
        rect_h = (abs_rectangle_shape[4])
        rect_r = (abs_rectangle_shape[5])

        circle_move_vector = (circle_physical_mover[IDX_MOVERS_PHYSICAL_VX], circle_physical_mover[IDX_MOVERS_PHYSICAL_VY])
        inelasticity = circle_physical_mover[IDX_MOVERS_PHYSICAL_INELASTICITY]

        FIXP_2 = yapyg.fixpoint.int2fix(2)
        
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
                        corner_y = None
                        corner_x = None
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

def _circle_circle_collision(state, circle_entity_name_1, circle_entity_name_2,
                abs_circle_shape_1, abs_circle_shape_2,
                circle_physical_mover_1, circle_physical_mover_2):
        """
        TODO
        """
        yapyg.entities.undo_last_move(state, circle_entity_name_1)

        abs_pos_1 = (abs_circle_shape_1[1], abs_circle_shape_1[2])
        abs_pos_2 = (abs_circle_shape_2[1], abs_circle_shape_2[2])

        unit_vector_1_to_2 = yapyg.fixpoint.unit_vector(abs_pos_1, abs_pos_2)

        speed_vector_1 = (circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VX], circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VY])
        speed_vector_2 = (circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VX], circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VY])

        new_vx1, new_vy1, new_vx2, new_vy2 = reflect_speeds(unit_vector_1_to_2,
                speed_vector_1,
                speed_vector_2,
                circle_physical_mover_1[IDX_MOVERS_PHYSICAL_MASS],
                circle_physical_mover_2[IDX_MOVERS_PHYSICAL_MASS])

        circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VX] = yapyg.fixpoint.mul(new_vx1, circle_physical_mover_1[IDX_MOVERS_PHYSICAL_INELASTICITY])
        circle_physical_mover_1[IDX_MOVERS_PHYSICAL_VY] = yapyg.fixpoint.mul(new_vy1, circle_physical_mover_1[IDX_MOVERS_PHYSICAL_INELASTICITY])

        circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VX] = yapyg.fixpoint.mul(new_vx2, circle_physical_mover_2[IDX_MOVERS_PHYSICAL_INELASTICITY])
        circle_physical_mover_2[IDX_MOVERS_PHYSICAL_VY] = yapyg.fixpoint.mul(new_vy2, circle_physical_mover_2[IDX_MOVERS_PHYSICAL_INELASTICITY])

def collision_handler(state, entity_name_1, entity_name_2, collision_def_1, collision_def_2, absolute_shape_1, absolute_shape_2):
        """
        TODO
        """
        entity_mover_1 = yapyg.movers.get_active(state, entity_name_1)
        entity_mover_2 = yapyg.movers.get_active(state, entity_name_2)

        physics_mover_1 = None
        physics_mover_2 = None
        if (entity_mover_1 and entity_mover_1[0] == "physics"):
                physics_mover_1 = entity_mover_1
        if (entity_mover_2 and entity_mover_2[0] == "physics"):
                physics_mover_2 = entity_mover_2

        if (physics_mover_1 or physics_mover_2):
                if absolute_shape_1[0] == "rectangle":
                        if absolute_shape_2[0] == "rectangle":
                                print "TODO r-r"
                                exit()
                        elif absolute_shape_2[0] == "circle":
                                _rectangle_circle_collision(state, entity_name_1, entity_name_2,
                                        absolute_shape_1, absolute_shape_2,
                                        physics_mover_1, physics_mover_2)
                elif absolute_shape_1[0] == "circle":
                        if absolute_shape_2[0] == "rectangle":
                                _rectangle_circle_collision(state, entity_name_2, entity_name_1,
                                        absolute_shape_2, absolute_shape_1,
                                        physics_mover_2, physics_mover_1)
                        elif absolute_shape_2[0] == "circle":
                                _circle_circle_collision(state, entity_name_1, entity_name_2,
                                        absolute_shape_1, absolute_shape_2,
                                        physics_mover_1, physics_mover_2)

def elastic_collision(v_1, v_2, m_1, m_2):
        """
        TODO
        """
        FIXP_2 = yapyg.fixpoint.int2fix(2)
        mass_sum = m_1 + m_2
        return (
                yapyg.fixpoint.div(yapyg.fixpoint.mul(v_1, m_1 - m_2) + yapyg.fixpoint.mul(FIXP_2, yapyg.fixpoint.mul(m_2, v_2)), mass_sum),
                yapyg.fixpoint.div(yapyg.fixpoint.mul(v_2, m_2 - m_1) + yapyg.fixpoint.mul(FIXP_2, yapyg.fixpoint.mul(m_1, v_1)), mass_sum),
                )

def reflect_speeds(unit_vector, v1_vector, v2_vector, m_1, m_2):
        """
        TODO
        """
        v1_eff = yapyg.fixpoint.dot_product(unit_vector, v1_vector)
        v2_eff = yapyg.fixpoint.dot_product(unit_vector, v2_vector)
        new_v1_eff, new_v2_eff = elastic_collision(v1_eff, yapyg.fixpoint.negate(v2_eff), m_1, m_2)

        new_v1_eff = yapyg.fixpoint.vector_product(unit_vector, new_v1_eff)
        new_v2_eff = yapyg.fixpoint.vector_product(unit_vector, new_v2_eff)

        v1_perpendicular = yapyg.fixpoint.components(unit_vector, v1_vector)[1]
        v2_perpendicular = yapyg.fixpoint.components(unit_vector, v2_vector)[1]

        new_v1_vector = yapyg.fixpoint.vector_diff(v1_perpendicular, new_v1_eff)
        new_v2_vector = yapyg.fixpoint.vector_sum(v2_perpendicular, new_v2_eff)

        return (new_v1_vector[0], new_v1_vector[1],
                new_v2_vector[0], new_v2_vector[1])
