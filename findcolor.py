"findcolor"

# 判断颜色是否符合样板
def check_color(pattern, color, f=10):
    if abs(pattern[0]-color[0]) <= f:
        if abs(pattern[1]-color[1]) <= f:
            if abs(pattern[2]-color[2]) <= f:
                return True
    return False

# 将十六进制转换为rgb元组
def to_rgb(hex_num):
    'turn the input num to rgb mode'
    if isinstance(hex_num, int):
        s = hex(hex_num).lstrip('0x')
    elif isinstance(hex_num, str):
        s = hex_num.lstrip('0x')
    else:
        raise TypeError('only hex or str')
    r = slice(0, 2)
    g = slice(2, 4)
    b = slice(4, 6)
    return (int(s[r], 16), int(s[g], 16), int(s[b], 16))

def check_rgb(sample, pattern, offset=5):
    "单点对比颜色"
    for s, p in zip(sample, pattern):
        if abs(s - p) > offset:
            return False
    return True

# 多点找色
def find_mul_colors(pattern, x1, y1, x2, y2, others, pix_data, mode=(0, 0)):
    """
    多点找色，根据xx助手的数据开发
    """
    enum_hor = range(x1, x2+1) if mode[0] == 0 else range(x2, x1-1, -1)
    enum_ver = range(y1, y2+1) if mode[1] == 0 else range(y2, y1-1, -1)

    for x in enum_hor:
        for y in enum_ver:
            if check_rgb(pix_data[x, y], pattern):
                for other in others:
                    try:
                        if not check_rgb(pix_data[x+other[1], y+other[2]],other[0]):
                            break
                    except IndexError:
                        break
                else:
                    return x, y
    return -1, -1
    

# 从叉叉生成的代码转换到python
# 0x242424,"-8|-6|0xffffff,11|-9|0xffffff,-8|7|0xffffff,11|10|0xffffff", 100, 7, 1025, 59, 1083
def translate(code):

    def tran_other(other):
        other = other.strip('"')
        ele = other.split('|')
        return (to_rgb(ele[2]), int(ele[0]), int(ele[1]))

    code_l = code.split(',')
    others_l = code_l[1:-5]

    res = dict(pattern=to_rgb(code_l[0]),
               x1=int(code_l[-4]),
               x2=int(code_l[-2]),
               y1=int(code_l[-3]),
               y2=int(code_l[-1]),
               others=tuple([tran_other(other) for other in others_l]))
    return  res

