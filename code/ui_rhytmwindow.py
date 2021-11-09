# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rhytmwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGridLayout,
    QGroupBox, QLabel, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_RhytmWindow(object):
    def setupUi(self, RhytmWindow):
        if not RhytmWindow.objectName():
            RhytmWindow.setObjectName(u"RhytmWindow")
        RhytmWindow.resize(1014, 444)
        self.formLayout = QFormLayout(RhytmWindow)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(4)
        self.formLayout.setVerticalSpacing(4)
        self.formLayout.setContentsMargins(4, 4, 4, 4)
        self.WidgetControl = QWidget(RhytmWindow)
        self.WidgetControl.setObjectName(u"WidgetControl")
        self.WidgetControl.setMinimumSize(QSize(150, 0))
        self.WidgetControl.setMaximumSize(QSize(150, 16777215))
        self.verticalLayout = QVBoxLayout(self.WidgetControl)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox_3 = QGroupBox(self.WidgetControl)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.ButtonStart = QPushButton(self.groupBox_3)
        self.ButtonStart.setObjectName(u"ButtonStart")

        self.verticalLayout_2.addWidget(self.ButtonStart)

        self.ButtonPause = QPushButton(self.groupBox_3)
        self.ButtonPause.setObjectName(u"ButtonPause")
        self.ButtonPause.setEnabled(False)

        self.verticalLayout_2.addWidget(self.ButtonPause)

        self.ButtonResume = QPushButton(self.groupBox_3)
        self.ButtonResume.setObjectName(u"ButtonResume")
        self.ButtonResume.setEnabled(False)

        self.verticalLayout_2.addWidget(self.ButtonResume)

        self.ButtonStop = QPushButton(self.groupBox_3)
        self.ButtonStop.setObjectName(u"ButtonStop")
        self.ButtonStop.setEnabled(False)

        self.verticalLayout_2.addWidget(self.ButtonStop)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox = QGroupBox(self.WidgetControl)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.SpinBox2_2 = QSpinBox(self.groupBox)
        self.SpinBox2_2.setObjectName(u"SpinBox2_2")
        self.SpinBox2_2.setMinimum(1)
        self.SpinBox2_2.setMaximum(100)
        self.SpinBox2_2.setValue(8)

        self.gridLayout.addWidget(self.SpinBox2_2, 1, 2, 1, 1)

        self.SpinBox3_2 = QSpinBox(self.groupBox)
        self.SpinBox3_2.setObjectName(u"SpinBox3_2")
        self.SpinBox3_2.setMinimum(1)
        self.SpinBox3_2.setMaximum(100)
        self.SpinBox3_2.setValue(13)

        self.gridLayout.addWidget(self.SpinBox3_2, 2, 2, 1, 1)

        self.SpinBox4_1 = QSpinBox(self.groupBox)
        self.SpinBox4_1.setObjectName(u"SpinBox4_1")
        self.SpinBox4_1.setMinimum(1)
        self.SpinBox4_1.setMaximum(100)
        self.SpinBox4_1.setValue(13)

        self.gridLayout.addWidget(self.SpinBox4_1, 3, 1, 1, 1)

        self.CheckBox5 = QCheckBox(self.groupBox)
        self.CheckBox5.setObjectName(u"CheckBox5")
        self.CheckBox5.setChecked(True)

        self.gridLayout.addWidget(self.CheckBox5, 4, 0, 1, 1)

        self.SpinBox1_2 = QSpinBox(self.groupBox)
        self.SpinBox1_2.setObjectName(u"SpinBox1_2")
        self.SpinBox1_2.setMinimum(1)
        self.SpinBox1_2.setMaximum(100)
        self.SpinBox1_2.setValue(4)

        self.gridLayout.addWidget(self.SpinBox1_2, 0, 2, 1, 1)

        self.CheckBox2 = QCheckBox(self.groupBox)
        self.CheckBox2.setObjectName(u"CheckBox2")
        self.CheckBox2.setChecked(True)

        self.gridLayout.addWidget(self.CheckBox2, 1, 0, 1, 1)

        self.CheckBox4 = QCheckBox(self.groupBox)
        self.CheckBox4.setObjectName(u"CheckBox4")
        self.CheckBox4.setChecked(True)

        self.gridLayout.addWidget(self.CheckBox4, 3, 0, 1, 1)

        self.CheckBox3 = QCheckBox(self.groupBox)
        self.CheckBox3.setObjectName(u"CheckBox3")
        self.CheckBox3.setChecked(True)

        self.gridLayout.addWidget(self.CheckBox3, 2, 0, 1, 1)

        self.SpinBox5_1 = QSpinBox(self.groupBox)
        self.SpinBox5_1.setObjectName(u"SpinBox5_1")
        self.SpinBox5_1.setMinimum(1)
        self.SpinBox5_1.setMaximum(100)
        self.SpinBox5_1.setValue(40)

        self.gridLayout.addWidget(self.SpinBox5_1, 4, 1, 1, 1)

        self.SpinBox5_2 = QSpinBox(self.groupBox)
        self.SpinBox5_2.setObjectName(u"SpinBox5_2")
        self.SpinBox5_2.setMinimum(1)
        self.SpinBox5_2.setMaximum(100)
        self.SpinBox5_2.setValue(48)

        self.gridLayout.addWidget(self.SpinBox5_2, 4, 2, 1, 1)

        self.SpinBox3_1 = QSpinBox(self.groupBox)
        self.SpinBox3_1.setObjectName(u"SpinBox3_1")
        self.SpinBox3_1.setMinimum(1)
        self.SpinBox3_1.setMaximum(100)
        self.SpinBox3_1.setValue(8)

        self.gridLayout.addWidget(self.SpinBox3_1, 2, 1, 1, 1)

        self.ButtonReset = QPushButton(self.groupBox)
        self.ButtonReset.setObjectName(u"ButtonReset")

        self.gridLayout.addWidget(self.ButtonReset, 5, 0, 1, 3)

        self.SpinBox4_2 = QSpinBox(self.groupBox)
        self.SpinBox4_2.setObjectName(u"SpinBox4_2")
        self.SpinBox4_2.setMinimum(1)
        self.SpinBox4_2.setMaximum(100)
        self.SpinBox4_2.setValue(40)

        self.gridLayout.addWidget(self.SpinBox4_2, 3, 2, 1, 1)

        self.SpinBox2_1 = QSpinBox(self.groupBox)
        self.SpinBox2_1.setObjectName(u"SpinBox2_1")
        self.SpinBox2_1.setMinimum(1)
        self.SpinBox2_1.setMaximum(100)
        self.SpinBox2_1.setValue(4)

        self.gridLayout.addWidget(self.SpinBox2_1, 1, 1, 1, 1)

        self.SpinBox1_1 = QSpinBox(self.groupBox)
        self.SpinBox1_1.setObjectName(u"SpinBox1_1")
        self.SpinBox1_1.setMinimum(1)
        self.SpinBox1_1.setMaximum(48)

        self.gridLayout.addWidget(self.SpinBox1_1, 0, 1, 1, 1)

        self.CheckBox1 = QCheckBox(self.groupBox)
        self.CheckBox1.setObjectName(u"CheckBox1")
        self.CheckBox1.setChecked(True)

        self.gridLayout.addWidget(self.CheckBox1, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.WidgetControl)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.LayoutChartSettings = QVBoxLayout(self.groupBox_2)
        self.LayoutChartSettings.setSpacing(2)
        self.LayoutChartSettings.setObjectName(u"LayoutChartSettings")
        self.LayoutChartSettings.setContentsMargins(2, 2, 2, 2)
        self.LabelDuration = QLabel(self.groupBox_2)
        self.LabelDuration.setObjectName(u"LabelDuration")

        self.LayoutChartSettings.addWidget(self.LabelDuration)

        self.SliderDuration = QSlider(self.groupBox_2)
        self.SliderDuration.setObjectName(u"SliderDuration")
        self.SliderDuration.setMinimum(1)
        self.SliderDuration.setMaximum(20)
        self.SliderDuration.setPageStep(1)
        self.SliderDuration.setValue(20)
        self.SliderDuration.setSliderPosition(20)
        self.SliderDuration.setOrientation(Qt.Horizontal)
        self.SliderDuration.setTickPosition(QSlider.TicksAbove)
        self.SliderDuration.setTickInterval(1)

        self.LayoutChartSettings.addWidget(self.SliderDuration)

        self.LabelAmplitude = QLabel(self.groupBox_2)
        self.LabelAmplitude.setObjectName(u"LabelAmplitude")

        self.LayoutChartSettings.addWidget(self.LabelAmplitude)

        self.SliderAmplitude = QSlider(self.groupBox_2)
        self.SliderAmplitude.setObjectName(u"SliderAmplitude")
        self.SliderAmplitude.setMinimum(20)
        self.SliderAmplitude.setMaximum(200)
        self.SliderAmplitude.setSingleStep(1)
        self.SliderAmplitude.setPageStep(1)
        self.SliderAmplitude.setValue(200)
        self.SliderAmplitude.setOrientation(Qt.Horizontal)
        self.SliderAmplitude.setInvertedAppearance(False)
        self.SliderAmplitude.setInvertedControls(False)
        self.SliderAmplitude.setTickPosition(QSlider.TicksAbove)
        self.SliderAmplitude.setTickInterval(5)

        self.LayoutChartSettings.addWidget(self.SliderAmplitude)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.WidgetControl)

        self.WidgetCharts = QWidget(RhytmWindow)
        self.WidgetCharts.setObjectName(u"WidgetCharts")
        self.LayoutCharts = QVBoxLayout(self.WidgetCharts)
        self.LayoutCharts.setSpacing(0)
        self.LayoutCharts.setObjectName(u"LayoutCharts")
        self.LayoutCharts.setContentsMargins(0, 0, 0, 0)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.WidgetCharts)

        self.SliderChart = QSlider(RhytmWindow)
        self.SliderChart.setObjectName(u"SliderChart")
        self.SliderChart.setEnabled(True)
        self.SliderChart.setMaximum(10000)
        self.SliderChart.setSingleStep(10)
        self.SliderChart.setPageStep(250)
        self.SliderChart.setValue(10000)
        self.SliderChart.setOrientation(Qt.Horizontal)

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.SliderChart)


        self.retranslateUi(RhytmWindow)
        self.SliderDuration.valueChanged.connect(RhytmWindow._chart_redraw_request)
        self.SliderAmplitude.valueChanged.connect(RhytmWindow._chart_redraw_request)
        self.CheckBox1.stateChanged.connect(RhytmWindow._rhytms_param_cnd)
        self.CheckBox2.stateChanged.connect(RhytmWindow._rhytms_param_cnd)
        self.CheckBox3.stateChanged.connect(RhytmWindow._rhytms_param_cnd)
        self.CheckBox4.stateChanged.connect(RhytmWindow._rhytms_param_cnd)
        self.CheckBox5.stateChanged.connect(RhytmWindow._rhytms_param_cnd)
        self.SpinBox1_1.valueChanged.connect(RhytmWindow._rhytms_param_cnd)
        self.SpinBox1_2.valueChanged.connect(RhytmWindow._rhytms_param_cnd)
        self.SpinBox2_1.valueChanged.connect(RhytmWindow._rhytms_param_cnd)
        self.SpinBox2_2.valueChanged.connect(RhytmWindow._rhytms_param_cnd)
        self.SpinBox3_1.valueChanged.connect(RhytmWindow._rhytms_param_cnd)
        self.SpinBox3_2.valueChanged.connect(RhytmWindow._rhytms_param_cnd)
        self.SpinBox4_1.valueChanged.connect(RhytmWindow._rhytms_param_cnd)
        self.SpinBox4_2.valueChanged.connect(RhytmWindow._rhytms_param_cnd)
        self.SpinBox5_1.valueChanged.connect(RhytmWindow._rhytms_param_cnd)
        self.SpinBox5_2.valueChanged.connect(RhytmWindow._rhytms_param_cnd)
        self.ButtonReset.clicked.connect(RhytmWindow._reset)
        self.ButtonPause.clicked.connect(RhytmWindow._pause)
        self.ButtonResume.clicked.connect(RhytmWindow._resume)
        self.SliderChart.valueChanged.connect(RhytmWindow._slider_value_cnd)
        self.ButtonStart.clicked.connect(RhytmWindow._start)
        self.ButtonStop.clicked.connect(RhytmWindow._stop)

        QMetaObject.connectSlotsByName(RhytmWindow)
    # setupUi

    def retranslateUi(self, RhytmWindow):
        RhytmWindow.setWindowTitle(QCoreApplication.translate("RhytmWindow", u"Rhytms view", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("RhytmWindow", u"Chart control", None))
        self.ButtonStart.setText(QCoreApplication.translate("RhytmWindow", u"Start", None))
        self.ButtonPause.setText(QCoreApplication.translate("RhytmWindow", u"Pause", None))
        self.ButtonResume.setText(QCoreApplication.translate("RhytmWindow", u"Resume", None))
        self.ButtonStop.setText(QCoreApplication.translate("RhytmWindow", u"Stop", None))
        self.groupBox.setTitle(QCoreApplication.translate("RhytmWindow", u"Rhytms settings", None))
        self.CheckBox5.setText(QCoreApplication.translate("RhytmWindow", u"gamma", None))
        self.CheckBox2.setText(QCoreApplication.translate("RhytmWindow", u"theta", None))
        self.CheckBox4.setText(QCoreApplication.translate("RhytmWindow", u"betha", None))
        self.CheckBox3.setText(QCoreApplication.translate("RhytmWindow", u"alpha", None))
        self.ButtonReset.setText(QCoreApplication.translate("RhytmWindow", u"Reset", None))
        self.CheckBox1.setText(QCoreApplication.translate("RhytmWindow", u"delta", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("RhytmWindow", u"Chart settings", None))
        self.LabelDuration.setText(QCoreApplication.translate("RhytmWindow", u"Duration (sec): 20", None))
        self.LabelAmplitude.setText(QCoreApplication.translate("RhytmWindow", u"Amplitude (uV): 20", None))
    # retranslateUi

