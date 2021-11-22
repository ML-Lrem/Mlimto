# 模块名：col
# 模块功能：调整色彩空间
# 功能：
#   色彩空间转换：rgb2hsv
#   二次量化色彩：getCate
#

import math


# Name：rgb2hsv
# Description: 将rgb转换为hsv
# input：
#   r,g,b：色彩rgb
# Return：
#   h,s,v：色彩hsv
#
# process：done
def rgb2hsv(rgb=None):
    r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
    h, s, v = 0, 0, 0
    mx = max(r, g, b)
    mn = min(r, g, b)
    m = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        if g >= b:
            h = ((g - b) / m) * 60
        else:
            h = ((g - b) / m) * 60 + 360
    elif mx == g:
        h = ((b - r) / m) * 60 + 120
    elif mx == b:
        h = ((r - g) / m) * 60 + 240
    if mx == 0:
        s = 0
    else:
        s = m / mx * 100
    v = mx * 100
    h = round(h/3.6)
    s = round(s)
    v = round(v)
    # 0 <= s,v <= 100，0 <= h <= 360
    return [h, s, v]


# Name：hsv2rgb
# Description: 将转换hsv为rgb
# input：
#   hsv：色彩hsv
# Return：
#   rgb：色彩rgb
#
# process：done
def hsv2rgb(hsv=None):
    h, s, v = hsv[0], hsv[1], hsv[2]
    s = s / 100
    v = v / 100
    if s == 0:
        r = g = b = v
    else:
        h = h / 60
        i = int(h)
        c = h - i
        x = v * (1 - s)
        y = v * (1 - s*c)
        z = v * (1 - s*(1-c))
        if i == 0:
            r, g, b = v, z, x
        elif i == 1:
            r, g, b = y, v, x
        elif i == 2:
            r, g, b = x, v, z
        elif i == 3:
            r, g, b = x, y, v
        elif i == 4:
            r, g, b = z, x, v
        else:
            r, g, b = v, x, y
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return [r, g, b]


# Name：getCate【待优化】
# Description: 对某一个rgb色进行分类
# input：
#   rgb：色彩的rgb值
#   SAH,SAS,SAV：量化精度，值越大，对应通道的量化精度越大
# Return：色彩的类别标签（标号）ctg
#
# process：done
def getCate(rgb=None, SAH=6, SAS=5, SAV=8):     # 6*5*8=240种颜色
    hsv = rgb2hsv(rgb)
    # 视情况调整参数【不应该是线性的】
    h_num = int(hsv[0] * SAH / 100)    # 1,2,3,4,5,6
    s_num = int(hsv[1] * SAS / 100)    # 1,2,3,4
    v_num = int(hsv[2] * SAV / 100)    # 1,2,3,4,5
    if h_num == SAH:
        h_num = SAH - 1
    if s_num == SAS:
        s_num = SAS - 1
    if v_num == SAV:
        v_num = SAV - 1
    vM = 125 * math.exp(-0.071 * hsv[1]) + 20    # 待修改
    if (hsv[2] <= vM) | (max(rgb)-min(rgb) <= 20):   # 处理灰色域、白色域
        h_num = 0
        s_num = 0
    ctg = [str(h_num), str(s_num), str(v_num)]
    ctg = ''.join(ctg)
    return ctg


# 测试用函数，ctg转如hsv, rgb
def ctgTran(ctg=None, out='rgb', SAH=6, SAS=5, SAV=8):
    degree = int(ctg[2]) / (SAV - 1)
    h = int(int(ctg[0]) * 100 / SAH + (100 / SAV) * degree)
    s = int(int(ctg[1]) * 100 / SAS)
    v = int(int(ctg[2]) * 100 / SAV + (100 / SAV) * degree)
    h = int(h * 3.6)
    if out == 'hsv':
        return [h, s, v]
    else:
        return hsv2rgb([h, s, v])

