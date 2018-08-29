"ocr相关，dpi识别，截图等"
from os import getcwd
from ctypes import windll
from win32gui import FindWindow, SetWindowPos, GetWindowRect
from win32con import HWND_TOPMOST, HWND_TOP, SWP_DEFERERASE, SWP_NOREPOSITION

from PIL import ImageGrab
from tesserocr import image_to_text

from findcolor import translate, find_mul_colors

class ocrError(Exception):
    pass

class yysWindow:

    def __init__(self):
        self.handle = 0
        self.set_dpi()
        self.get_yys_handle()


    def set_dpi(self):
        "设置系统的缩放信息dpi"
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

    def get_yys_handle(self):
        "获取阴阳师的窗口句柄"
        self.handle = FindWindow(None, "阴阳师-网易游戏")
        if not self.handle:
            raise ocrError("cannot find yys window")
        return self.handle

    def adjust_yys_resolution(self):
        "调节阴阳师的分辨率，置顶"
        SetWindowPos(self.handle, HWND_TOPMOST, 0, 0, 1533, 901, SWP_DEFERERASE|SWP_NOREPOSITION)
    
    def release_yys_topmost(self):
        x, y, _, _ = self.get_window_rect()
        SetWindowPos(self.handle, HWND_TOP, x, y, 1533, 901, SWP_DEFERERASE|SWP_NOREPOSITION)

    def get_window_rect(self):
        "获取当前窗口的坐标"
        return GetWindowRect(self.handle)

    def snap_shot(self):
        "输出截图"
        # 获取yys窗口句柄
        if not self.handle:
            self.get_yys_handle()
        # 检查当前yys分辨率
        _, y1, _, y2 = self.get_window_rect()
        # 调整分辨率，如有必要
        if (y2 - y1) != 901:
            self.adjust_yys_resolution()
        # 用PIL进行截图
        return ImageGrab.grab(bbox=self.get_window_rect())

class OCR:

    def __init__(self, img):
        self.image = img
        self.pix = img.load()
        self.path = getcwd()
        self.position = 0
        self.calculate_rect()

    def calculate_rect(self):
        if self.is_yuhun_exist():
            self.status_rect = self.cal_status_rect()
            self.extra_rect = self.cal_extra_rect()
            self.name_rect = self.cal_name_rect()
            self.check_yuhun_position()
        else:
            raise ocrError("cannot find yuhun status pic")
    
    def cal_name_rect(self):
        x, y = find_mul_colors(pix_data=self.pix, **FindColorCode.gouyu)
        return  x - 16, y - 46, x + 123, y - 10
    
    def cal_status_rect(self):
        # 计算四个边的坐标
        x1, _ = find_mul_colors(pix_data=self.pix, **FindColorCode.status_left, mode=(1, 0))
        x2, _ = find_mul_colors(pix_data=self.pix, **FindColorCode.status_right)
        _, y1 = find_mul_colors(pix_data=self.pix, **FindColorCode.status_up, mode=(0, 1))
        _, y2 = find_mul_colors(pix_data=self.pix, **FindColorCode.status_down)
        
        if x1 > -1 and x2 > -1 and y1 > -1 and y2 > -1:
            return x1, y1, x2, y2
        return 740, 283, 1100, 485
    
    def cal_extra_rect(self):
        return self.status_rect[0], self.status_rect[3], self.status_rect[2], self.status_rect[3] + 48
    
    def check_yuhun_position(self):
        "找御魂的位置"
        for i, code in enumerate(FindColorCode.position, 1):
            if find_mul_colors(pix_data=self.pix, **code)[0] > -1:
                self.position = i
                return
    
    def ocr_text(self, img):
        return image_to_text(img, lang="yys", psm=6, path=self.path)

    def is_yuhun_exist(self):
        x, _ = find_mul_colors(pix_data=self.pix, **FindColorCode.exist_code)
        return True if x > -1 else False

    
    def get_name_img(self):
        return self.image.crop(self.name_rect)
    
    def get_name_text(self):
        pass
    
    def get_status_img(self):
        return self.image.crop(self.status_rect)
    
    def get_status_text(self):
        raw = self.ocr_text(self.get_status_img())
        return self.parse_raw_text(raw)

    def parse_raw_text(self, raw):
        res = []
        for char in raw:
            if char == " ": continue
            if char == "中" and res[-1] != "命": char = "+"
            res.append(char)
        return "".join(res)
    
    def parse_status_data(self, string):

        def put_in(res, temp):
            if temp:
                res.append("".join(temp))
                temp.clear()
    
        name = []
        number = []
        name_temp = []
        number_temp = []
        num_pattern = "0123456789%"
        for char in string:
            if char == "\n" or char == "+":
                put_in(name, name_temp)
                put_in(number, number_temp)
            elif char in num_pattern:
                number_temp.append(char)
            else:
                name_temp.append(char)
        if (name and number) and (len(name) == len(number)):
            return name, number
        else:
            raise ocrError("not correct data")

    def get_extra_img(self):
        return self.image.crop(self.extra_rect)


    @staticmethod
    def check_rgb(sample, pattern, offset=5):
        for s, p in zip(sample, pattern):
            if abs(s - p) > offset:
                return False
        return True

class FindColorCode:

    exist_code = translate('0xcbb59c,"-2|-15|0xcbb59c,-1|-33|0xcbb59c", 95, 871, 348, 900, 382')
    status_left = translate('0x6a523e,"-1|0|0x412711,-2|0|0x533a1b,8|3|0xc6b097", 95, 678, 373, 791, 418')
    status_right = translate('0x78614c,"1|0|0x3e240f,2|0|0x50371a,-11|-1|0xcbb59c", 95, 1046, 353, 1183, 397')
    status_up = translate('0xb6937f,"4|-3|0xaf8977,4|-5|0xbb9b86,6|-6|0xcbb59c", 95, 902, 257, 927, 303')
    status_down = translate('0xba9b86,"1|2|0xb08a77,5|5|0xb69480,8|6|0xcbb59c", 95, 899, 316, 959, 503')
    position = [
        translate('0x21130d,"2|2|0xfffb7c,-2|-2|0xff9449,4|4|0xfff173", 95, 742, 172, 769, 199'),
        translate('0x1f110e,"-3|0|0xff833a,4|0|0xfff979", 95, 725, 166, 859, 284'),
        translate('0x130a09,"2|-2|0xfffb7c,-2|2|0xff9249", 95, 725, 166, 859, 284'),
        translate('0x25160e,"-2|-2|0xfffb7c,2|2|0xffa358", 95, 725, 166, 859, 284'),
        translate('0x190e0c,"-3|0|0xfffb7c,3|0|0xff9047", 95, 725, 166, 859, 284'),
        translate('0x26160e,"-2|2|0xfffb7c,2|-2|0xff9f54", 95, 725, 166, 859, 284')
    ]
    gouyu = translate('0x8d7d71,"-3|3|0xdd4a27,3|3|0xf36739,0|-4|0xff5f4e", 95, 822, 216, 965, 265')

def main():
    "测试模块"
    # from time import time
    # 获取yys句柄
    yys = yysWindow()
    hw = yys.get_yys_handle()
    print("yys的窗口句柄是", hw)
    # 截图并显示
    img = yys.snap_shot()
    # 移交ocr处理文字
    ocr = OCR(img)
    # new_img = ocr.get_status_img()
    # ocr.img_init(new_img)
    # new_img.show()
    status = ocr.get_status_text()
    print(ocr.position)
    print(status)
    # file_num = round(time())
    # ocr.get_extra_img().save("extra_"+str(file_num)+".bmp")

if __name__ == '__main__':
    main()