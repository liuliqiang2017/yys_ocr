# -*- coding: utf-8 -*-
# @Author: liuliqiang
# @Date:   2018-08-26 05:11:39
# @Last Modified by:   liuliqiang
# @Last Modified time: 2018-08-26 17:20:06
"test ui"
import json

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from mainwindow import Ui_yuhun_ocr
from showtable import Ui_showtable

from yuhun_ocr import OCR, yysWindow, ocrError


class mainWindow(QMainWindow, Ui_yuhun_ocr):

    def __init__(self):
        super().__init__(None)
        self.setupUi(self)
        self.set_name_cb()
        self.set_position_cb()
        self.set_amplify_cb()
        # 设置触发事件
        self.set_trigger()
        # 一些存储用的变量
        self.yys = None
        self.yuhun_data = [[], [], [], [], [], []]
        # 完成信息
        self.show_message("系统初始化完成")
        # 查找yys窗口，设置缩放
        self.search_yys()

    def set_name_cb(self):
        option = ["三味", "破势", "针女", "网切", "镇墓兽", "伤魂鸟", "心眼", "狰", "轮入道"]
        self.yuhun_select.addItems(option)

    def set_position_cb(self):
        option = ["自动识别", "1号位", "2号位", "3号位", "4号位", "5号位", "6号位"]
        self.position_select.addItems(option)
    
    def set_amplify_cb(self):
        option = ["正常", "十倍", "百倍", "千倍", "万倍"]
        self.amplify_ratio.addItems(option)

    def set_trigger(self):
        self.bt_1.clicked.connect(self.load_data_from_json)
        self.bt_2.clicked.connect(self.save_data_to_json)
        self.bt_3.clicked.connect(self.search_yys)
        self.ocr_bt.clicked.connect(self.ocr_yuhun)
        self.inquire_bt.clicked.connect(self.show_yuhun_table)

    def show_yuhun_table(self):
        show_table = showTable(self)
        show_table.exec_()

    def ocr_yuhun(self):
        # 检测是否已经识别yys客户端
        if not self.yys:
            self.search_yys()
        if not self.yys: return
        # 获取游戏界面截图
        ocr = OCR(self.yys.snap_shot())
        # 识别御魂属性
        self.show_message("御魂识别:")
        yuhun_status = ocr.parse_status_data(ocr.get_status_text())
        for name, num in zip(*yuhun_status):
            self.show_message(name + ":" + num)


    def show_message(self, msg):
        self.textBrowser.append(msg)

    def save_data_to_json(self):
        "把所有yuhun的data数据保存到json文件"

        # 弹出窗口要求用户选择存储位置
        fileName = QFileDialog.getSaveFileName(None,
                                             r'保存御魂信息',
                                             r'yuhun_data',
                                             r'JSON Files(*.json)')
        # 保存文件，默认文件名yys_teamdata.json
        with open(fileName[0], "w") as f_obj:
            json.dump(self.yuhun_data, f_obj)

        self.show_message("保存御魂信息成功")

    def load_data_from_json(self):
        "读取数据"
        # 弹出窗口要求用户选择文件
        fileName = QFileDialog.getOpenFileName(None,
                                             r'创建御魂信息并保存',
                                             r'yuhun_data',
                                             r'JSON Files(*.json)')
        with open(fileName[0], "r") as f_obj:
            try:
                data = json.load(f_obj)
            except json.decoder.JSONDecodeError:
                self.show_message("读取御魂信息失败，数据损坏")
                return

        if len(data) == 6:
            # 读取json，覆盖本身的data
            self.yuhun_data = data
            self.show_message("读取御魂信息成功")
        else:
            self.show_message("读取御魂信息失败，数据损坏")
    
    def search_yys(self):
        try:
            self.yys = yysWindow()
            self.yys.adjust_yys_resolution()
            self.show_message("找到阴阳师窗口\n设置分辨率为1533x900\n设置阴阳师窗口置顶")
        except ocrError:
            self.show_message("未找到阴阳师窗口")


class showTable(QDialog, Ui_showtable):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        super().setupUi(self)
        # 设置触发
        self.set_trigger()
        # 加载表格
        self.load_table()
        self.show()

    def load_table(self):
        pass

    def set_trigger(self):
        self.insert_bt.clicked.connect(self.add_new_line)
        self.modify_bt.clicked.connect(self.save_table)
        self.back_bt.clicked.connect(self.reject)

    def add_new_line(self):
        pass

    def save_table(self):
        pass


if __name__ == "__main__":
    import sys
    import cgitb
    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    widget = mainWindow()
    widget.show()
    sys.exit(app.exec_())
