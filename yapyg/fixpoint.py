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

def int2fix(value):
        """
        TODO
        """
        return value << 16

def float2fix(value):
        """
        TODO
        """
        return int(value * 65536.0)

def fix2int(value):
        """
        TODO
        """
        return value >> 16

def fix2float(value):
        """
        TODO
        """
        return value * 0.0000152587890625  # (1/65536.0)

def mul(op1, op2):
        """
        TODO
        """
        r = long(op1) * long(op2)
        return int(r >> 16)

def div(op1, op2):
        """
        TODO
        """
        o1 = long(op1) << 16
        r = long(o1 / long(op2))
        return int(r)

FIXP_0 = int2fix(0)
FIXP_1 = int2fix(1)
FIXP_2 = int2fix(2)
FIXP_90 = int2fix(90)
FIXP_128 = int2fix(128)
FIXP_180 = int2fix(180)
FIXP_270 = int2fix(270)
FIXP_360 = int2fix(360)
FIXP_1000 = int2fix(1000)

FIXP_1_5 = float2fix(1.5)

FIXP_PI = float2fix(3.14159265359)

def dot_product(v_1, v_2):
        """
        TODO
        """
        return mul(v_1[0], v_2[0]) + mul(v_1[1], v_2[1])

def vector_product(vec, factor):
        """
        TODO
        """
        return (mul(vec[0], factor), mul(vec[1], factor))

def vector_diff(v_1, v_2):
        """
        TODO
        """
        return (v_1[0] - v_2[0], v_1[1] - v_2[1])

def vector_sum(v_1, v_2):
        """
        TODO
        """
        return (v_1[0] + v_2[0], v_1[1] + v_2[1])

def components(normal_vector, v_vector):
        """
        TODO
        """
        parallel_vector = vector_product(normal_vector,
                dot_product(normal_vector, v_vector))
        perpendicular_vector = vector_diff(v_vector, parallel_vector)
        return (parallel_vector, perpendicular_vector)

def complex_multiply(complex_1, complex_2):
        """
        TODO
        """
        return (mul(complex_1[0], complex_2[0]) - mul(complex_1[1], complex_2[1]),
                mul(complex_1[0], complex_2[1]) + mul(complex_1[1], complex_2[0]))

