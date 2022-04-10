import utils.setting as Setting

from PySide2.QtWidgets import (
    QComboBox,
    QLabel,
    QCheckBox,
    QSpinBox,
    QHBoxLayout,
    QMessageBox
)

def show_message_box(self, msg, title, msg_type='information'):
    msgbox = QMessageBox(self)

    if msg_type == 'warning':
        msgbox.setIcon(QMessageBox.Warning)
        self.logger.warning(msg)
    elif msg_type == 'question':
        msgbox.setIcon(QMessageBox.Question)
        msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    else:  # Information
        msgbox.setIcon(QMessageBox.Information)
        self.logger.info(msg)

    msgbox.setText(msg)
    msgbox.setWindowTitle(title)
    msgbox.show()

    return msgbox

def create_key_value_fields(row_num):
    key_combobox = QComboBox()
    key_combobox.setEditable(True)
    set_default_keys(key_combobox)

    value_spinbox = QSpinBox()
    value_spinbox.setValue(0)
    value_spinbox.setRange(-10000, 10000)

    value_typebox = QComboBox()
    set_value_types(value_typebox)

    checkbox = QCheckBox()
    if row_num == 0:
        checkbox.setEnabled(False)
        checkbox.setChecked(True)
    else:
        key_combobox.setEnabled(False)
        value_spinbox.setEnabled(False)
        value_typebox.setEnabled(False)

    keyvaluebox = QHBoxLayout()
    keyvaluebox.addWidget(key_combobox)
    keyvaluebox.addWidget(QLabel(f'Value-{str(row_num + 1)}:'))
    keyvaluebox.addWidget(value_spinbox)
    keyvaluebox.addWidget(value_typebox)
    keyvaluebox.addWidget(checkbox)

    return keyvaluebox


def get_keyvaluebox_widgets(keyvaluebox):
    key_combobox = keyvaluebox.itemAt(0).widget()
    value_spinbox = keyvaluebox.itemAt(2).widget()
    value_typebox = keyvaluebox.itemAt(3).widget()
    checkbox = keyvaluebox.itemAt(4).widget()

    return key_combobox, value_spinbox, value_typebox, checkbox


def set_default_keys(key_combobox):
    for key in Setting.get_default_keys():
        key_combobox.addItem(key)

def set_value_types(value_typebox):
    for key in Setting.get_value_types():
        value_typebox.addItem(key)
