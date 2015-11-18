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
Fixed point math
"""

cdef int FIXP_minus1 = int2fix(-1)
cdef int FIXP_2 = int2fix(2)

cpdef int int2fix(int value):
        """
        TODO
        """
        return value << 16

cpdef int float2fix(float value):
        """
        TODO
        """
        return int(value * 65536.0)

cpdef int fix2int(int value):
        """
        TODO
        """
        return value >> 16

cpdef float fix2float(int value):
        """
        TODO
        """
        return value * 0.0000152587890625  # (1/65536.0)

cpdef int mul(int op1, int op2):
        """
        TODO
        """
        cdef long long r
        r = long(op1) * long(op2)
        return int(r >> 16)

cpdef int div(int op1, int op2):
        """
        TODO
        """
        cdef long long o1
        o1 = long(op1) << 16
        cdef long long r
        r = o1 / long(op2)
        return int(r)

cdef int _bit_len(int int_type):
        """
        TODO
        """
        cdef int length
        length = 0
        while (int_type):
                int_type >>= 1
                length += 1
        return length

cpdef int sqrt(int x):
        """
        Babylonian method
        """
        if x == 0:
                return 0
        cdef int significant_bits
        significant_bits = _bit_len(x >> 16)

        cdef int x_n
        x_n = int2fix(1 << (significant_bits / 2))

        cdef int x_n_plus_1
        for i in xrange(10):
                if x_n == 0:
                        return x_n
                x_n_plus_1 = div((x_n + div(x, x_n)), FIXP_2)
                if x_n_plus_1 == x_n:
                        return x_n
                else:
                        x_n = x_n_plus_1
        return x_n

cpdef int negate(int x):
        """
        TODO
        """
        return mul(FIXP_minus1, x)

cpdef int floor(int x):
        """
        TODO
        """
        return int2fix(fix2int(x))

cpdef int modulo(int x, int d):
        """
        TODO
        """
        cdef int int_x = fix2int(x)
        cdef int int_d = fix2int(d)

        cdef int int_res = int_x % int_d

        cdef int x_fraction = x - int2fix(int_x)
        cdef fix_res = int2fix(int_res)
        fix_res += x_fraction

        return fix_res

cpdef list fixtuple2floatlist(fix_tuple):
        cdef list out_list = []
        cdef int fix_value
        for fix_value in fix_tuple:
                out_list.append(fix2float(fix_value))
        return out_list

cpdef str fixtuple2str(tuple fix_tuple, int precision=3):
        cdef list float_list = fixtuple2floatlist(fix_tuple)
        cdef str out_string = "("
        cdef int i
        cdef float float_value
        cdef str format_string
        for i in xrange(len(float_list)):
                float_value = float_list[i]
                format_string = "%%.%df" % precision
                out_string += (format_string % float_value)
                if i != len(float_list) - 1:
                        out_string += ", "
        out_string += ")"
        return out_string