# sin/cos
trigonometry_table = (
        (0, 65536), # 0
        (1143, 65526), # 1
        (2287, 65496), # 2
        (3429, 65446), # 3
        (4571, 65376), # 4
        (5711, 65286), # 5
        (6850, 65176), # 6
        (7986, 65047), # 7
        (9120, 64898), # 8
        (10252, 64729), # 9
        (11380, 64540), # 10
        (12504, 64331), # 11
        (13625, 64103), # 12
        (14742, 63856), # 13
        (15854, 63589), # 14
        (16961, 63302), # 15
        (18064, 62997), # 16
        (19160, 62672), # 17
        (20251, 62328), # 18
        (21336, 61965), # 19
        (22414, 61583), # 20
        (23486, 61183), # 21
        (24550, 60763), # 22
        (25606, 60326), # 23
        (26655, 59870), # 24
        (27696, 59395), # 25
        (28729, 58903), # 26
        (29752, 58393), # 27
        (30767, 57864), # 28
        (31772, 57319), # 29
        (32767, 56755), # 30
        (33753, 56175), # 31
        (34728, 55577), # 32
        (35693, 54963), # 33
        (36647, 54331), # 34
        (37589, 53683), # 35
        (38521, 53019), # 36
        (39440, 52339), # 37
        (40347, 51643), # 38
        (41243, 50931), # 39
        (42125, 50203), # 40
        (42995, 49460), # 41
        (43852, 48702), # 42
        (44695, 47929), # 43
        (45525, 47142), # 44
        (46340, 46340), # 45
        (47142, 45525), # 46
        (47929, 44695), # 47
        (48702, 43852), # 48
        (49460, 42995), # 49
        (50203, 42125), # 50
        (50931, 41243), # 51
        (51643, 40347), # 52
        (52339, 39440), # 53
        (53019, 38521), # 54
        (53683, 37589), # 55
        (54331, 36647), # 56
        (54963, 35693), # 57
        (55577, 34728), # 58
        (56175, 33753), # 59
        (56755, 32768), # 60
        (57319, 31772), # 61
        (57864, 30767), # 62
        (58393, 29752), # 63
        (58903, 28729), # 64
        (59395, 27696), # 65
        (59870, 26655), # 66
        (60326, 25606), # 67
        (60763, 24550), # 68
        (61183, 23486), # 69
        (61583, 22414), # 70
        (61965, 21336), # 71
        (62328, 20251), # 72
        (62672, 19160), # 73
        (62997, 18064), # 74
        (63302, 16961), # 75
        (63589, 15854), # 76
        (63856, 14742), # 77
        (64103, 13625), # 78
        (64331, 12504), # 79
        (64540, 11380), # 80
        (64729, 10252), # 81
        (64898, 9120), # 82
        (65047, 7986), # 83
        (65176, 6850), # 84
        (65286, 5711), # 85
        (65376, 4571), # 86
        (65446, 3429), # 87
        (65496, 2287), # 88
        (65526, 1143), # 89
        (65536, 0), # 90
        (65526, -1143), # 91
        (65496, -2287), # 92
        (65446, -3429), # 93
        (65376, -4571), # 94
        (65286, -5711), # 95
        (65176, -6850), # 96
        (65047, -7986), # 97
        (64898, -9120), # 98
        (64729, -10252), # 99
        (64540, -11380), # 100
        (64331, -12504), # 101
        (64103, -13625), # 102
        (63856, -14742), # 103
        (63589, -15854), # 104
        (63302, -16961), # 105
        (62997, -18064), # 106
        (62672, -19160), # 107
        (62328, -20251), # 108
        (61965, -21336), # 109
        (61583, -22414), # 110
        (61183, -23486), # 111
        (60763, -24550), # 112
        (60326, -25606), # 113
        (59870, -26655), # 114
        (59395, -27696), # 115
        (58903, -28729), # 116
        (58393, -29752), # 117
        (57864, -30767), # 118
        (57319, -31772), # 119
        (56755, -32767), # 120
        (56175, -33753), # 121
        (55577, -34728), # 122
        (54963, -35693), # 123
        (54331, -36647), # 124
        (53683, -37589), # 125
        (53019, -38521), # 126
        (52339, -39440), # 127
        (51643, -40347), # 128
        (50931, -41243), # 129
        (50203, -42125), # 130
        (49460, -42995), # 131
        (48702, -43852), # 132
        (47929, -44695), # 133
        (47142, -45525), # 134
        (46340, -46340), # 135
        (45525, -47142), # 136
        (44695, -47929), # 137
        (43852, -48702), # 138
        (42995, -49460), # 139
        (42125, -50203), # 140
        (41243, -50931), # 141
        (40347, -51643), # 142
        (39440, -52339), # 143
        (38521, -53019), # 144
        (37589, -53683), # 145
        (36647, -54331), # 146
        (35693, -54963), # 147
        (34728, -55577), # 148
        (33753, -56175), # 149
        (32767, -56755), # 150
        (31772, -57319), # 151
        (30767, -57864), # 152
        (29752, -58393), # 153
        (28729, -58903), # 154
        (27696, -59395), # 155
        (26655, -59870), # 156
        (25606, -60326), # 157
        (24550, -60763), # 158
        (23486, -61183), # 159
        (22414, -61583), # 160
        (21336, -61965), # 161
        (20251, -62328), # 162
        (19160, -62672), # 163
        (18064, -62997), # 164
        (16961, -63302), # 165
        (15854, -63589), # 166
        (14742, -63856), # 167
        (13625, -64103), # 168
        (12504, -64331), # 169
        (11380, -64540), # 170
        (10252, -64729), # 171
        (9120, -64898), # 172
        (7986, -65047), # 173
        (6850, -65176), # 174
        (5711, -65286), # 175
        (4571, -65376), # 176
        (3429, -65446), # 177
        (2287, -65496), # 178
        (1143, -65526), # 179
        (0, -65536), # 180
        (-1143, -65526), # 181
        (-2287, -65496), # 182
        (-3429, -65446), # 183
        (-4571, -65376), # 184
        (-5711, -65286), # 185
        (-6850, -65176), # 186
        (-7986, -65047), # 187
        (-9120, -64898), # 188
        (-10252, -64729), # 189
        (-11380, -64540), # 190
        (-12504, -64331), # 191
        (-13625, -64103), # 192
        (-14742, -63856), # 193
        (-15854, -63589), # 194
        (-16961, -63302), # 195
        (-18064, -62997), # 196
        (-19160, -62672), # 197
        (-20251, -62328), # 198
        (-21336, -61965), # 199
        (-22414, -61583), # 200
        (-23486, -61183), # 201
        (-24550, -60763), # 202
        (-25606, -60326), # 203
        (-26655, -59870), # 204
        (-27696, -59395), # 205
        (-28729, -58903), # 206
        (-29752, -58393), # 207
        (-30767, -57864), # 208
        (-31772, -57319), # 209
        (-32768, -56755), # 210
        (-33753, -56175), # 211
        (-34728, -55577), # 212
        (-35693, -54963), # 213
        (-36647, -54331), # 214
        (-37589, -53683), # 215
        (-38521, -53019), # 216
        (-39440, -52339), # 217
        (-40347, -51643), # 218
        (-41243, -50931), # 219
        (-42125, -50203), # 220
        (-42995, -49460), # 221
        (-43852, -48702), # 222
        (-44695, -47929), # 223
        (-45525, -47142), # 224
        (-46340, -46340), # 225
        (-47142, -45525), # 226
        (-47929, -44695), # 227
        (-48702, -43852), # 228
        (-49460, -42995), # 229
        (-50203, -42125), # 230
        (-50931, -41243), # 231
        (-51643, -40347), # 232
        (-52339, -39440), # 233
        (-53019, -38521), # 234
        (-53683, -37589), # 235
        (-54331, -36647), # 236
        (-54963, -35693), # 237
        (-55577, -34728), # 238
        (-56175, -33753), # 239
        (-56755, -32768), # 240
        (-57319, -31772), # 241
        (-57864, -30767), # 242
        (-58393, -29752), # 243
        (-58903, -28729), # 244
        (-59395, -27696), # 245
        (-59870, -26655), # 246
        (-60326, -25606), # 247
        (-60763, -24550), # 248
        (-61183, -23486), # 249
        (-61583, -22414), # 250
        (-61965, -21336), # 251
        (-62328, -20251), # 252
        (-62672, -19160), # 253
        (-62997, -18064), # 254
        (-63302, -16961), # 255
        (-63589, -15854), # 256
        (-63856, -14742), # 257
        (-64103, -13625), # 258
        (-64331, -12504), # 259
        (-64540, -11380), # 260
        (-64729, -10252), # 261
        (-64898, -9120), # 262
        (-65047, -7986), # 263
        (-65176, -6850), # 264
        (-65286, -5711), # 265
        (-65376, -4571), # 266
        (-65446, -3429), # 267
        (-65496, -2287), # 268
        (-65526, -1143), # 269
        (-65536, 0), # 270
        (-65526, 1143), # 271
        (-65496, 2287), # 272
        (-65446, 3429), # 273
        (-65376, 4571), # 274
        (-65286, 5711), # 275
        (-65176, 6850), # 276
        (-65047, 7986), # 277
        (-64898, 9120), # 278
        (-64729, 10252), # 279
        (-64540, 11380), # 280
        (-64331, 12504), # 281
        (-64103, 13625), # 282
        (-63856, 14742), # 283
        (-63589, 15854), # 284
        (-63302, 16961), # 285
        (-62997, 18064), # 286
        (-62672, 19160), # 287
        (-62328, 20251), # 288
        (-61965, 21336), # 289
        (-61583, 22414), # 290
        (-61183, 23486), # 291
        (-60763, 24550), # 292
        (-60326, 25606), # 293
        (-59870, 26655), # 294
        (-59395, 27696), # 295
        (-58903, 28729), # 296
        (-58393, 29752), # 297
        (-57864, 30767), # 298
        (-57319, 31772), # 299
        (-56755, 32768), # 300
        (-56175, 33753), # 301
        (-55577, 34728), # 302
        (-54963, 35693), # 303
        (-54331, 36647), # 304
        (-53683, 37589), # 305
        (-53019, 38521), # 306
        (-52339, 39440), # 307
        (-51643, 40347), # 308
        (-50931, 41243), # 309
        (-50203, 42125), # 310
        (-49460, 42995), # 311
        (-48702, 43852), # 312
        (-47929, 44695), # 313
        (-47142, 45525), # 314
        (-46340, 46340), # 315
        (-45525, 47142), # 316
        (-44695, 47929), # 317
        (-43852, 48702), # 318
        (-42995, 49460), # 319
        (-42125, 50203), # 320
        (-41243, 50931), # 321
        (-40347, 51643), # 322
        (-39440, 52339), # 323
        (-38521, 53019), # 324
        (-37589, 53683), # 325
        (-36647, 54331), # 326
        (-35693, 54963), # 327
        (-34728, 55577), # 328
        (-33753, 56175), # 329
        (-32768, 56755), # 330
        (-31772, 57319), # 331
        (-30767, 57864), # 332
        (-29752, 58393), # 333
        (-28729, 58903), # 334
        (-27696, 59395), # 335
        (-26655, 59870), # 336
        (-25606, 60326), # 337
        (-24550, 60763), # 338
        (-23486, 61183), # 339
        (-22414, 61583), # 340
        (-21336, 61965), # 341
        (-20251, 62328), # 342
        (-19160, 62672), # 343
        (-18064, 62997), # 344
        (-16961, 63302), # 345
        (-15854, 63589), # 346
        (-14742, 63856), # 347
        (-13625, 64103), # 348
        (-12504, 64331), # 349
        (-11380, 64540), # 350
        (-10252, 64729), # 351
        (-9120, 64898), # 352
        (-7986, 65047), # 353
        (-6850, 65176), # 354
        (-5711, 65286), # 355
        (-4571, 65376), # 356
        (-3429, 65446), # 357
        (-2287, 65496), # 358
        (-1143, 65526), # 359
        (0, 65536), # 360
        )

