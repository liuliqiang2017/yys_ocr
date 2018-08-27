# -*- coding: utf-8 -*-
# @Author: liuliqiang
# @Date:   2018-08-26 05:11:39
# @Last Modified by:   liuliqiang
# @Last Modified time: 2018-08-26 17:20:06
"test ui"
import json
import platform

from PyQt5 import QtWidgets, QtCore

from mainwindow import Ui_yuhun_ocr
from showtable import Ui_showtable

from yuhun_ocr import OCR, OCR_win7, yysWindow, ocrError


class mainWindow(QtWidgets.QMainWindow, Ui_yuhun_ocr):

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
        self.yuhun_data = []
        # 检验系统版本
        self.system = platform.uname().release
        # 完成信息
        self.show_message("系统初始化完成")
        self.show_message("系统版本为：windows-{}".format(self.system))
        # 查找yys窗口，设置缩放
        self.search_yys()

    def set_name_cb(self):
        option = ["三味", "破势", "针女", "网切", "镇墓兽", "伤魂鸟", "心眼", "狰", "轮入道"]
        self.yuhun_select.addItems(option)

    def set_position_cb(self):
        option = ["选择位置", "1号位", "2号位", "3号位", "4号位", "5号位", "6号位"]
        self.position_select.addItems(option)
    
    def set_amplify_cb(self):
        option = ["正常", "十倍", "百倍", "千倍", "万倍"]
        self.amplify_ratio.addItems(option)

    def set_trigger(self):
        self.bt_1.clicked.connect(self.load_data_from_json)
        self.bt_2.clicked.connect(self.save_data_to_json)
        self.bt_3.clicked.connect(self.search_yys)
        self.bt_4.clicked.connect(self.release_yys)
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
        # 获取游戏界面截图,并根据系统不同，采用不同的ocr装载
        try:
            ocr = OCR(self.yys.snap_shot()) if self.system == "10" else OCR_win7(self.yys.snap_shot())
        except ocrError:
            self.show_message("识别失败，请确认正确显示御魂信息")
        # 识别御魂属性
        yuhun_name = self.yuhun_select.currentText()
        yuhun_position = self.position_select.currentIndex()
        if yuhun_position == 0:
            yuhun_position = ocr.position
        try:
            yuhun_status = ocr.parse_status_data(ocr.get_status_text())
        except ocrError:
            return self.show_message("识别失败，请确认正确显示御魂信息")
        self.show_message("-" * 10)
        self.show_message("御魂识别:")
        self.show_message("{}号位{}".format(yuhun_position, yuhun_name))
        for name, num in zip(*yuhun_status):
            self.show_message(name + ":" + num)
        self.show_message("-" * 10)
        # 生成御魂数据，入库
        yh = self.create_yuhun(yuhun_name, yuhun_position, yuhun_status)
        self.yuhun_data.append(yh)

    def create_yuhun(self, yh_name, yh_position, yh_status):
        """
        存储御魂数据，御魂数据由列表构成，按顺序为种类，位置，攻击，攻击加成，防御，防御加成，生命，生命加成
        ，暴击，暴击伤害，速度，效果命中，效果抵抗，共计 13位
        """
        pattern = [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        RATIO = 10 ** self.amplify_ratio.currentIndex()
        COUPLE = {"攻击": 2, "攻击加成": 3, "防御": 4, "防御加成": 5, "生命": 6, "生命加成": 7, 
                    "暴击": 8, "暴击伤害": 9, "速度": 10, "效果命中": 11, "效果抵抗": 12}
        
        # 属性录入
        for name, num in zip(*yh_status):
            if name in COUPLE:
                ratio = RATIO
                if num.endswith("%"):
                    ratio *= 100
                    num = num[:-1]
                real_num = int(num) / ratio
                pattern[COUPLE[name]] += real_num
        
        # 名称，位置录入
        pattern[0] = yh_name
        pattern[1] = yh_position

        return pattern
        

    def show_message(self, msg):
        self.textBrowser.append(msg)

    def save_data_to_json(self):
        "把所有yuhun的data数据保存到json文件"

        # 弹出窗口要求用户选择存储位置
        fileName = QtWidgets.QFileDialog.getSaveFileName(None,
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
        fileName = QtWidgets.QFileDialog.getOpenFileName(None,
                                             r'创建御魂信息并保存',
                                             r'yuhun_data',
                                             r'JSON Files(*.json)')
        with open(fileName[0], "r") as f_obj:
            try:
                data = json.load(f_obj)
            except json.decoder.JSONDecodeError:
                self.show_message("读取御魂信息失败，数据损坏")
                return

        if isinstance(data, list) and len(data[0]) == 13:
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
    
    def release_yys(self):
        if self.yys:
            self.yys.release_yys_topmost()


class showTable(QtWidgets.QDialog, Ui_showtable):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        super().setupUi(self)
        # 初始化表格
        self.init_table()
        # 设置触发
        self.set_trigger()
        # 加载表格
        self.load_table()
        self.show()

    def init_table(self):
        # 表头
        header = ["类别", "位置", "攻击", "攻击加成", "防御", "防御加成", "生命", "生命加成",
        "暴击", "暴击伤害", "速度", "效果命中", "效果抵抗"]
        self.tableView.setColumnCount(13)
        self.tableView.setRowCount(0)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        for i, name in enumerate(header):
            item = QtWidgets.QTableWidgetItem()
            item.setText(name)
            self.tableView.setHorizontalHeaderItem(i, item)
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def load_table(self):
        for yuhun in self.parent.yuhun_data:
            self.add_new_line(yuhun)

    def set_trigger(self):
        # self.insert_bt.clicked.connect(self.add_new_line)
        self.modify_bt.clicked.connect(self.save_table)
        self.back_bt.clicked.connect(self.reject)

    def add_new_line(self, yh_data):
        row = self.tableView.rowCount()
        self.tableView.setRowCount(row + 1)
        for col, data in enumerate(yh_data):
            newItem = QtWidgets.QTableWidgetItem(str(data))
            newItem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableView.setItem(row, col, newItem)

    def save_table(self):
        pass

def main():
    import sys
    import cgitb
    cgitb.enable(format='text')
    app = QtWidgets.QApplication(sys.argv)
    widget = mainWindow()
    widget.show()
    run = app.exec_()
    sys.exit(run)


if __name__ == "__main__":
    main()