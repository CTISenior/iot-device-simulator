#!/usr/bin/python3

import sys
import os
import logging
import time
import threading

from dialogs.AddDialog import AddDialog
from connectors.client import Client
import utils.helper as Helper
import utils.gui_helper as GUIHelper

from PySide2.QtWidgets import (
    QMainWindow,
    QHeaderView,
    QApplication,
    QGridLayout,
    QMessageBox,
    QGroupBox,
    QLabel,
    QTableWidget,
    QPushButton,
    QMenu,
    QWidget,
    QAction,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QAbstractItemView,
    QPlainTextEdit
)
from PySide2.QtCore import (
    Qt,
    QEvent
)
from PySide2.QtGui import (
    QTextCursor
)


class MainWindow(QMainWindow):
    def __init__(self):
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

        
        self.initMenuBar()
        self.initUI()

        self.display_log_thread = None

        self.add_window = AddDialog(self)

    def initMenuBar(self):
        menubar = self.menuBar()

        fileMenuBar = menubar.addMenu('File')
        refresh_act = QAction('Refresh', self)
        close_act = QAction('Close', self)
        refresh_act.triggered.connect(self.display_devices)
        close_act.triggered.connect(self.closeEvent)
        fileMenuBar.addAction(refresh_act)
        fileMenuBar.addAction(close_act)

        devicesMenuBar = menubar.addMenu('Devices')
        newDevice_act = QAction('Add Device', self)
        command_act = QAction('Command Panel', self)
        newDevice_act.triggered.connect(self.addDeviceBtn)
        devicesMenuBar.addAction(newDevice_act)
        devicesMenuBar.addAction(command_act)

        helpMenuBar = menubar.addMenu('Help')
        thread_act = QAction('List Threads', self)
        helpMenuBar.addAction(thread_act)

    def initUI(self):
        main_layout = QGridLayout()

        self.deviceCount = QLabel()

        self.device_list_box()
        self.device_log_box()

        initbutton = QPushButton('Add device', self)
        initbutton.clicked.connect(self.addDeviceBtn)

        main_layout.addWidget(self.deviceListBox, 0, 0)
       
        main_layout.addWidget(self.deviceLogBox, 0, 1)
        main_layout.addWidget(self.deviceCount, 1,0)
        main_layout.addWidget(initbutton, 1,1)

        main_layout.setColumnStretch(0, 4)
        main_layout.setColumnStretch(1, 2)
        
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(main_layout)


    def device_list_box(self):
        self.deviceListBox = QGroupBox("<Device List>")
        vbox = QVBoxLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setColumnHidden(7, True)
        self.tableWidget.setRowCount(15)
        self.tableWidget.setHorizontalHeaderLabels(['SN', 'Protocol', 'Interval', 'Status', 'Keys', 'Values', 'Value Types', 'Thread'])

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)
        self.tableWidget.viewport().installEventFilter(self)

        self.tableWidget.doubleClicked.connect(self.tableWidget_doubleClicked)

        vbox.addWidget(self.tableWidget)
        self.deviceListBox.setLayout(vbox)

        self.display_devices()

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton and source is self.tableWidget.viewport():
                item = self.tableWidget.itemAt(event.pos())
                self.menu = QMenu(self)
                if item is not None:
                    if int(item.column()) == 0:
                        self.current_deviceSN = item.text()
                        self.startAction = self.menu.addAction('Start') 
                        self.stopAction = self.menu.addAction('Stop')
                        self.deleteAction = self.menu.addAction('Delete') 
        return super(MainWindow, self).eventFilter(source, event)

    def generateMenu(self, pos):
        action = self.menu.exec_(self.tableWidget.mapToGlobal(pos))
        if action != None:
            if action == self.startAction:
                self.startDevice()
            elif action == self.deleteAction:
                self.deleteDevice()
            elif action == self.stopAction:
                self.stopDevice()
            self.display_devices()

    def device_log_box(self):
        self.deviceLogBox = QGroupBox("<Device Log>")
        vbox = QVBoxLayout()
        

        self.log_area = QPlainTextEdit(self)
        self.log_area.setReadOnly(True)

        self.log_area.setStyleSheet( """QPlainTextEdit{
                color: white;
                background: black;
            }
            """
        )
        
        self.log_area.insertPlainText(f'Double click on SN column to see the running device log')

        vbox.addWidget(self.log_area)
        self.deviceLogBox.setLayout(vbox)
    
    def tableWidget_doubleClicked(self):
        self.stop_display_log_thread()

        row = self.tableWidget.currentIndex().row()
        sn = self.tableWidget.item(row, 0).text() #first column <SN> only
        status = self.tableWidget.item(row, 7).text() #first column <SN> only

        self.log_area.clear() # clear list items
        self.log_area.insertPlainText(f'Device logs: {sn}\n************************\n')
        self.get_device_logs(sn, bool(int(status)))

    def get_device_logs(self, sn, status):
        self.logger.debug(f'Show device logs: {sn}')
        
        logfile = Helper.get_device_log_file(sn)
        log_lines = Helper.read_log_file(logfile)

        if log_lines != None:
            self.log_area.appendPlainText("\n".join(log_lines))

            if status != False : # if the device running, start threading to display logs
                logfilename = Helper.get_device_log_file(sn)
                logfile = open(logfilename,"r")
                logfile.seek(0, os.SEEK_END)
                self.display_logs = True
                self.display_log_thread = threading.Thread(
                    target = self.follow_last_line, 
                    args = (logfile,), 
                    name = "thread-logger_"+sn
                )
                self.display_log_thread.setDaemon(True) 
                self.display_log_thread.start()
        else:
            err = f'Log file does not exists: [{logfilename}]'
            self.b.insertPlainText(err + "\n")
            self.logger.debug(err)
    
    def follow_last_line(self, logfile):
        while self.display_logs:
            line = logfile.readline()
            if line:
                self.log_area.appendPlainText(line)
            time.sleep(1)

    def stop_display_log_thread(self):
        if self.display_log_thread != None:
            self.display_logs = False
            self.display_log_thread.join()

    def display_devices(self):
        devices = Helper.read_json()['devices']
        self.tableWidget.setRowCount(len(devices))
        
        
        for i in range(len(devices)):
            self.tableWidget.setItem(
                i, 0, 
                QTableWidgetItem(devices[i]['serialNumber'])
            )
            self.tableWidget.setItem(
                i, 1, 
                QTableWidgetItem(devices[i]['protocol'])
            )
            self.tableWidget.setItem(
                i, 2, 
                QTableWidgetItem(f'({devices[i]["interval"]})')
            )
            
            obj = Helper.get_device_instance(self.device_instance_list, devices[i]['serialNumber'])
            self.tableWidget.setItem(
                i, 3, 
                QTableWidgetItem('Stopped')
            )
            self.tableWidget.setItem(
                i, 7, 
                QTableWidgetItem('0')
            )
            if obj != False and obj.check_thread() != False:
                self.tableWidget.setItem(
                    i, 3, 
                    QTableWidgetItem('Running')
                )
                self.tableWidget.setItem(
                    i, 7, 
                    QTableWidgetItem('1')
                )
            
            #keys = [item['key'] for item in dev['keyValue']]
            #keys2 = devices[i]['keyValue'][0:len(devices[i]['keyValue'])]
            keys, init_values, value_types  = [], [], []
            for item in devices[i]['keyValue']:
                keys.append(item['key'])
                init_values.append( item['initValue'] )
                value_types.append( item['valueType'] )
            
            self.tableWidget.setItem(
                i, 4, 
                QTableWidgetItem(str(keys))
            )
            self.tableWidget.setItem(
                i, 5, 
                QTableWidgetItem(str(init_values))
            )
            self.tableWidget.setItem(
                i, 6, 
                QTableWidgetItem(str(value_types))
            )
            
        msg = f'Number of running devices: [{str(Helper.get_running_device_count())}]'
        self.deviceCount.setText( msg )
        self.logger.debug( msg )

    def startDevice(self):
        if self.check_device_status() == False:
            deviceObj = Helper.get_device_data(self.current_deviceSN)
            msg = Helper.create_message(deviceObj)
            
            new_client = Client()
            device_instance = new_client.run(self.current_deviceSN, deviceObj, msg, deviceObj['protocol'])
            if device_instance != None:
                self.appendToList(device_instance)
                #self.logger.debug(f'Start device: [{self.current_deviceSN}]')
                GUIHelper.show_message_box(
                    self, 
                    msg=f'Start device: [{self.current_deviceSN}]', 
                    title='Success'
                )
            else:
                #self.logger.warning(f'Protocol is not supported!: [{self.current_deviceSN} - {protocol}]')
                GUIHelper.show_message_box(
                    self, 
                    msg=f'Protocol is not supported!: [{self.current_deviceSN} - {protocol}]', 
                    title='Warning!',
                    msgType='warning'
                )
        else:
            GUIHelper.show_message_box(
                self, 
                msg=f'The device is already running [{self.current_deviceSN}]', 
                title='Warning!', 
                msgType='warning'
            )
    
    def stopDevice(self):
        if self.check_device_status() == False:
            GUIHelper.show_message_box(
                self, 
                msg=f'The device is already stopped! [{self.current_deviceSN}]', 
                title='Warning!', 
                msgType='warning'
            )
        else:
            deviceObj = Helper.get_device_instance(self.device_instance_list, self.current_deviceSN)
            deviceObj.stop_thread()
            self.removeFromList(deviceObj)
            #self.logger.debug(f'Stop device: {self.current_deviceSN}')
            GUIHelper.show_message_box(
                self, 
                msg=f'Stop device: {self.current_deviceSN}', 
                title='Success'
            )

    def deleteDevice(self):
        if self.check_device_status() == False:
            Helper.delete_json(self.current_deviceSN)
            #self.logger.debug(f'Delete device: [{self.current_deviceSN}]')
            GUIHelper.show_message_box(
                self, 
                msg=f'Delete device: [{self.current_deviceSN}]', 
                title='Success'
            )
        else:
            GUIHelper.show_message_box(
                self, 
                msg=f'Running device cannot be deleted! [{self.current_deviceSN}]', 
                title='Warning!', 
                msgType='warning'
            )

    def check_device_status(self):
        return Helper.get_device_instance(self.device_instance_list, self.current_deviceSN)
    
    def addDeviceBtn(self):
        if self.add_window.isVisible():
            self.logger.warning(f'AddDialog is already visible')
        else:
            self.logger.debug(f'AddDialog opened')
            self.add_window = AddDialog(self)
            self.stop_display_log_thread()
            self.add_window.show()

    def closeEvent(self, event):
        quit_msg = 'Are you sure you want to exit the program?'
        msgBox = GUIHelper.show_message_box(
            self, 
            msg='Are you sure you want to exit the program?', 
            title='Confirmation', 
            msgType='question'
        )
        reply = msgBox.exec()

        if reply == QMessageBox.Ok:
            Helper.remove_device_log_files() # delete all device .log files
            self.logger.debug(f'Delete all device log files ["./logs/deviceLogs/*"]')
            self.logger.debug(f'Main Window closed')

            event.accept()
            sys.exit()
        else:
            event.ignore()

    #@staticmethod
    def appendToList(self, obj):
        self.device_instance_list.append( obj )
    def removeFromList(self, obj):
        self.device_instance_list.remove( obj )
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