def sin(degrees):
        """
        TODO
        """
        int_degrees = fix2int(degrees)
        fix_whole_degrees = int2fix(int_degrees)
        fix_remainder_degrees = degrees - fix_whole_degrees

        int_degrees_capped = int_degrees % 360
        lower_sin = trigonometry_table[int_degrees_capped][0]
        higher_sin = trigonometry_table[int_degrees_capped + 1][0]
        delta_sin = higher_sin - lower_sin
        return lower_sin + mul(delta_sin, fix_remainder_degrees)

def cos(degrees):
        """
        TODO
        """
        int_degrees = fix2int(degrees)
        fix_whole_degrees = int2fix(int_degrees)
        fix_remainder_degrees = degrees - fix_whole_degrees

        int_degrees_capped = int_degrees % 360
        lower_cos = trigonometry_table[int_degrees_capped][1]
        higher_cos = trigonometry_table[int_degrees_capped + 1][1]
        delta_cos = higher_cos - lower_cos
        return lower_cos + mul(delta_cos, fix_remainder_degrees)

def rotated_point(origin_point, point, rot):
        """
        TODO
        """
        rot_relative_point = complex_multiply((point[0] - origin_point[0],
                point[1] - origin_point[1]), (cos(rot), sin(rot)))
        return (origin_point[0] + rot_relative_point[0], origin_point[1] + rot_relative_point[1])

