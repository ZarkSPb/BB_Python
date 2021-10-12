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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(910, 774)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.WidgetControl = QWidget(self.centralwidget)
        self.WidgetControl.setObjectName(u"WidgetControl")
        self.WidgetControl.setMinimumSize(QSize(180, 0))
        self.WidgetControl.setMaximumSize(QSize(180, 16777215))
        self.verticalLayout = QVBoxLayout(self.WidgetControl)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox_3 = QGroupBox(self.WidgetControl)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.LayoutControl = QVBoxLayout(self.groupBox_3)
        self.LayoutControl.setSpacing(4)
        self.LayoutControl.setObjectName(u"LayoutControl")
        self.LayoutControl.setContentsMargins(2, 2, 2, 2)
        self.ButtonConnect = QPushButton(self.groupBox_3)
        self.ButtonConnect.setObjectName(u"ButtonConnect")

        self.LayoutControl.addWidget(self.ButtonConnect)

        self.ButtonStart = QPushButton(self.groupBox_3)
        self.ButtonStart.setObjectName(u"ButtonStart")
        self.ButtonStart.setEnabled(False)

        self.LayoutControl.addWidget(self.ButtonStart)

        self.ButtonStop = QPushButton(self.groupBox_3)
        self.ButtonStop.setObjectName(u"ButtonStop")
        self.ButtonStop.setEnabled(False)

        self.LayoutControl.addWidget(self.ButtonStop)

        self.ButtonDisconnect = QPushButton(self.groupBox_3)
        self.ButtonDisconnect.setObjectName(u"ButtonDisconnect")
        self.ButtonDisconnect.setEnabled(False)

        self.LayoutControl.addWidget(self.ButtonDisconnect)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.WidgetControl)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.LayoutImpedance = QVBoxLayout(self.groupBox_2)
        self.LayoutImpedance.setSpacing(4)
        self.LayoutImpedance.setObjectName(u"LayoutImpedance")
        self.LayoutImpedance.setContentsMargins(2, 2, 2, 2)
        self.ButtonImpedanceStart = QPushButton(self.groupBox_2)
        self.ButtonImpedanceStart.setObjectName(u"ButtonImpedanceStart")
        self.ButtonImpedanceStart.setEnabled(False)

        self.LayoutImpedance.addWidget(self.ButtonImpedanceStart)

        self.ButtonImpedanceStop = QPushButton(self.groupBox_2)
        self.ButtonImpedanceStop.setObjectName(u"ButtonImpedanceStop")
        self.ButtonImpedanceStop.setEnabled(False)

        self.LayoutImpedance.addWidget(self.ButtonImpedanceStop)

        self.LabelCh0 = QLabel(self.groupBox_2)
        self.LabelCh0.setObjectName(u"LabelCh0")

        self.LayoutImpedance.addWidget(self.LabelCh0)

        self.LabelCh1 = QLabel(self.groupBox_2)
        self.LabelCh1.setObjectName(u"LabelCh1")

        self.LayoutImpedance.addWidget(self.LabelCh1)

        self.LabelCh2 = QLabel(self.groupBox_2)
        self.LabelCh2.setObjectName(u"LabelCh2")

        self.LayoutImpedance.addWidget(self.LabelCh2)

        self.LabelCh3 = QLabel(self.groupBox_2)
        self.LabelCh3.setObjectName(u"LabelCh3")

        self.LayoutImpedance.addWidget(self.LabelCh3)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.WidgetControl)
        self.groupBox.setObjectName(u"groupBox")
        self.LayoutChartSettings = QVBoxLayout(self.groupBox)
        self.LayoutChartSettings.setSpacing(4)
        self.LayoutChartSettings.setObjectName(u"LayoutChartSettings")
        self.LayoutChartSettings.setContentsMargins(2, 2, 2, 2)
        self.LabelDuration = QLabel(self.groupBox)
        self.LabelDuration.setObjectName(u"LabelDuration")

        self.LayoutChartSettings.addWidget(self.LabelDuration)

        self.SliderDuration = QSlider(self.groupBox)
        self.SliderDuration.setObjectName(u"SliderDuration")
        self.SliderDuration.setMinimum(1)
        self.SliderDuration.setMaximum(10)
        self.SliderDuration.setValue(10)
        self.SliderDuration.setSliderPosition(10)
        self.SliderDuration.setOrientation(Qt.Horizontal)
        self.SliderDuration.setTickPosition(QSlider.TicksAbove)
        self.SliderDuration.setTickInterval(1)

        self.LayoutChartSettings.addWidget(self.SliderDuration)

        self.LabelAmplitude = QLabel(self.groupBox)
        self.LabelAmplitude.setObjectName(u"LabelAmplitude")

        self.LayoutChartSettings.addWidget(self.LabelAmplitude)

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

        self.LayoutChartSettings.addWidget(self.SliderAmplitude)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_4 = QGroupBox(self.WidgetControl)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.LayoutPatient = QVBoxLayout(self.groupBox_4)
        self.LayoutPatient.setSpacing(4)
        self.LayoutPatient.setObjectName(u"LayoutPatient")
        self.LayoutPatient.setContentsMargins(2, 2, 2, 2)
        self.label = QLabel(self.groupBox_4)
        self.label.setObjectName(u"label")

        self.LayoutPatient.addWidget(self.label)

        self.LinePatientFirstName = QLineEdit(self.groupBox_4)
        self.LinePatientFirstName.setObjectName(u"LinePatientFirstName")

        self.LayoutPatient.addWidget(self.LinePatientFirstName)

        self.label_2 = QLabel(self.groupBox_4)
        self.label_2.setObjectName(u"label_2")

        self.LayoutPatient.addWidget(self.label_2)

        self.LinePatientLastName = QLineEdit(self.groupBox_4)
        self.LinePatientLastName.setObjectName(u"LinePatientLastName")

        self.LayoutPatient.addWidget(self.LinePatientLastName)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.WidgetControl)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.LayoutSave = QVBoxLayout(self.groupBox_5)
        self.LayoutSave.setSpacing(4)
        self.LayoutSave.setObjectName(u"LayoutSave")
        self.LayoutSave.setContentsMargins(2, 2, 2, 2)
        self.CheckBoxAutosave = QCheckBox(self.groupBox_5)
        self.CheckBoxAutosave.setObjectName(u"CheckBoxAutosave")
        self.CheckBoxAutosave.setChecked(True)

        self.LayoutSave.addWidget(self.CheckBoxAutosave)

        self.CheckBoxFiltered = QCheckBox(self.groupBox_5)
        self.CheckBoxFiltered.setObjectName(u"CheckBoxFiltered")
        self.CheckBoxFiltered.setChecked(True)

        self.LayoutSave.addWidget(self.CheckBoxFiltered)

        self.ButtonSave = QPushButton(self.groupBox_5)
        self.ButtonSave.setObjectName(u"ButtonSave")
        self.ButtonSave.setEnabled(False)

        self.LayoutSave.addWidget(self.ButtonSave)


        self.verticalLayout.addWidget(self.groupBox_5)

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
        self.menubar.setGeometry(QRect(0, 0, 910, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(True)
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
        self.ButtonSave.clicked.connect(MainWindow._save_data)

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
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Patient data", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"First name:", None))
        self.LinePatientFirstName.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Last name:", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Save settings", None))
        self.CheckBoxAutosave.setText(QCoreApplication.translate("MainWindow", u"Auto save", None))
        self.CheckBoxFiltered.setText(QCoreApplication.translate("MainWindow", u"Save filtered data", None))
        self.ButtonSave.setText(QCoreApplication.translate("MainWindow", u"Save...", None))
    # retranslateUi

