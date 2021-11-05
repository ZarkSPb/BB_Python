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

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(980, 649)
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(4)
        self.formLayout.setVerticalSpacing(4)
        self.formLayout.setContentsMargins(4, 4, 4, 4)
        self.WidgetControl = QWidget(Form)
        self.WidgetControl.setObjectName(u"WidgetControl")
        self.WidgetControl.setMinimumSize(QSize(150, 0))
        self.WidgetControl.setMaximumSize(QSize(150, 16777215))
        self.verticalLayout = QVBoxLayout(self.WidgetControl)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.WidgetControl)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)

        self.spinBox = QSpinBox(self.groupBox)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMaximum(50)

        self.gridLayout.addWidget(self.spinBox, 0, 1, 1, 1)

        self.spinBox_2 = QSpinBox(self.groupBox)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setMaximum(50)

        self.gridLayout.addWidget(self.spinBox_2, 0, 2, 1, 1)

        self.checkBox_2 = QCheckBox(self.groupBox)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.gridLayout.addWidget(self.checkBox_2, 1, 0, 1, 1)

        self.spinBox_3 = QSpinBox(self.groupBox)
        self.spinBox_3.setObjectName(u"spinBox_3")
        self.spinBox_3.setMaximum(50)

        self.gridLayout.addWidget(self.spinBox_3, 1, 1, 1, 1)

        self.spinBox_4 = QSpinBox(self.groupBox)
        self.spinBox_4.setObjectName(u"spinBox_4")
        self.spinBox_4.setMaximum(50)

        self.gridLayout.addWidget(self.spinBox_4, 1, 2, 1, 1)

        self.checkBox_3 = QCheckBox(self.groupBox)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.gridLayout.addWidget(self.checkBox_3, 2, 0, 1, 1)

        self.spinBox_5 = QSpinBox(self.groupBox)
        self.spinBox_5.setObjectName(u"spinBox_5")
        self.spinBox_5.setMaximum(50)

        self.gridLayout.addWidget(self.spinBox_5, 2, 1, 1, 1)

        self.spinBox_6 = QSpinBox(self.groupBox)
        self.spinBox_6.setObjectName(u"spinBox_6")
        self.spinBox_6.setMaximum(50)

        self.gridLayout.addWidget(self.spinBox_6, 2, 2, 1, 1)

        self.checkBox_4 = QCheckBox(self.groupBox)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.gridLayout.addWidget(self.checkBox_4, 3, 0, 1, 1)

        self.spinBox_7 = QSpinBox(self.groupBox)
        self.spinBox_7.setObjectName(u"spinBox_7")
        self.spinBox_7.setMaximum(50)

        self.gridLayout.addWidget(self.spinBox_7, 3, 1, 1, 1)

        self.spinBox_8 = QSpinBox(self.groupBox)
        self.spinBox_8.setObjectName(u"spinBox_8")
        self.spinBox_8.setMaximum(50)

        self.gridLayout.addWidget(self.spinBox_8, 3, 2, 1, 1)

        self.checkBox_5 = QCheckBox(self.groupBox)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.gridLayout.addWidget(self.checkBox_5, 4, 0, 1, 1)

        self.spinBox_9 = QSpinBox(self.groupBox)
        self.spinBox_9.setObjectName(u"spinBox_9")
        self.spinBox_9.setMaximum(50)

        self.gridLayout.addWidget(self.spinBox_9, 4, 1, 1, 1)

        self.spinBox_10 = QSpinBox(self.groupBox)
        self.spinBox_10.setObjectName(u"spinBox_10")
        self.spinBox_10.setMaximum(50)

        self.gridLayout.addWidget(self.spinBox_10, 4, 2, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.WidgetControl)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.LayoutChartSettings = QVBoxLayout(self.groupBox_2)
        self.LayoutChartSettings.setSpacing(4)
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

        self.WidgetCharts = QWidget(Form)
        self.WidgetCharts.setObjectName(u"WidgetCharts")
        self.LayoutCharts = QVBoxLayout(self.WidgetCharts)
        self.LayoutCharts.setSpacing(0)
        self.LayoutCharts.setObjectName(u"LayoutCharts")
        self.LayoutCharts.setContentsMargins(0, 0, 0, 0)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.WidgetCharts)

        self.horizontalSlider = QSlider(Form)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.horizontalSlider)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Rhytms settings", None))
        self.checkBox.setText(QCoreApplication.translate("Form", u"delta", None))
        self.checkBox_2.setText(QCoreApplication.translate("Form", u"theta", None))
        self.checkBox_3.setText(QCoreApplication.translate("Form", u"alpha", None))
        self.checkBox_4.setText(QCoreApplication.translate("Form", u"betha", None))
        self.checkBox_5.setText(QCoreApplication.translate("Form", u"gamma", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Chart settings", None))
        self.LabelDuration.setText(QCoreApplication.translate("Form", u"Duration (sec): 20", None))
        self.LabelAmplitude.setText(QCoreApplication.translate("Form", u"Amplitude (uV): 20", None))
    # retranslateUi

