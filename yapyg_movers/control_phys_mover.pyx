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
Controller-influenced mover
"""

import yapyg
cimport yapyg.movers
cimport yapyg.entities
cimport yapyg.math_2d
cimport yapyg.controls

import yapyg_movers
cimport yapyg_movers.physical_mover

cdef int IDX_CONTROLLED_PHYSICAL_MOVER_DIR_FACTOR = yapyg_movers.physical_mover.IDX_MOVERS_PHYSICAL_LAST_PARAMETER + 1
cdef int IDX_CONTROLLED_PHYSICAL_MOVER_POS_ACCEL = yapyg_movers.physical_mover.IDX_MOVERS_PHYSICAL_LAST_PARAMETER + 2
cdef int IDX_CONTROLLED_PHYSICAL_MOVER_NEG_ACCEL = yapyg_movers.physical_mover.IDX_MOVERS_PHYSICAL_LAST_PARAMETER + 3
cdef int IDX_CONTROLLED_PHYSICAL_MOVER_REST_SPRITE = yapyg_movers.physical_mover.IDX_MOVERS_PHYSICAL_LAST_PARAMETER + 4
cdef int IDX_CONTROLLED_PHYSICAL_MOVER_POS_SPRITE = yapyg_movers.physical_mover.IDX_MOVERS_PHYSICAL_LAST_PARAMETER + 5
cdef int IDX_CONTROLLED_PHYSICAL_MOVER_NEG_SPRITE = yapyg_movers.physical_mover.IDX_MOVERS_PHYSICAL_LAST_PARAMETER + 6

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
        float dir_factor,
        float pos_accel,
        float neg_accel,
        str rest_sprite=None,
        str pos_sprite=None,
        str neg_sprite=None,
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
                                stickyness,
                                dir_factor,
                                pos_accel,
                                neg_accel,
                                rest_sprite,
                                pos_sprite,
                                neg_sprite
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
                float stickyness,
                float dir_factor,
                float pos_accel,
                float neg_accel,
                str rest_sprite,
                str pos_sprite,
                str neg_sprite,
                ):
        """
        TODO
        """
        cdef list phys_mover_list = yapyg_movers.physical_mover.create(entity_name,
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
                                                        stickyness
                                                        )
        phys_mover_list[yapyg.movers.G_IDX_MOVER_RUN_FUNCTION] = run
        phys_mover_list.append(dir_factor)
        phys_mover_list.append(pos_accel)
        phys_mover_list.append(neg_accel)
        phys_mover_list.append(rest_sprite)
        phys_mover_list.append(pos_sprite)
        phys_mover_list.append(neg_sprite)
        return phys_mover_list

cpdef run(list state, str entity_name, list mover, float frame_time_delta, list movers_to_delete):
        cdef list direction = yapyg.controls.get_joystick(state)
        cdef float joy_dir = direction[0]
        cdef float joy_accel = direction[1]

        cdef tuple player_pos = yapyg.entities.get_pos(state, entity_name)
        cdef float player_rot = player_pos[2]

        cdef tuple player_speed = yapyg_movers.physical_mover.get_velocity(mover)
        cdef float dir_factor = mover[IDX_CONTROLLED_PHYSICAL_MOVER_DIR_FACTOR] * yapyg.math_2d.length(player_speed)

        cdef float accel_factor
        if joy_accel > 0.0:
                accel_factor = mover[IDX_CONTROLLED_PHYSICAL_MOVER_POS_ACCEL]
        else:
                accel_factor = mover[IDX_CONTROLLED_PHYSICAL_MOVER_NEG_ACCEL]

        cdef tuple accel_vector = yapyg.math_2d.vector_mul(yapyg.math_2d.rotated_point((0, 0), (0.0, 1.0), player_rot), accel_factor * joy_accel)
        yapyg_movers.physical_mover.set_acceleration(mover, accel_vector)
        yapyg_movers.physical_mover.set_velocity(mover,
                                    (player_speed[0],
                                     player_speed[1],
                                     player_speed[2] + (-joy_dir) * dir_factor * (-1 if joy_accel < 0 else 1)
                                     )
                                    )

        cdef str pos_sprite = mover[IDX_CONTROLLED_PHYSICAL_MOVER_POS_SPRITE]
        cdef str neg_sprite = mover[IDX_CONTROLLED_PHYSICAL_MOVER_NEG_SPRITE]
        cdef str rest_sprite = mover[IDX_CONTROLLED_PHYSICAL_MOVER_REST_SPRITE]
        if pos_sprite and joy_accel > 0.0:
                yapyg.entities.set_active_sprite(state, entity_name, pos_sprite)
        elif rest_sprite and joy_accel == 0.0:
                yapyg.entities.set_active_sprite(state, entity_name, rest_sprite)
        elif neg_sprite:
                yapyg.entities.set_active_sprite(state, entity_name, neg_sprite)

        return yapyg_movers.physical_mover.run(state, entity_name, mover, frame_time_delta, movers_to_delete)
