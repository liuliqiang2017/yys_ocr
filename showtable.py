# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\showtable.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_showtable(object):
    def setupUi(self, showtable):
        showtable.setObjectName("showtable")
        showtable.resize(1000, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(showtable)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(showtable)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableView = QtWidgets.QTableWidget(self.widget)
        self.tableView.setBaseSize(QtCore.QSize(0, 0))
        self.tableView.setInputMethodHints(QtCore.Qt.ImhNone)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_2.addWidget(self.tableView)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(showtable)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(30, 10, 30, 10)
        self.horizontalLayout.setSpacing(80)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.insert_bt = QtWidgets.QPushButton(self.widget_2)
        self.insert_bt.setObjectName("insert_bt")
        self.horizontalLayout.addWidget(self.insert_bt)
        self.modify_bt = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modify_bt.sizePolicy().hasHeightForWidth())
        self.modify_bt.setSizePolicy(sizePolicy)
        self.modify_bt.setFlat(False)
        self.modify_bt.setObjectName("modify_bt")
        self.horizontalLayout.addWidget(self.modify_bt)
        self.back_bt = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.back_bt.sizePolicy().hasHeightForWidth())
        self.back_bt.setSizePolicy(sizePolicy)
        self.back_bt.setFlat(False)
        self.back_bt.setObjectName("back_bt")
        self.horizontalLayout.addWidget(self.back_bt)
        self.verticalLayout.addWidget(self.widget_2)
        self.verticalLayout.setStretch(0, 10)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(showtable)
        QtCore.QMetaObject.connectSlotsByName(showtable)

    def retranslateUi(self, showtable):
        _translate = QtCore.QCoreApplication.translate
        showtable.setWindowTitle(_translate("showtable", "已有御魂"))
        self.insert_bt.setText(_translate("showtable", "手动添加"))
        self.modify_bt.setText(_translate("showtable", "保存修改"))
        self.back_bt.setText(_translate("showtable", "返回"))

