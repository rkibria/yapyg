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
from yapyg import fixpoint

class TestFixpoint(unittest.TestCase):
        def test_fixpoint_ints(self):
                for i in xrange(-32768, 32768):
                        fx_1 = fixpoint.int2fix(i)
                        i_2 = fixpoint.fix2int(fx_1)
                        self.assertEqual(i, i_2)

        def test_fixpoint_floats(self):
                micro_steps = 100
                for i in xrange(-32768, 32768):
                        for i_ratio in xrange(micro_steps):
                                f_1 = float(i) + float(i_ratio) / float(micro_steps)
                                fx_1 = fixpoint.float2fix(f_1)
                                f_2 = fixpoint.fix2float(fx_1)
                                self.assertAlmostEqual(f_1, f_2, places=2)

        def test_fixpoint_mul(self):
                micro_steps = 10
                for i in xrange(-180, 180):
                        for i_ratio in xrange(micro_steps):
                                f_1 = float(i) + float(i_ratio) / float(micro_steps)
                                fx_1 = fixpoint.float2fix(f_1)
                                for k in xrange(-180, 180):
                                        for k_ratio in xrange(micro_steps):
                                                f_2 = float(k) + float(k_ratio) / float(micro_steps)
                                                fx_2 = fixpoint.float2fix(f_2)
                                                f_mul = f_1 * f_2
                                                fx_mul = fixpoint.mul(fx_1, fx_2)
                                                f_mul_2 = fixpoint.fix2float(fx_mul)
                                                self.assertAlmostEqual(f_mul, f_mul_2, places=2)

if __name__ == '__main__':
        suite = unittest.TestLoader().loadTestsFromTestCase(TestFixpoint)
        unittest.TextTestRunner(verbosity=2).run(suite)
