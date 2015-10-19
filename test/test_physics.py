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

import unittest
from yapyg import math_collision
from yapyg import math_2d

class TestPhysicsCollisionRectRect(unittest.TestCase):
        def test_contact_top_side(self):
                print
                rect_2_angle = 0.0
                rect_1 = ("rectangle", 0.0, 0.0, 1.0, 1.0, 0.0)
                rect_2 = ("rectangle", 0.0, 1.0, 1.0, 1.0, rect_2_angle)
                contact_points = []
                result = math_collision.is_rect_rect_collision(rect_1, rect_2, contact_points)
                contact_sum_vector = math_collision.get_contact_sum_vector(contact_points, (0.0, 0.0))
                self.assertEqual(result, True)
                self.assertEqual(contact_points, [(0.0, 1.0), (1.0, 1.0)])
                self.assertEqual(contact_sum_vector, (0.5, 1.0))

                cases = [
                         # hit from above
                         (0.0, (1.0, -1.0), (1.0, 1.0)),
                         (0.0, (0.0, -1.0), (0.0, 1.0)),
                         (0.0, (-1.0, -1.0), (-1.0, 1.0)),

                         (180.0, (1.0, -1.0), (1.0, 1.0)),

                         # hit from below
                         (0.0, (1.0, 1.0), (1.0, -1.0)),
                         (0.0, (0.0, 1.0), (0.0, -1.0)),
                         (0.0, (-1.0, 1.0), (-1.0, -1.0)),

                         # 
                         (45.0, (1.0, 0.0), (0.0, 1.0)),
                         (45.0, (0.0, -1.0), (-1.0, 0.0)),

                         # hit from the left
                         (90.0, (1.0, 0.0), (-1.0, 0.0)),
                         (90.0, (1.0, 1.0), (-1.0, 1.0)),
                         (90.0, (1.0, -1.0), (-1.0, -1.0)),
                        ]
                for rect_2_angle, v_1, expected_v in cases:
                        rect_2_unit_axis_vector = math_2d.create_unit_vector(rect_2_angle)
                        parallel_v,perpend_v = math_2d.get_projection_vectors(rect_2_unit_axis_vector, v_1)
                        reflect_v = math_2d.vector_sub(v_1, math_2d.vector_mul(perpend_v, 2.0))
                        print rect_2_angle, v_1, ":", reflect_v
                        self.assertAlmostEqual(reflect_v[0], expected_v[0], places=5)
                        self.assertAlmostEqual(reflect_v[1], expected_v[1], places=5)



if __name__ == '__main__':
        suite = unittest.TestLoader().loadTestsFromTestCase(TestPhysicsCollisionRectRect)
        unittest.TextTestRunner(verbosity=2).run(suite)
