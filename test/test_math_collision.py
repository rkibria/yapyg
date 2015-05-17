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

class TestMathCollisionRectCircle(unittest.TestCase):
        def test_contact_mid_left_side(self):
                circ = ("circle", 0.0, 0.0, 1.0)
                rect = ("rectangle", 1.0, -1.0, 1.0, 2.0, 0.0)
                contact_points = []
                self.assertEqual(math_collision.is_rect_circle_collision(circ, rect, contact_points), 1)
                self.assertEqual(contact_points, [(1.0, 0.0)])

        def test_contact_mid_right_side(self):
                circ = ("circle", 0.0, 0.0, 1.0)
                rect = ("rectangle", -2.0, -1.0, 1.0, 2.0, 0.0)
                contact_points = []
                self.assertEqual(math_collision.is_rect_circle_collision(circ, rect, contact_points), 1)
                self.assertEqual(contact_points, [(-1.0, 0.0)])

        def test_contact_mid_top_side(self):
                circ = ("circle", 0.0, 0.0, 1.0)
                rect = ("rectangle", -1.0, -2.0, 2.0, 1.0, 0.0)
                contact_points = []
                self.assertEqual(math_collision.is_rect_circle_collision(circ, rect, contact_points), 1)
                self.assertEqual(contact_points, [(0.0, -1.0)])

        def test_contact_mid_bottom_side(self):
                circ = ("circle", 0.0, 0.0, 1.0)
                rect = ("rectangle", -1.0, 1.0, 2.0, 1.0, 0.0)
                contact_points = []
                self.assertEqual(math_collision.is_rect_circle_collision(circ, rect, contact_points), 1)
                self.assertEqual(contact_points, [(0.0, 1.0)])

if __name__ == '__main__':
        suite = unittest.TestLoader().loadTestsFromTestCase(TestMathCollisionRectCircle)
        unittest.TextTestRunner(verbosity=2).run(suite)