def _bit_len(int_type):
        length = 0
        while (int_type):
                int_type >>= 1
                length += 1
        return length

def sqrt(x):
        """
        Babylonian method
        """
        if x == FIXP_0:
                return FIXP_0
        significant_bits = _bit_len(x >> 16)
        x_n = int2fix(1 << (significant_bits / 2))

        for i in xrange(10):
                if x_n == 0:
                        return x_n
                x_n_plus_1 = div((x_n + div(x, x_n)), FIXP_2)
                if x_n_plus_1 == x_n:
                        return x_n
                else:
                        x_n = x_n_plus_1
        return x_n

def length(vector):
        """
        TODO
        """
        x_dist = vector[0]
        x_dist = mul(x_dist, x_dist)

        y_dist = vector[1]
        y_dist = mul(y_dist, y_dist)

        return sqrt(x_dist + y_dist)

def distance(pos_1, pos_2):
        """
        Euclidian distance between pos_1 and pos_2
        """
        return length((pos_2[0] - pos_1[0], pos_2[1] - pos_1[1],))

def unit_vector(pos_1, pos_2):
        """
        Returns a unit vector pointing from pos_1 to pos_2
        """
        vector_distance = distance(pos_1, pos_2)
        return (div(pos_2[0] - pos_1[0], vector_distance),
                div(pos_2[1] - pos_1[1], vector_distance),)

