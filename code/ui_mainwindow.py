# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QLabel,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1500, 1000)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.WidgetControl = QWidget(self.centralwidget)
        self.WidgetControl.setObjectName(u"WidgetControl")
        self.WidgetControl.setMinimumSize(QSize(180, 0))
        self.WidgetControl.setMaximumSize(QSize(180, 16777215))
        self.verticalLayout = QVBoxLayout(self.WidgetControl)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.ButtonConnect = QPushButton(self.WidgetControl)
        self.ButtonConnect.setObjectName(u"ButtonConnect")

        self.verticalLayout.addWidget(self.ButtonConnect)

        self.ButtonStart = QPushButton(self.WidgetControl)
        self.ButtonStart.setObjectName(u"ButtonStart")
        self.ButtonStart.setEnabled(False)

        self.verticalLayout.addWidget(self.ButtonStart)

        self.ButtonStop = QPushButton(self.WidgetControl)
        self.ButtonStop.setObjectName(u"ButtonStop")
        self.ButtonStop.setEnabled(False)

        self.verticalLayout.addWidget(self.ButtonStop)

        self.ButtonDisconnect = QPushButton(self.WidgetControl)
        self.ButtonDisconnect.setObjectName(u"ButtonDisconnect")
        self.ButtonDisconnect.setEnabled(False)

        self.verticalLayout.addWidget(self.ButtonDisconnect)

        self.groupBox = QGroupBox(self.WidgetControl)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.LabelDuration = QLabel(self.groupBox)
        self.LabelDuration.setObjectName(u"LabelDuration")

        self.verticalLayout_2.addWidget(self.LabelDuration)

        self.SliderDuration = QSlider(self.groupBox)
        self.SliderDuration.setObjectName(u"SliderDuration")
        self.SliderDuration.setMinimum(1)
        self.SliderDuration.setMaximum(10)
        self.SliderDuration.setValue(10)
        self.SliderDuration.setSliderPosition(10)
        self.SliderDuration.setOrientation(Qt.Horizontal)
        self.SliderDuration.setTickPosition(QSlider.TicksAbove)
        self.SliderDuration.setTickInterval(1)

        self.verticalLayout_2.addWidget(self.SliderDuration)

        self.LabelAmplitude = QLabel(self.groupBox)
        self.LabelAmplitude.setObjectName(u"LabelAmplitude")

        self.verticalLayout_2.addWidget(self.LabelAmplitude)

        self.SliderAmplitude = QSlider(self.groupBox)
        self.SliderAmplitude.setObjectName(u"SliderAmplitude")
        self.SliderAmplitude.setMinimum(50)
        self.SliderAmplitude.setMaximum(50000)
        self.SliderAmplitude.setOrientation(Qt.Horizontal)
        self.SliderAmplitude.setInvertedAppearance(False)
        self.SliderAmplitude.setInvertedControls(False)
        self.SliderAmplitude.setTickPosition(QSlider.TicksAbove)
        self.SliderAmplitude.setTickInterval(100)

        self.verticalLayout_2.addWidget(self.SliderAmplitude)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 269, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout.addWidget(self.WidgetControl, 0, 0, 1, 1)

        self.WidgetCharts = QWidget(self.centralwidget)
        self.WidgetCharts.setObjectName(u"WidgetCharts")
        self.WidgetCharts.setToolTipDuration(-1)
        self.verticalLayout_3 = QVBoxLayout(self.WidgetCharts)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.gridLayout.addWidget(self.WidgetCharts, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1500, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.ButtonConnect, self.ButtonStart)
        QWidget.setTabOrder(self.ButtonStart, self.ButtonStop)
        QWidget.setTabOrder(self.ButtonStop, self.ButtonDisconnect)
        QWidget.setTabOrder(self.ButtonDisconnect, self.SliderDuration)
        QWidget.setTabOrder(self.SliderDuration, self.SliderAmplitude)

        self.retranslateUi(MainWindow)
        self.SliderDuration.valueChanged.connect(MainWindow.update)
        self.SliderAmplitude.valueChanged.connect(MainWindow.update)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.ButtonConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.ButtonStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.ButtonStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.ButtonDisconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Chart settings", None))
        self.LabelDuration.setText(QCoreApplication.translate("MainWindow", u"Duration (sec): 1", None))
        self.LabelAmplitude.setText(QCoreApplication.translate("MainWindow", u"Amplitude (uV): 50", None))
    # retranslateUi

