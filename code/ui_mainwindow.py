# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect, QSize, QTime,
                            QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QGradient, QIcon, QImage,
                           QKeySequence, QLinearGradient, QPainter, QPalette,
                           QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow,
                               QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
                               QStatusBar, QVBoxLayout, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ButtonConnect = QPushButton(self.centralwidget)
        self.ButtonConnect.setObjectName(u"ButtonConnect")

        self.verticalLayout.addWidget(self.ButtonConnect)

        self.ButtonStart = QPushButton(self.centralwidget)
        self.ButtonStart.setObjectName(u"ButtonStart")
        self.ButtonStart.setEnabled(False)

        self.verticalLayout.addWidget(self.ButtonStart)

        self.ButtonStop = QPushButton(self.centralwidget)
        self.ButtonStop.setObjectName(u"ButtonStop")
        self.ButtonStop.setEnabled(False)

        self.verticalLayout.addWidget(self.ButtonStop)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum,
                                          QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 166, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.ButtonConnect.setText(
            QCoreApplication.translate("MainWindow", u"Connect", None))
        self.ButtonStart.setText(
            QCoreApplication.translate("MainWindow", u"Start", None))
        self.ButtonStop.setText(
            QCoreApplication.translate("MainWindow", u"Stop", None))

    # retranslateUi