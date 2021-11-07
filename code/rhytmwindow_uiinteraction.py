def rhytms_param_cnd(ui):
    ui.SpinBox1_1.setMinimum(1)
    ui.SpinBox1_1.setMaximum(ui.SpinBox1_2.value() - 1)
    ui.SpinBox1_2.setMinimum(ui.SpinBox1_1.value() + 1)
    ui.SpinBox1_2.setMaximum(ui.SpinBox2_1.value())

    ui.SpinBox2_1.setMinimum(ui.SpinBox1_2.value())
    ui.SpinBox2_1.setMaximum(ui.SpinBox2_2.value() - 1)
    ui.SpinBox2_2.setMinimum(ui.SpinBox2_1.value() + 1)
    ui.SpinBox2_2.setMaximum(ui.SpinBox3_1.value())

    ui.SpinBox3_1.setMinimum(ui.SpinBox2_2.value())
    ui.SpinBox3_1.setMaximum(ui.SpinBox3_2.value() - 1)
    ui.SpinBox3_2.setMinimum(ui.SpinBox3_1.value() + 1)
    ui.SpinBox3_2.setMaximum(ui.SpinBox4_1.value())

    ui.SpinBox4_1.setMinimum(ui.SpinBox3_2.value())
    ui.SpinBox4_1.setMaximum(ui.SpinBox4_2.value() - 1)
    ui.SpinBox4_2.setMinimum(ui.SpinBox4_1.value() + 1)
    ui.SpinBox4_2.setMaximum(ui.SpinBox5_1.value())

    ui.SpinBox5_1.setMinimum(ui.SpinBox4_2.value())
    ui.SpinBox5_1.setMaximum(ui.SpinBox5_2.value() - 1)
    ui.SpinBox5_2.setMinimum(ui.SpinBox5_1.value() + 1)
    ui.SpinBox5_2.setMaximum(100)


def open_session_run(ui):
    ui.ButtonStart.setEnabled(False)
    ui.ButtonPause.setEnabled(True)
    ui.ButtonResume.setEnabled(False)
    ui.ButtonStop.setEnabled(True)


def open_session_norun(ui):
    ui.ButtonStart.setEnabled(True)
    ui.ButtonPause.setEnabled(False)
    ui.ButtonResume.setEnabled(False)
    ui.ButtonStop.setEnabled(False)


def start(ui):
    ui.ButtonStart.setEnabled(False)
    ui.ButtonPause.setEnabled(True)
    ui.ButtonStop.setEnabled(True)


def stop(ui):
    ui.ButtonStart.setEnabled(True)
    ui.ButtonPause.setEnabled(False)
    ui.ButtonResume.setEnabled(False)
    ui.ButtonStop.setEnabled(False)


def pause(ui):
    ui.ButtonPause.setEnabled(False)
    ui.ButtonResume.setEnabled(True)
    ui.SliderChart.setEnabled(True)


def resume(ui):
    ui.ButtonPause.setEnabled(True)
    ui.ButtonResume.setEnabled(False)
    ui.SliderChart.setEnabled(False)