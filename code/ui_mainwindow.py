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
        MainWindow.resize(1039, 835)
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
        self.groupBox_3 = QGroupBox(self.WidgetControl)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.ButtonConnect = QPushButton(self.groupBox_3)
        self.ButtonConnect.setObjectName(u"ButtonConnect")

        self.verticalLayout_3.addWidget(self.ButtonConnect)

        self.ButtonStart = QPushButton(self.groupBox_3)
        self.ButtonStart.setObjectName(u"ButtonStart")
        self.ButtonStart.setEnabled(False)

        self.verticalLayout_3.addWidget(self.ButtonStart)

        self.ButtonStop = QPushButton(self.groupBox_3)
        self.ButtonStop.setObjectName(u"ButtonStop")
        self.ButtonStop.setEnabled(False)

        self.verticalLayout_3.addWidget(self.ButtonStop)

        self.ButtonDisconnect = QPushButton(self.groupBox_3)
        self.ButtonDisconnect.setObjectName(u"ButtonDisconnect")
        self.ButtonDisconnect.setEnabled(False)

        self.verticalLayout_3.addWidget(self.ButtonDisconnect)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.WidgetControl)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.ButtonImpedanceStart = QPushButton(self.groupBox_2)
        self.ButtonImpedanceStart.setObjectName(u"ButtonImpedanceStart")
        self.ButtonImpedanceStart.setEnabled(False)

        self.verticalLayout_4.addWidget(self.ButtonImpedanceStart)

        self.ButtonImpedanceStop = QPushButton(self.groupBox_2)
        self.ButtonImpedanceStop.setObjectName(u"ButtonImpedanceStop")
        self.ButtonImpedanceStop.setEnabled(False)

        self.verticalLayout_4.addWidget(self.ButtonImpedanceStop)

        self.LabelCh0 = QLabel(self.groupBox_2)
        self.LabelCh0.setObjectName(u"LabelCh0")

        self.verticalLayout_4.addWidget(self.LabelCh0)

        self.LabelCh1 = QLabel(self.groupBox_2)
        self.LabelCh1.setObjectName(u"LabelCh1")

        self.verticalLayout_4.addWidget(self.LabelCh1)

        self.LabelCh2 = QLabel(self.groupBox_2)
        self.LabelCh2.setObjectName(u"LabelCh2")

        self.verticalLayout_4.addWidget(self.LabelCh2)

        self.LabelCh3 = QLabel(self.groupBox_2)
        self.LabelCh3.setObjectName(u"LabelCh3")

        self.verticalLayout_4.addWidget(self.LabelCh3)


        self.verticalLayout.addWidget(self.groupBox_2)

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
        self.SliderAmplitude.setMinimum(20)
        self.SliderAmplitude.setMaximum(200)
        self.SliderAmplitude.setSingleStep(5)
        self.SliderAmplitude.setPageStep(20)
        self.SliderAmplitude.setValue(20)
        self.SliderAmplitude.setOrientation(Qt.Horizontal)
        self.SliderAmplitude.setInvertedAppearance(False)
        self.SliderAmplitude.setInvertedControls(False)
        self.SliderAmplitude.setTickPosition(QSlider.TicksAbove)
        self.SliderAmplitude.setTickInterval(5)

        self.verticalLayout_2.addWidget(self.SliderAmplitude)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 269, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout.addWidget(self.WidgetControl, 0, 0, 1, 1)

        self.WidgetCharts = QWidget(self.centralwidget)
        self.WidgetCharts.setObjectName(u"WidgetCharts")
        self.WidgetCharts.setToolTipDuration(-1)
        self.LayoutCharts = QVBoxLayout(self.WidgetCharts)
        self.LayoutCharts.setSpacing(0)
        self.LayoutCharts.setObjectName(u"LayoutCharts")
        self.LayoutCharts.setContentsMargins(0, 0, 0, 0)

        self.gridLayout.addWidget(self.WidgetCharts, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1039, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.SliderDuration, self.SliderAmplitude)

        self.retranslateUi(MainWindow)
        self.SliderDuration.valueChanged.connect(MainWindow.update_ui)
        self.SliderAmplitude.valueChanged.connect(MainWindow.update_ui)
        self.ButtonConnect.clicked.connect(MainWindow._connect)
        self.ButtonStart.clicked.connect(MainWindow._start_capture)
        self.ButtonStop.clicked.connect(MainWindow._stop_capture)
        self.ButtonDisconnect.clicked.connect(MainWindow._disconnect)
        self.ButtonImpedanceStart.clicked.connect(MainWindow._start_impedance)
        self.ButtonImpedanceStop.clicked.connect(MainWindow._stop_impedance)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"BrainBit", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"BrainBit control", None))
        self.ButtonConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.ButtonStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.ButtonStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.ButtonDisconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Impedance", None))
        self.ButtonImpedanceStart.setText(QCoreApplication.translate("MainWindow", u"Start impedance", None))
        self.ButtonImpedanceStop.setText(QCoreApplication.translate("MainWindow", u"Stop impedance", None))
        self.LabelCh0.setText(QCoreApplication.translate("MainWindow", u"T3 (Ohm):", None))
        self.LabelCh1.setText(QCoreApplication.translate("MainWindow", u"T4 (Ohm):", None))
        self.LabelCh2.setText(QCoreApplication.translate("MainWindow", u"O1 (Ohm):", None))
        self.LabelCh3.setText(QCoreApplication.translate("MainWindow", u"O2 (Ohm):", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Chart settings", None))
        self.LabelDuration.setText(QCoreApplication.translate("MainWindow", u"Duration (sec): 1", None))
        self.LabelAmplitude.setText(QCoreApplication.translate("MainWindow", u"Amplitude (uV): 20", None))
    # retranslateUi

