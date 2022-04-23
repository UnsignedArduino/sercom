# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.main_glayout = QtWidgets.QGridLayout(self.central_widget)
        self.main_glayout.setContentsMargins(0, 0, 0, 0)
        self.main_glayout.setObjectName("main_glayout")
        self.text_edit = QtWidgets.QPlainTextEdit(self.central_widget)
        self.text_edit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.text_edit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.text_edit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.text_edit.setReadOnly(True)
        self.text_edit.setObjectName("text_edit")
        self.main_glayout.addWidget(self.text_edit, 0, 0, 1, 1)
        main_window.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menu_bar.setObjectName("menu_bar")
        self.menu_file = QtWidgets.QMenu(self.menu_bar)
        self.menu_file.setObjectName("menu_file")
        self.menu_port = QtWidgets.QMenu(self.menu_bar)
        self.menu_port.setObjectName("menu_port")
        self.menu_connect_to_port = QtWidgets.QMenu(self.menu_port)
        self.menu_connect_to_port.setToolTipsVisible(True)
        self.menu_connect_to_port.setObjectName("menu_connect_to_port")
        self.menu_configuration = QtWidgets.QMenu(self.menu_bar)
        self.menu_configuration.setObjectName("menu_configuration")
        self.menu_byte_size = QtWidgets.QMenu(self.menu_configuration)
        self.menu_byte_size.setObjectName("menu_byte_size")
        self.menu_flow_control = QtWidgets.QMenu(self.menu_configuration)
        self.menu_flow_control.setObjectName("menu_flow_control")
        self.menu_stop_bits = QtWidgets.QMenu(self.menu_configuration)
        self.menu_stop_bits.setObjectName("menu_stop_bits")
        self.menu_parity = QtWidgets.QMenu(self.menu_configuration)
        self.menu_parity.setObjectName("menu_parity")
        self.menu_line_ending = QtWidgets.QMenu(self.menu_configuration)
        self.menu_line_ending.setObjectName("menu_line_ending")
        main_window.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(main_window)
        self.status_bar.setObjectName("status_bar")
        main_window.setStatusBar(self.status_bar)
        self.action_new_session = QtWidgets.QAction(main_window)
        self.action_new_session.setObjectName("action_new_session")
        self.action_exit = QtWidgets.QAction(main_window)
        self.action_exit.setMenuRole(QtWidgets.QAction.QuitRole)
        self.action_exit.setObjectName("action_exit")
        self.action_enter_custom_port = QtWidgets.QAction(main_window)
        self.action_enter_custom_port.setObjectName("action_enter_custom_port")
        self.action_disconnect = QtWidgets.QAction(main_window)
        self.action_disconnect.setObjectName("action_disconnect")
        self.action0 = QtWidgets.QAction(main_window)
        self.action0.setObjectName("action0")
        self.action0_2 = QtWidgets.QAction(main_window)
        self.action0_2.setObjectName("action0_2")
        self.action0_3 = QtWidgets.QAction(main_window)
        self.action0_3.setObjectName("action0_3")
        self.action0_4 = QtWidgets.QAction(main_window)
        self.action0_4.setObjectName("action0_4")
        self.action0_5 = QtWidgets.QAction(main_window)
        self.action0_5.setObjectName("action0_5")
        self.action0_6 = QtWidgets.QAction(main_window)
        self.action0_6.setObjectName("action0_6")
        self.action_baud_rate = QtWidgets.QAction(main_window)
        self.action_baud_rate.setObjectName("action_baud_rate")
        self.menu_file.addAction(self.action_new_session)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menu_port.addAction(self.menu_connect_to_port.menuAction())
        self.menu_port.addAction(self.action_disconnect)
        self.menu_configuration.addAction(self.action_baud_rate)
        self.menu_configuration.addAction(self.menu_byte_size.menuAction())
        self.menu_configuration.addAction(self.menu_parity.menuAction())
        self.menu_configuration.addAction(self.menu_stop_bits.menuAction())
        self.menu_configuration.addAction(self.menu_flow_control.menuAction())
        self.menu_configuration.addAction(self.menu_line_ending.menuAction())
        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_port.menuAction())
        self.menu_bar.addAction(self.menu_configuration.menuAction())

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "sercom"))
        self.text_edit.setPlaceholderText(_translate("main_window", "Not connected to a port."))
        self.menu_file.setTitle(_translate("main_window", "&File"))
        self.menu_port.setTitle(_translate("main_window", "&Port"))
        self.menu_connect_to_port.setToolTip(_translate("main_window", "Connect to a serial port."))
        self.menu_connect_to_port.setStatusTip(_translate("main_window", "Connect to a serial port."))
        self.menu_connect_to_port.setTitle(_translate("main_window", "&Connect to port"))
        self.menu_configuration.setTitle(_translate("main_window", "&Configuration"))
        self.menu_byte_size.setTitle(_translate("main_window", "&Byte size"))
        self.menu_flow_control.setTitle(_translate("main_window", "&Flow control"))
        self.menu_stop_bits.setTitle(_translate("main_window", "&Stop bits"))
        self.menu_parity.setTitle(_translate("main_window", "&Parity"))
        self.menu_line_ending.setTitle(_translate("main_window", "&Line ending"))
        self.action_new_session.setText(_translate("main_window", "&New session..."))
        self.action_new_session.setToolTip(_translate("main_window", "Create a new session."))
        self.action_new_session.setStatusTip(_translate("main_window", "Create a new session."))
        self.action_exit.setText(_translate("main_window", "&Exit"))
        self.action_exit.setToolTip(_translate("main_window", "Disconnect and exit."))
        self.action_exit.setStatusTip(_translate("main_window", "Disconnect and exit."))
        self.action_enter_custom_port.setText(_translate("main_window", "Enter &custom port..."))
        self.action_disconnect.setText(_translate("main_window", "&Disconnect"))
        self.action_disconnect.setToolTip(_translate("main_window", "Disconnect from the connected serial port."))
        self.action_disconnect.setStatusTip(_translate("main_window", "Disconnect from the connected serial port."))
        self.action0.setText(_translate("main_window", "0"))
        self.action0_2.setText(_translate("main_window", "0"))
        self.action0_3.setText(_translate("main_window", "0"))
        self.action0_4.setText(_translate("main_window", "0"))
        self.action0_5.setText(_translate("main_window", "0"))
        self.action0_6.setText(_translate("main_window", "0"))
        self.action_baud_rate.setText(_translate("main_window", "Baud &rate..."))