# t[i] = arctan_degrees(1.0 / 128 * i)
arctan_table = (
        0, # 0
        29334, # 1
        58666, # 2
        87990, # 3
        117303, # 4
        146602, # 5
        175883, # 6
        205143, # 7
        234378, # 8
        263585, # 9
        292759, # 10
        321898, # 11
        350999, # 12
        380057, # 13
        409070, # 14
        438033, # 15
        466945, # 16
        495800, # 17
        524597, # 18
        553332, # 19
        582002, # 20
        610604, # 21
        639134, # 22
        667590, # 23
        695969, # 24
        724268, # 25
        752483, # 26
        780613, # 27
        808654, # 28
        836604, # 29
        864459, # 30
        892219, # 31
        919879, # 32
        947437, # 33
        974892, # 34
        1002241, # 35
        1029481, # 36
        1056610, # 37
        1083627, # 38
        1110528, # 39
        1137313, # 40
        1163979, # 41
        1190524, # 42
        1216946, # 43
        1243244, # 44
        1269416, # 45
        1295461, # 46
        1321376, # 47
        1347160, # 48
        1372813, # 49
        1398332, # 50
        1423716, # 51
        1448964, # 52
        1474075, # 53
        1499048, # 54
        1523881, # 55
        1548574, # 56
        1573126, # 57
        1597536, # 58
        1621802, # 59
        1645925, # 60
        1669904, # 61
        1693737, # 62
        1717425, # 63
        1740967, # 64
        1764362, # 65
        1787609, # 66
        1810710, # 67
        1833662, # 68
        1856467, # 69
        1879123, # 70
        1901630, # 71
        1923989, # 72
        1946199, # 73
        1968261, # 74
        1990173, # 75
        2011937, # 76
        2033551, # 77
        2055017, # 78
        2076335, # 79
        2097504, # 80
        2118525, # 81
        2139399, # 82
        2160124, # 83
        2180703, # 84
        2201134, # 85
        2221419, # 86
        2241557, # 87
        2261550, # 88
        2281398, # 89
        2301100, # 90
        2320659, # 91
        2340073, # 92
        2359345, # 93
        2378473, # 94
        2397460, # 95
        2416305, # 96
        2435009, # 97
        2453574, # 98
        2471998, # 99
        2490284, # 100
        2508432, # 101
        2526443, # 102
        2544317, # 103
        2562055, # 104
        2579657, # 105
        2597126, # 106
        2614461, # 107
        2631663, # 108
        2648733, # 109
        2665672, # 110
        2682481, # 111
        2699160, # 112
        2715711, # 113
        2732134, # 114
        2748429, # 115
        2764599, # 116
        2780644, # 117
        2796564, # 118
        2812360, # 119
        2828035, # 120
        2843587, # 121
        2859018, # 122
        2874330, # 123
        2889522, # 124
        2904597, # 125
        2919554, # 126
        2934394, # 127
        2949120, # 128
        )

ARCTAN_STEP_SIZE = div(FIXP_1, FIXP_128)

