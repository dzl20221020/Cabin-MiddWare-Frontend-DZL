# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'startWindow2QKHfzI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_StartExpWindow2(object):
    def setupUi(self, StartExpWindow2):
        if not StartExpWindow2.objectName():
            StartExpWindow2.setObjectName(u"StartExpWindow2")
        StartExpWindow2.resize(1920, 1080)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(StartExpWindow2.sizePolicy().hasHeightForWidth())
        StartExpWindow2.setSizePolicy(sizePolicy)
        StartExpWindow2.setMinimumSize(QSize(1920, 1080))
        self.groupBox = QGroupBox(StartExpWindow2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(180, 60, 1621, 811))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 40, 1720, 41))
        font = QFont()
        font.setFamily(u"\u9ed1\u4f53")
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.layoutWidget = QWidget(self.groupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 770, 1601, 25))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.backBtn = QPushButton(self.layoutWidget)
        self.backBtn.setObjectName(u"backBtn")

        self.horizontalLayout_2.addWidget(self.backBtn)

        self.pushButton_3 = QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.layoutWidget1 = QWidget(self.groupBox)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 100, 1601, 661))
        self.gridLayout = QGridLayout(self.layoutWidget1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.layoutWidget1)
        self.widget_4.setObjectName(u"widget_4")
        self.label_6 = QLabel(self.widget_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(170, 290, 101, 81))
        self.naodian = QGroupBox(self.widget_4)
        self.naodian.setObjectName(u"naodian")
        self.naodian.setGeometry(QRect(10, 10, 771, 641))

        self.gridLayout.addWidget(self.widget_4, 0, 1, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cameraWidget = QWidget(self.layoutWidget1)
        self.cameraWidget.setObjectName(u"cameraWidget")
        self.groupBox_2 = QGroupBox(self.cameraWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 10, 381, 201))

        self.horizontalLayout.addWidget(self.cameraWidget)

        self.widget = QWidget(self.layoutWidget1)
        self.widget.setObjectName(u"widget")
        self.groupBox_3 = QGroupBox(self.widget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 10, 381, 201))

        self.horizontalLayout.addWidget(self.widget)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.widget_2 = QWidget(self.layoutWidget1)
        self.widget_2.setObjectName(u"widget_2")
        self.label_4 = QLabel(self.widget_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(150, 60, 101, 81))
        self.groupBox_4 = QGroupBox(self.widget_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 0, 781, 211))
        self.layoutWidget2 = QWidget(self.groupBox_4)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 20, 761, 181))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.calibraeBtn = QPushButton(self.layoutWidget2)
        self.calibraeBtn.setObjectName(u"calibraeBtn")

        self.verticalLayout_2.addWidget(self.calibraeBtn)

        self.undoView = QUndoView(self.layoutWidget2)
        self.undoView.setObjectName(u"undoView")

        self.verticalLayout_2.addWidget(self.undoView)


        self.verticalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.layoutWidget1)
        self.widget_3.setObjectName(u"widget_3")
        self.label_5 = QLabel(self.widget_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(180, 60, 101, 81))
        self.groupBox_5 = QGroupBox(self.widget_3)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(10, 0, 781, 211))

        self.verticalLayout.addWidget(self.widget_3)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.label_2 = QLabel(StartExpWindow2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(60, 170, 101, 81))

        self.retranslateUi(StartExpWindow2)

        QMetaObject.connectSlotsByName(StartExpWindow2)
    # setupUi

    def retranslateUi(self, StartExpWindow2):
        StartExpWindow2.setWindowTitle(QCoreApplication.translate("StartExpWindow2", u"Form", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("StartExpWindow2", u"\u8bbe\u5907\u4fe1\u606f\u53ca\u72b6\u6001", None))
        self.backBtn.setText(QCoreApplication.translate("StartExpWindow2", u"\u4e0a\u4e00\u6b65", None))
        self.pushButton_3.setText(QCoreApplication.translate("StartExpWindow2", u"\u4e0b\u4e00\u6b65", None))
        self.label_6.setText("")
        self.naodian.setTitle(QCoreApplication.translate("StartExpWindow2", u"\u8111\u7535", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("StartExpWindow2", u"\u6444\u50cf\u5934\u753b\u9762", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("StartExpWindow2", u"\u5fc3\u7387", None))
        self.label_4.setText("")
        self.groupBox_4.setTitle(QCoreApplication.translate("StartExpWindow2", u"\u773c\u52a8\u4eea", None))
        self.calibraeBtn.setText(QCoreApplication.translate("StartExpWindow2", u"\u6821\u51c6", None))
        self.label_5.setText("")
        self.groupBox_5.setTitle(QCoreApplication.translate("StartExpWindow2", u"\u76ae\u80a4\u7535", None))
        self.label_2.setText("")
    # retranslateUi

