"ocr相关，dpi识别，截图等"
from ctypes import windll
from win32gui import FindWindow, SetWindowPos, GetWindowRect
from win32con import HWND_TOPMOST, SWP_DEFERERASE, SWP_NOREPOSITION

from PIL import ImageGrab
from tesserocr import image_to_text

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

    def get_window_rect(self):
        "获取当前窗口的坐标"
        return GetWindowRect(self.handle)

    def snap_shot(self):
        "输出截图"
        # 获取yys窗口句柄
        if not self.handle:
            self.get_yys_handle()
        # 检查当前yys分辨率
        x1, y1, x2, y2 = self.get_window_rect()
        # 调整分辨率，如有必要
        if (x2 - x1) != 1533:
            self.adjust_yys_resolution()
        # 用PIL进行截图
        return ImageGrab.grab(bbox=(x1, y1, x2, y2))

class OCR:

    def __init__(self, img):
        self.image = img
        self.pix = img.load()
        self.position = 0
        self.name_rect = (829, 197, 969, 231)
        self.bottom_line_rgb = (177, 140, 120)
        if self.is_yuhun_exist():
            self.check_yuhun_position()
            bottom_y = self.get_status_bottom()
            if not bottom_y:
                raise ocrError("cannot find yuhun status bottom line")
            self.status_rect = (740, 290, 1095, bottom_y - 3)
            self.extra_rect = (740, bottom_y + 8, 1095, bottom_y + 48)
        else:
            raise ocrError("cannot find yuhun status pic")

    
    def ocr_text(self, img):
        return image_to_text(img, lang="yys")
    
    def is_yuhun_exist(self):
        if self.check_rgb(self.pix[845, 245], (239, 110, 25)) \
            and self.check_rgb(self.pix[845, 240], (113, 82, 68)) \
            and self.check_rgb(self.pix[860, 245], (228, 86, 34)):
            return True
        return False

    def check_yuhun_position(self):
        "找御魂的位置"
        check_group = [
            ((755, 199), (255, 236, 115), 1),
            ((741, 231), (255, 240, 114), 2),
            ((755, 263), (255, 235, 112), 3),
            ((820, 263), (255, 237, 112), 4),
            ((834, 231), (255, 240, 115), 5),
            ((820, 199), (255, 237, 112), 6),
            ]
        for coordinate, pattern, position in check_group:
            if self.check_rgb(self.pix[coordinate], pattern):
                self.position = position
                break
    
    def get_name_img(self):
        return self.image.crop(self.name_rect)
    
    def get_status_img(self):
        return self.image.crop(self.status_rect)
    
    def get_extra_img(self):
        return self.image.crop(self.extra_rect)

    def get_status_bottom(self):
        # 从横坐标900，纵坐标500，垂直向上找色(176, 138, 120)
        for y in range(500, 290, -1):
            if self.check_rgb(self.pix[900, y], self.bottom_line_rgb):
                return y

    @staticmethod
    def check_rgb(sample, pattern, offset=5):
        for s, p in zip(sample, pattern):
            if abs(s - p) > offset:
                return False
        return True
    
    @staticmethod
    def img_init(img):
        pix = img.load()
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                pix[x, y] = (255, 255, 255) if pix[x, y] == (203, 181, 156) else (0, 0, 0)


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
    new_img = ocr.get_status_img()
    ocr.img_init(new_img)
    new_img.show()
    status = ocr.ocr_text(new_img)
    print(ocr.position)
    print(status)
    # file_num = round(time())
    # ocr.get_extra_img().save("extra_"+str(file_num)+".bmp")

if __name__ == '__main__':
    main()