def atan2(y, x):
        """
        TODO
        """
        y_abs = abs(y)
        x_abs = abs(x)

        # Octants start in upper right quadrant and go counter-clockwise
        if y >= 0:
                if x >= 0:
                        # upper right quadrant
                        if y_abs < x_abs:
                                # octant 1
                                quot = div(y_abs, x_abs)
                                base = FIXP_0
                                add_to_base = True
                        else:
                                # octant 2
                                quot = div(x_abs, y_abs)
                                base = FIXP_90
                                add_to_base = False
                else:
                        # upper left quadrant
                        if y_abs >= x_abs:
                                # octant 3
                                quot = div(x_abs, y_abs)
                                base = FIXP_90
                                add_to_base = True
                        else:
                                # octant 4
                                quot = div(y_abs, x_abs)
                                base = FIXP_180
                                add_to_base = False
        else:
                if x < 0:
                        # lower left quadrant
                        if y_abs < x_abs:
                                # octant 5
                                quot = div(y_abs, x_abs)
                                base = FIXP_180
                                add_to_base = True
                        else:
                                # octant 6
                                quot = div(x_abs, y_abs)
                                base = FIXP_270
                                add_to_base = False
                else:
                        # lower right quadrant
                        if y_abs >= x_abs:
                                # octant 7
                                quot = div(x_abs, y_abs)
                                base = FIXP_270
                                add_to_base = True
                        else:
                                # octant 8
                                quot = div(y_abs, x_abs)
                                base = FIXP_360
                                add_to_base = False

        index = fix2int(div(quot, ARCTAN_STEP_SIZE))
        lookup = arctan_table[index]

        if add_to_base:
                result = base + lookup
        else:
                result = base - lookup
        return result

FIXP_minus1 = int2fix(-1)

def negate(x):
        """
        TODO
        """
        return mul(FIXP_minus1, x)

def is_circle_circle_collision(c_1, c_2):
        """
        circ = ("circle", x, y, r): x/y = center, r = radius

        Test if distance between circle centers is smaller
        than the sum of circle radii.
        """
        c1_x = c_1[1]
        c1_y = c_1[2]
        c1_r = c_1[3]

        c2_x = c_2[1]
        c2_y = c_2[2]
        c2_r = c_2[3]

        sq_1 = c2_x - c1_x
        sq_1 = mul(sq_1, sq_1)

        sq_2 = c2_y - c1_y
        sq_2 = mul(sq_2, sq_2)

        sq_3 = c1_r + c2_r
        sq_3 = mul(sq_3, sq_3)

        return sq_3 >= (sq_1 + sq_2)

def is_rect_circle_collision(circ, rect):
        """
        circ = ("circle", x, y, r)
        rect = ("rectangle", x, y, w, h, rot)
        """
        c_x = circ[1]
        c_y = circ[2]
        c_r = circ[3]

        r_x1 = rect[1]
        r_y1 = rect[2]
        r_w = rect[3]
        r_h = rect[4]
        r_rot = rect[5]

        r_x2 = r_x1 + r_w
        r_y3 = r_y1 + r_h

        if r_rot != 0:
                rotated_circle = rotated_point((r_x1 + div(r_w, FIXP_2), r_y1 + div(r_h, FIXP_2)), (c_x, c_y), -r_rot)
                c_x = rotated_circle[0]
                c_y = rotated_circle[1]

        circle_outside = True

        corner_circles = (
                (r_y1, r_x1, c_r),
                (r_y1, r_x2, c_r),
                (r_y3, r_x1, c_r),
                (r_y3, r_x2, c_r),
        )
        circle_point = (c_y, c_x)
        for corner_circle in corner_circles:
                circle_outside = not is_point_in_circle(circle_point, corner_circle)
                if not circle_outside:
                        break

        if circle_outside:
                if ((c_x >= r_x1 and c_x <= r_x2)
                        or
                        (c_y >= r_y1 and c_y <= r_y3)
                        ):
                        circle_outside = (c_x < r_x1 - c_r or c_x > r_x2 + c_r
                                or c_y < r_y1 - c_r or c_y > r_y3 + c_r)

        return not circle_outside

def is_point_in_circle(point, circ):
        """
        point = (x, y)
        circ = (x, y, r)
        """
        c_x = circ[0]
        c_y = circ[1]
        c_r = circ[2]
        p_x = point[0]
        p_y = point[1]

        y_d = p_y - c_y
        y_d = mul(y_d, y_d)

        x_d = p_x - c_x
        x_d = mul(x_d, x_d)

        dist = y_d + x_d

        return dist <= mul(c_r, c_r)

def heading_from_to(pos1, pos2):
        """
        TODO
        """
        return atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])

def floor(x):
        """
        TODO
        """
        return int2fix(fix2int(x))
