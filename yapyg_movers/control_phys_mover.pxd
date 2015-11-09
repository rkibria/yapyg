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
        str rest_sprite=*,
        str pos_sprite=*,
        str neg_sprite=*,
        int do_replace=*
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
                )

cpdef run(list state, str entity_name, list mover, int frame_time_delta, list movers_to_delete)
