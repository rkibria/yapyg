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
Phyics
"""

import geometry

def elastic_collision(v_1, v_2, m_1, m_2):
    """
    TODO
    """
    return (
        (v_1 * (m_1 - m_2) + 2.0 * m_2 * v_2) / (m_1 + m_2),
        (v_2 * (m_2 - m_1) + 2.0 * m_1 * v_1) / (m_1 + m_2),
        )

def reflect_speeds(normal_vector, v1_vector, v2_vector, m_1, m_2):
    """
    TODO
    """
    v1_eff = geometry.dot_product(normal_vector, v1_vector)
    v2_eff = geometry.dot_product(normal_vector, v2_vector)
    new_v1_eff, new_v2_eff = elastic_collision(v1_eff, -v2_eff, m_1, m_2)
    #
    new_v1_eff = geometry.vector_prod(normal_vector, new_v1_eff)
    new_v2_eff = geometry.vector_prod(normal_vector, new_v2_eff)
    #
    v1_perpendicular = geometry.components(normal_vector, v1_vector)[1]
    v2_perpendicular = geometry.components(normal_vector, v2_vector)[1]
    #
    new_v1_vector = geometry.vector_diff(v1_perpendicular, new_v1_eff)
    new_v2_vector = geometry.vector_sum(v2_perpendicular, new_v2_eff)
    #
    return (new_v1_vector[0], new_v1_vector[1],
        new_v2_vector[0], new_v2_vector[1])
