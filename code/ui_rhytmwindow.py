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
    QGroupBox, QLabel, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_RhytmWindow(object):
    def setupUi(self, RhytmWindow):
        if not RhytmWindow.objectName():
            RhytmWindow.setObjectName(u"RhytmWindow")
        RhytmWindow.resize(1012, 633)
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
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.WidgetControl)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.CheckBoxDelta = QCheckBox(self.groupBox)
        self.CheckBoxDelta.setObjectName(u"CheckBoxDelta")

        self.gridLayout.addWidget(self.CheckBoxDelta, 0, 0, 1, 1)

        self.spinBox = QSpinBox(self.groupBox)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(48)

        self.gridLayout.addWidget(self.spinBox, 0, 1, 1, 1)

        self.spinBox_2 = QSpinBox(self.groupBox)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(100)
        self.spinBox_2.setValue(4)

        self.gridLayout.addWidget(self.spinBox_2, 0, 2, 1, 1)

        self.CheckBoxTheta = QCheckBox(self.groupBox)
        self.CheckBoxTheta.setObjectName(u"CheckBoxTheta")

        self.gridLayout.addWidget(self.CheckBoxTheta, 1, 0, 1, 1)

        self.spinBox_3 = QSpinBox(self.groupBox)
        self.spinBox_3.setObjectName(u"spinBox_3")
        self.spinBox_3.setMinimum(1)
        self.spinBox_3.setMaximum(100)
        self.spinBox_3.setValue(4)

        self.gridLayout.addWidget(self.spinBox_3, 1, 1, 1, 1)

        self.spinBox_4 = QSpinBox(self.groupBox)
        self.spinBox_4.setObjectName(u"spinBox_4")
        self.spinBox_4.setMinimum(1)
        self.spinBox_4.setMaximum(100)
        self.spinBox_4.setValue(8)

        self.gridLayout.addWidget(self.spinBox_4, 1, 2, 1, 1)

        self.CheckBoxAlpha = QCheckBox(self.groupBox)
        self.CheckBoxAlpha.setObjectName(u"CheckBoxAlpha")

        self.gridLayout.addWidget(self.CheckBoxAlpha, 2, 0, 1, 1)

        self.spinBox_5 = QSpinBox(self.groupBox)
        self.spinBox_5.setObjectName(u"spinBox_5")
        self.spinBox_5.setMinimum(1)
        self.spinBox_5.setMaximum(100)
        self.spinBox_5.setValue(8)

        self.gridLayout.addWidget(self.spinBox_5, 2, 1, 1, 1)

        self.spinBox_6 = QSpinBox(self.groupBox)
        self.spinBox_6.setObjectName(u"spinBox_6")
        self.spinBox_6.setMinimum(1)
        self.spinBox_6.setMaximum(100)
        self.spinBox_6.setValue(13)

        self.gridLayout.addWidget(self.spinBox_6, 2, 2, 1, 1)

        self.CheckBoxBetha = QCheckBox(self.groupBox)
        self.CheckBoxBetha.setObjectName(u"CheckBoxBetha")

        self.gridLayout.addWidget(self.CheckBoxBetha, 3, 0, 1, 1)

        self.spinBox_7 = QSpinBox(self.groupBox)
        self.spinBox_7.setObjectName(u"spinBox_7")
        self.spinBox_7.setMinimum(1)
        self.spinBox_7.setMaximum(100)
        self.spinBox_7.setValue(14)

        self.gridLayout.addWidget(self.spinBox_7, 3, 1, 1, 1)

        self.spinBox_8 = QSpinBox(self.groupBox)
        self.spinBox_8.setObjectName(u"spinBox_8")
        self.spinBox_8.setMinimum(1)
        self.spinBox_8.setMaximum(100)
        self.spinBox_8.setValue(40)

        self.gridLayout.addWidget(self.spinBox_8, 3, 2, 1, 1)

        self.CheckBoxGamma = QCheckBox(self.groupBox)
        self.CheckBoxGamma.setObjectName(u"CheckBoxGamma")

        self.gridLayout.addWidget(self.CheckBoxGamma, 4, 0, 1, 1)

        self.spinBox_9 = QSpinBox(self.groupBox)
        self.spinBox_9.setObjectName(u"spinBox_9")
        self.spinBox_9.setMinimum(1)
        self.spinBox_9.setMaximum(100)
        self.spinBox_9.setValue(40)

        self.gridLayout.addWidget(self.spinBox_9, 4, 1, 1, 1)

        self.spinBox_10 = QSpinBox(self.groupBox)
        self.spinBox_10.setObjectName(u"spinBox_10")
        self.spinBox_10.setMinimum(1)
        self.spinBox_10.setMaximum(100)
        self.spinBox_10.setValue(48)

        self.gridLayout.addWidget(self.spinBox_10, 4, 2, 1, 1)


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
        self.SliderAmplitude.setSingleStep(5)
        self.SliderAmplitude.setPageStep(20)
        self.SliderAmplitude.setValue(20)
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
        self.SliderChart.setEnabled(False)
        self.SliderChart.setOrientation(Qt.Horizontal)

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.SliderChart)


        self.retranslateUi(RhytmWindow)
        self.SliderDuration.valueChanged.connect(RhytmWindow._chart_redraw_request)
        self.SliderAmplitude.valueChanged.connect(RhytmWindow._chart_redraw_request)

        QMetaObject.connectSlotsByName(RhytmWindow)
    # setupUi

    def retranslateUi(self, RhytmWindow):
        RhytmWindow.setWindowTitle(QCoreApplication.translate("RhytmWindow", u"Rhytms view", None))
        self.groupBox.setTitle(QCoreApplication.translate("RhytmWindow", u"Rhytms settings", None))
        self.CheckBoxDelta.setText(QCoreApplication.translate("RhytmWindow", u"delta", None))
        self.CheckBoxTheta.setText(QCoreApplication.translate("RhytmWindow", u"theta", None))
        self.CheckBoxAlpha.setText(QCoreApplication.translate("RhytmWindow", u"alpha", None))
        self.CheckBoxBetha.setText(QCoreApplication.translate("RhytmWindow", u"betha", None))
        self.CheckBoxGamma.setText(QCoreApplication.translate("RhytmWindow", u"gamma", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("RhytmWindow", u"Chart settings", None))
        self.LabelDuration.setText(QCoreApplication.translate("RhytmWindow", u"Duration (sec): 20", None))
        self.LabelAmplitude.setText(QCoreApplication.translate("RhytmWindow", u"Amplitude (uV): 20", None))
    # retranslateUi

