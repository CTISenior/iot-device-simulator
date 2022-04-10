#!/usr/bin/python3

import sys

import utils.helper as Helper
import utils.gui_helper as GUIHelper
from dialogs.AddDialog import AddDialog
from connectors.mqtt_client import MQTT_Client
from connectors.http_client import HTTP_Client

from PySide2.QtWidgets import (
    QMainWindow,
    QHeaderView,
    QApplication,
    QGridLayout,
    QMessageBox,
    QGroupBox,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMenu,
    QWidget,
    QAction,
    QVBoxLayout,
    QPlainTextEdit
)
from PySide2.QtCore import (
    QEvent,
    Qt
)

class MainWindow(QMainWindow):
    def __init__(self):
        # init function
        QMainWindow.__init__(self)
        self.left = 200
        self.top = 200
        self.width = 800
        self.height = 600

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setWindowTitle("IoTwin | Data Generator")
        self.device_instance_list = []

        Helper.init()

        self.logger = Helper.create_logger('main', './logs/main.log')
        self.logger.debug('Main window created')

        self.init_menu_bar()
        self.init_ui()

        self.add_window = AddDialog(self)

    def init_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        refresh_act = QAction('Refresh', self)
        close_act = QAction('Close', self)
        refresh_act.triggered.connect(self.display_devices)
        close_act.triggered.connect(self.close)
        file_menu.addAction(refresh_act)
        file_menu.addAction(close_act)

        devices_menu = menubar.addMenu('Devices')
        device_act = QAction('Add Device', self)
        command_act = QAction('Command Panel', self)
        device_act.triggered.connect(self.add_device)
        devices_menu.addAction(device_act)
        devices_menu.addAction(command_act)

    def init_ui(self):
        main_layout = QGridLayout()

        self.device_count = QLabel()

        self.set_device_list_box()
        self.set_device_log_box()

        init_button = QPushButton('Add device', self)
        init_button.clicked.connect(self.add_device)

        main_layout.addWidget(self.device_list_box, 0, 0)

        main_layout.addWidget(self.device_log_box, 0, 1)
        main_layout.addWidget(self.device_count, 1, 0)
        main_layout.addWidget(init_button, 1, 1)

        main_layout.setColumnStretch(0, 4)
        main_layout.setColumnStretch(1, 2)

        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(main_layout)

    def set_device_list_box(self):
        self.device_list_box = QGroupBox("<Device List>")
        vbox = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setRowCount(15)
        self.table_widget.setHorizontalHeaderLabels(
            ['SN', 'Protocol', 'Interval', 'Status', 'Keys', 'Values', 'Value Types']
        )

        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)

        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.generate_menu)
        self.table_widget.viewport().installEventFilter(self)

        self.table_widget.doubleClicked.connect(self.table_widget_doubleClicked)

        vbox.addWidget(self.table_widget)
        self.device_list_box.setLayout(vbox)

        self.display_devices()

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton and source is self.table_widget.viewport():
                item = self.table_widget.itemAt(event.pos())
                self.menu = QMenu(self)
                if item is not None:
                    if int(item.column()) == 0:
                        self.current_device_sn = item.text()
                        self.start_action = self.menu.addAction('Start')
                        self.stop_action = self.menu.addAction('Stop')
                        self.delete_action = self.menu.addAction('Delete')
        return super().eventFilter(source, event)

    def generate_menu(self, pos):
        action = self.menu.exec_(self.table_widget.mapToGlobal(pos))
        if action is not None:
            if action == self.start_action:
                self.start_device()
            elif action == self.delete_action:
                self.delete_device()
            elif action == self.stop_action:
                self.stop_device()
            self.display_devices()

    def set_device_log_box(self):
        self.device_log_box = QGroupBox("<Device Log>")
        vbox = QVBoxLayout()

        self.log_area = QPlainTextEdit(self)
        self.log_area.setReadOnly(True)

        self.log_area.setStyleSheet("""QPlainTextEdit{
                color: white;
                background: black;
            }
            """
        )

        self.log_area.insertPlainText('Double click on the device row to see the running device log')

        vbox.addWidget(self.log_area)
        self.device_log_box.setLayout(vbox)

    def table_widget_doubleClicked(self):
        """ Show logs """

        row = self.table_widget.currentIndex().row()
        sn = self.table_widget.item(row, 0).text()  # first column <SN> only

        self.log_area.clear()  # clear list items
        self.get_device_logs(sn)

    def get_device_logs(self, sn):
        self.logger.debug(f'Show device logs: {sn}')

        logfile = Helper.get_device_log_file(sn)
        log_lines = Helper.read_log_file(logfile)

        if log_lines is not None:
            self.log_area.insertPlainText(f'Device logs: {sn}\n************************\n')
            self.log_area.appendPlainText("\n".join(log_lines))
        else:
            err = f'Log file does not exists: "{Helper.get_device_log_file(sn)}"'
            self.log_area.insertPlainText(err + "\n")
            self.logger.debug(err)

    def display_devices(self):
        ''' Display devices on the listbox '''

        devices = Helper.read_json()['devices']
        self.table_widget.setRowCount(len(devices))

        for index, value in enumerate(devices):
            self.table_widget.setItem(
                index, 0,
                QTableWidgetItem(value['serialNumber'])
            )
            self.table_widget.setItem(
                index, 1,
                QTableWidgetItem(value['protocol'])
            )
            self.table_widget.setItem(
                index, 2,
                QTableWidgetItem(f'({value["interval"]})')
            )

            obj = Helper.get_device_instance(self.device_instance_list, value['serialNumber'])
            self.table_widget.setItem(
                index, 3,
                QTableWidgetItem('Stopped')
            )
            self.table_widget.setItem(
                index, 7,
                QTableWidgetItem('0')
            )

            if obj and obj.check_thread():
                self.table_widget.setItem(
                    index, 3,
                    QTableWidgetItem('{Running}')
                )
                self.table_widget.setItem(
                    index, 7,
                    QTableWidgetItem('1')
                )

            #keys = [item['key'] for item in dev['keyValue']]
            #keys2 = devices[i]['keyValue'][0:len(devices[i]['keyValue'])]
            keys, init_values, value_types = [], [], []
            for item in value['keyValue']:
                keys.append(item['key'])
                init_values.append(item['initValue'])
                value_types.append(item['valueType'])

            self.table_widget.setItem(
                index, 4,
                QTableWidgetItem(str(keys))
            )
            self.table_widget.setItem(
                index, 5,
                QTableWidgetItem(str(init_values))
            )
            self.table_widget.setItem(
                index, 6,
                QTableWidgetItem(str(value_types))
            )

        msg = f'Number of running devices: [{str(Helper.get_running_device_count())}]'
        self.device_count.setText(msg)
        self.logger.debug(msg)

    def start_device(self):
        """ Righ-click menu item """

        if self.check_device_status() is None:
            device_obj = Helper.get_device_data(self.current_device_sn)
            msg = Helper.prepare_telemetry_data(device_obj)
            protocol = device_obj['protocol']

            if protocol == 'mqtt':
                device_instance = MQTT_Client(self.current_device_sn, device_obj, device_obj['protocol'])
                device_instance.run(msg)
            elif protocol == 'http':
                device_instance = HTTP_Client(self.current_device_sn, device_obj, device_obj['protocol'])
                device_instance.run(msg)

            self.append_to_instance_list(device_instance)
            #self.logger.debug(f'Start device: [{self.current_device_sn}]')
            GUIHelper.show_message_box(
                self,
                msg=f'Start device: [{self.current_device_sn}]',
                title='Success'
            )
        else:
            GUIHelper.show_message_box(
                self,
                msg=f'The device is already running [{self.current_device_sn}]',
                title='Warning!',
                msg_type='warning'
            )

    def stop_device(self):
        """ Righ-click menu item """

        if self.check_device_status() is None:
            GUIHelper.show_message_box(
                self,
                msg=f'The device is already stopped! [{self.current_device_sn}]',
                title='Warning!',
                msg_type='warning'
            )
        else:
            device_obj = Helper.get_device_instance(self.device_instance_list, self.current_device_sn)
            device_obj.stop_thread()
            self.remove_from_instance_list(device_obj)
            #self.logger.debug(f'Stop device: {self.current_device_sn}')
            GUIHelper.show_message_box(
                self,
                msg=f'Stop device: {self.current_device_sn}',
                title='Success'
            )

    def delete_device(self):
        """ Righ-click menu item """

        if self.check_device_status() is None:
            Helper.delete_json(self.current_device_sn)
            #self.logger.debug(f'Delete device: [{self.current_device_sn}]')
            GUIHelper.show_message_box(
                self,
                msg=f'Delete device: [{self.current_device_sn}]',
                title='Success'
            )
        else:
            GUIHelper.show_message_box(
                self,
                msg=f'Running device cannot be deleted! [{self.current_device_sn}]',
                title='Warning!',
                msg_type='warning'
            )

    def check_device_status(self):
        return Helper.get_device_instance(self.device_instance_list, self.current_device_sn)

    def add_device(self):
        """ Show add device dialog """

        if self.add_window.isVisible():
            self.logger.warning('AddDialog is already visible')
        else:
            self.logger.debug('AddDialog opened')
            self.add_window = AddDialog(self)
            self.add_window.show()

    def closeEvent(self, event):
        """ Exit the main window """

        msg_box = GUIHelper.show_message_box(
            self,
            msg='Are you sure you want to exit the program?',
            title='Confirmation',
            msg_type='question'
        )
        reply = msg_box.exec()

        if reply == QMessageBox.Ok:
            Helper.remove_device_log_files()  # delete all device .log files
            self.logger.debug('Delete all device log files [./logs/deviceLogs/*]')
            self.logger.debug('Main Window closed')

            event.accept()
            sys.exit()
        else:
            event.ignore()

    def append_to_instance_list(self, obj):
        self.device_instance_list.append(obj)
    def remove_from_instance_list(self, obj):
        self.device_instance_list.remove(obj)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
