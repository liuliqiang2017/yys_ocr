"ocr相关，dpi识别，截图等"
from ctypes import windll
from win32gui import FindWindow, SetWindowPos, GetWindowRect
from win32con import HWND_TOPMOST, SWP_DEFERERASE, SWP_NOREPOSITION

from PIL import ImageGrab

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
        return self.handle

    def adjust_yys_resolution(self):
        "调节阴阳师的分辨率，置顶"
        SetWindowPos(self.handle, HWND_TOPMOST, 0, 0, 1600, 901, SWP_DEFERERASE)

    def get_window_rect(self):
        "获取当前窗口的坐标"
        return GetWindowRect(self.handle)

    def yys_snap_shot(self):
        "输出截图"
        # 获取yys窗口句柄
        if not self.handle:
            self.get_yys_handle()
        if not self.handle:
            raise ocrError("找不到阴阳师窗口")
        # 检查当前yys分辨率
        x1, y1, x2, y2 = self.get_window_rect()
        # 调整分辨率，如有必要
        if (x2 - x1) != 1600:
            self.adjust_yys_resolution()
        # 用PIL进行截图
        return ImageGrab.grab(bbox=(x1, y1, x2, y2))