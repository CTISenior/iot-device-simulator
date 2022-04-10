#!/usr/bin/python3

import logging
import utils.helper as Helper
import utils.gui_helper as GUIHelper

from PySide2.QtWidgets import (
    QFormLayout,
    QComboBox,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QCheckBox,
    QTabWidget,
    QSpinBox,
    QHBoxLayout,
    QDialogButtonBox,
)
from PySide2.QtCore import (
    Qt
)


class AddDialog(QTabWidget):
    def __init__(self, main_window, parent=None):
        super(AddDialog, self).__init__(parent)
        self.left = 250
        self.top = 250
        self.width = 450
        self.height = 450
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.main_window = main_window

        #self.setFixedSize(QSize(self.width, self.height))
        self.setWindowTitle("Add New Device")

        layout = QVBoxLayout()
        self.setLayout(layout)

        tabs = QTabWidget()
        tabs.addTab(self.tab1_ui(), "Thread")

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Close,
            Qt.Horizontal,
            self
        )

        self.button_box.accepted.connect(self.add_device)
        self.button_box.rejected.connect(self.close)

        self.device_status_label = QLabel()
        self.device_status_label.setText('')

        layout2 = QHBoxLayout()

        layout.addWidget(tabs)
        layout2.addWidget(self.device_status_label)
        layout2.addWidget(self.button_box)
        layout.addLayout(layout2)

        self.logger = logging.getLogger('main')
        self.logger.debug('AddDialog created')

    def tab1_ui(self):
        self.tab1 = QWidget()

        tab1_box_layout = QVBoxLayout()
        tab1_form_layout = QFormLayout()

        self.device_sn = QLineEdit(self)
        tab1_form_layout.addRow("SN*:", self.device_sn)

        self.device_name = QLineEdit(self)
        tab1_form_layout.addRow("Type/Name*:", self.device_name)
        self.device_model = QLineEdit(self)
        tab1_form_layout.addRow("Model*:", self.device_model)
        self.device_token = QLineEdit(self)
        self.device_token.setEnabled(False)
        tab1_form_layout.addRow("Token:", self.device_token)

        self.keyvaluebox = []
        for i in range(5):  # 5 key-value rows
            keyvaluebox = GUIHelper.create_key_value_fields(i)
            self.keyvaluebox.append(keyvaluebox)

        for index, value in enumerate(self.keyvaluebox):
            key_combobox, value_spinbox, value_typebox, checkbox = GUIHelper.get_keyvaluebox_widgets(
                value)

            checkbox.toggled.connect(key_combobox.setEnabled)
            checkbox.toggled.connect(value_spinbox.setEnabled)
            checkbox.toggled.connect(value_typebox.setEnabled)

            tab1_form_layout.addRow(f'Key-{str(index+1)}:', value)

        self.interval = QSpinBox(self)
        self.interval.setRange(1, 100)
        tab1_form_layout.addRow(QLabel("Interval(sec):"), self.interval)

        self.protocol = QComboBox(self)
        self.protocol.addItem("MQTT")
        self.protocol.addItem("HTTP")
        tab1_form_layout.addRow(QLabel("Protocol:"), self.protocol)

        self.secbox = QCheckBox("")
        self.secbox.setEnabled(False)
        tab1_form_layout.addRow(QLabel("Secure:"), self.secbox)
        # self.secbox.stateChanged.connect(self.click_secure)

        tab1_form_layout.setSpacing(10)
        tab1_box_layout.addLayout(tab1_form_layout)
        self.tab1.setLayout(tab1_box_layout)

        return self.tab1

    def add_device(self):
        """Add device operation."""

        protocol = self.protocol.currentText().lower()
        device_type = self.device_name.text()
        device_model = self.device_model.text()
        device_sn = self.device_sn.text()
        interval = int(self.interval.value())

        data_obj = {
            "serialNumber": device_sn,
            "sensorType": device_type,
            "sensorModel": device_model,
            "accessToken": "",
            "keyValue": [],
            "protocol": protocol,
            "thread": True,
            "interval": interval
        }

        fields_to_validate = [
            device_sn,
            device_type,
            device_model
        ]

        invalid_edit_field = True
        invalid_key_field = True
        for field in fields_to_validate:
            invalid_edit_field = Helper.validate_field(field)
            if not invalid_edit_field:
                break

        key_list = []
        for index, value in enumerate(self.keyvaluebox):
            key_combobox, value_spinbox, value_typebox, checkbox = GUIHelper.get_keyvaluebox_widgets(value)

            if checkbox.isChecked():
                key = key_combobox.currentText()
                value = int(value_spinbox.text())
                value_type = value_typebox.currentText()

                obj = {
                    "key": key,
                    "initValue": value,
                    "valueType": value_type
                }

                key_list.append(key)

                data_obj["keyValue"].append(obj)

                if not Helper.validate_field(key):
                    invalid_key_field = False

        if (
           not invalid_edit_field or
           not invalid_key_field
           ):
            err = 'Invalid input! (Min: 3 and Max: 30 characters)'
            self.device_status_label.setText(err)
            GUIHelper.show_message_box(
                self,
                msg=err,
                title='Warning!',
                msg_type='warning'
            )
            return

        check_duplicated_keys = Helper.check_duplicated_keys(key_list)
        if check_duplicated_keys:  # same keys are invalid
            err = 'Duplicated keys!'
            self.device_status_label.setText(err)
            GUIHelper.show_message_box(
                self,
                msg=err,
                title='Warning!',
                msg_type='warning'
            )
            return

        status = Helper.check_device_exist(device_sn)
        if not status:
            Helper.update_json(data_obj)
            self.device_status_label.setText('Added!')
            self.main_window.display_devices()  # refresh content
            GUIHelper.show_message_box(
                self,
                msg=f'New device added: [{device_sn} - {protocol}]',
                title='Success'
            )
            #self.logger.debug(f'New device added: [{deviceSN} - {protocol}]')
        else:
            err = 'DeviceSN already exists!'
            self.device_status_label.setText(err)
            GUIHelper.show_message_box(
                self,
                msg=f'{err}: [{device_sn} - {protocol}]',
                title='Warning!',
                msg_type='warning'
            )
            #self.logger.warning(f'Device already exists!: [{deviceSN} - {protocol}]')

    def closeEvent(self, event):
        self.main_window.display_devices()
        self.logger.warning('AddDialog closed')
