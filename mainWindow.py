# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 900)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("config/TheaterLogo_icon.ico"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        mainLayout.setContentsMargins(10, 10, 10, 10)

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        mainLayout.addWidget(self.splitter)

        # Left panel: file management and presets
        self.leftWidget = QtWidgets.QWidget()
        leftLayout = QtWidgets.QVBoxLayout(self.leftWidget)
        leftLayout.setContentsMargins(5, 5, 5, 5)
        leftLayout.setSpacing(12)

        self.groupPresets = QtWidgets.QGroupBox("Tickets")
        presetsLayout = QtWidgets.QVBoxLayout(self.groupPresets)
        self.list_presets = QtWidgets.QListWidget()
        presetsLayout.addWidget(self.list_presets)
        presetRow = QtWidgets.QHBoxLayout()
        self.le_preset_name = QtWidgets.QLineEdit()
        self.le_preset_name.setPlaceholderText("Preset-Name")
        self.pb_save_preset = QtWidgets.QPushButton("Preset speichern")
        presetRow.addWidget(self.le_preset_name)
        presetRow.addWidget(self.pb_save_preset)
        presetsLayout.addLayout(presetRow)
        leftLayout.addWidget(self.groupPresets)

        self.groupFiles = QtWidgets.QGroupBox("Dateien")
        filesLayout = QtWidgets.QFormLayout(self.groupFiles)
        filesLayout.setLabelAlignment(QtCore.Qt.AlignRight)
        filesLayout.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # Input folder and file list
        inputRow = QtWidgets.QHBoxLayout()
        self.te_input_dir = QtWidgets.QLineEdit()
        self.te_input_dir.setReadOnly(True)
        self.pb_input_dir = QtWidgets.QPushButton("Ordner")
        inputRow.addWidget(self.te_input_dir)
        inputRow.addWidget(self.pb_input_dir)
        filesLayout.addRow("TicketLeo Ordner", inputRow)

        self.list_input_files = QtWidgets.QListWidget()
        self.list_input_files.setMinimumHeight(120)
        filesLayout.addRow("Dateien", self.list_input_files)

        # Template
        templateRow = QtWidgets.QHBoxLayout()
        self.te_template = QtWidgets.QLineEdit()
        self.te_template.setReadOnly(True)
        self.pb_template = QtWidgets.QPushButton("Wählen")
        templateRow.addWidget(self.te_template)
        templateRow.addWidget(self.pb_template)
        filesLayout.addRow("Template (PNG)", templateRow)

        # Outline
        outlineRow = QtWidgets.QHBoxLayout()
        self.te_outline = QtWidgets.QLineEdit()
        self.te_outline.setReadOnly(True)
        self.pb_outline = QtWidgets.QPushButton("Laden")
        self.pb_new_outline = QtWidgets.QPushButton("Neu")
        outlineRow.addWidget(self.te_outline)
        outlineRow.addWidget(self.pb_outline)
        outlineRow.addWidget(self.pb_new_outline)
        filesLayout.addRow("Outline (JSON)", outlineRow)

        leftLayout.addWidget(self.groupFiles)
        leftLayout.addStretch()
        self.logo_label = QtWidgets.QLabel()
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_label.setMinimumHeight(80)
        leftLayout.addWidget(self.logo_label)
        self.logo_caption = QtWidgets.QLabel("Created by Luka Fricker")
        self.logo_caption.setAlignment(QtCore.Qt.AlignCenter)
        font_caption = QtGui.QFont()
        font_caption.setPointSize(10)
        self.logo_caption.setFont(font_caption)
        leftLayout.addWidget(self.logo_caption)
        self.splitter.addWidget(self.leftWidget)

        # Center panel: controls and preview
        self.centerWidget = QtWidgets.QWidget()
        centerLayout = QtWidgets.QVBoxLayout(self.centerWidget)
        centerLayout.setContentsMargins(5, 5, 5, 5)
        centerLayout.setSpacing(12)

        self.groupFields = QtWidgets.QGroupBox("Feld-Einstellungen")
        fieldsGrid = QtWidgets.QGridLayout(self.groupFields)
        fieldsGrid.setHorizontalSpacing(10)
        fieldsGrid.setVerticalSpacing(8)

        self.list_toEdit = QtWidgets.QListWidget()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.list_toEdit.setFont(font)
        self.list_toEdit.addItems(["name", "datum", "platz"])
        fieldsGrid.addWidget(self.list_toEdit, 0, 0, 6, 1)

        self.l_font = QtWidgets.QLabel("Font: -")
        fieldsGrid.addWidget(self.l_font, 0, 1, 1, 2)
        self.pb_font = QtWidgets.QPushButton("Font wählen")
        fieldsGrid.addWidget(self.pb_font, 0, 3, 1, 1)

        self.cb_centered = QtWidgets.QCheckBox("Zentriert")
        fieldsGrid.addWidget(self.cb_centered, 1, 1, 1, 1)

        self.spin_size = QtWidgets.QSpinBox()
        self.spin_size.setRange(6, 200)
        fieldsGrid.addWidget(QtWidgets.QLabel("Größe"), 1, 2, 1, 1)
        fieldsGrid.addWidget(self.spin_size, 1, 3, 1, 1)

        self.spin_x = QtWidgets.QSpinBox()
        self.spin_x.setRange(-500, 500)
        self.spin_y = QtWidgets.QSpinBox()
        self.spin_y.setRange(-500, 500)
        self.spin_rot = QtWidgets.QSpinBox()
        self.spin_rot.setRange(-180, 180)
        fieldsGrid.addWidget(QtWidgets.QLabel("Pos X"), 2, 1, 1, 1)
        fieldsGrid.addWidget(self.spin_x, 2, 2, 1, 2)
        fieldsGrid.addWidget(QtWidgets.QLabel("Pos Y"), 3, 1, 1, 1)
        fieldsGrid.addWidget(self.spin_y, 3, 2, 1, 2)
        fieldsGrid.addWidget(QtWidgets.QLabel("Rotation"), 4, 1, 1, 1)
        fieldsGrid.addWidget(self.spin_rot, 4, 2, 1, 2)

        self.spin_cards_x = QtWidgets.QSpinBox()
        self.spin_cards_x.setRange(1, 10)
        self.spin_cards_y = QtWidgets.QSpinBox()
        self.spin_cards_y.setRange(1, 10)
        fieldsGrid.addWidget(QtWidgets.QLabel("Nebeneinander"), 5, 1, 1, 1)
        fieldsGrid.addWidget(self.spin_cards_x, 5, 2, 1, 1)
        fieldsGrid.addWidget(QtWidgets.QLabel("Untereinander"), 5, 3, 1, 1)
        fieldsGrid.addWidget(self.spin_cards_y, 5, 4, 1, 1)

        centerLayout.addWidget(self.groupFields)

        self.groupPreview = QtWidgets.QGroupBox("Vorschau")
        previewLayout = QtWidgets.QVBoxLayout(self.groupPreview)
        self.ticket_preview = QtWidgets.QLabel()
        self.ticket_preview.setMinimumHeight(300)
        self.ticket_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.ticket_preview.setScaledContents(False)
        previewLayout.addWidget(self.ticket_preview)
        centerLayout.addWidget(self.groupPreview, 1)

        self.splitter.addWidget(self.centerWidget)

        # Right panel: export
        self.rightWidget = QtWidgets.QWidget()
        rightLayout = QtWidgets.QVBoxLayout(self.rightWidget)
        rightLayout.setContentsMargins(5, 5, 5, 5)
        rightLayout.setSpacing(12)

        self.groupExport = QtWidgets.QGroupBox("Export")
        exportLayout = QtWidgets.QFormLayout(self.groupExport)
        exportLayout.setLabelAlignment(QtCore.Qt.AlignRight)

        exportRow = QtWidgets.QHBoxLayout()
        self.te_export_dir = QtWidgets.QLineEdit()
        self.te_export_dir.setReadOnly(True)
        self.pb_export_dir = QtWidgets.QPushButton("Ordner")
        exportRow.addWidget(self.te_export_dir)
        exportRow.addWidget(self.pb_export_dir)
        exportLayout.addRow("PDF Ordner", exportRow)

        self.l_export_name = QtWidgets.QLabel("Ticket_YYYYMMDD1.pdf")
        exportLayout.addRow("Dateiname", self.l_export_name)

        self.tb_anzahl = QtWidgets.QLabel("0")
        exportLayout.addRow("Anzahl Tickets", self.tb_anzahl)

        self.te_leer = QtWidgets.QLineEdit("0")
        exportLayout.addRow("Leere Plätze", self.te_leer)

        self.te_bus = QtWidgets.QLineEdit("0")
        exportLayout.addRow("Bus Plätze", self.te_bus)

        self.cb_fill = QtWidgets.QCheckBox("Platz füllen")
        exportLayout.addRow("Auto auffüllen", self.cb_fill)

        rightLayout.addWidget(self.groupExport)

        self.l_status = QtWidgets.QLabel("-status-")
        statusFont = QtGui.QFont()
        statusFont.setPointSize(12)
        self.l_status.setFont(statusFont)
        rightLayout.addWidget(self.l_status)

        self.pb_start = QtWidgets.QPushButton("Start")
        startFont = QtGui.QFont()
        startFont.setPointSize(14)
        self.pb_start.setFont(startFont)
        rightLayout.addWidget(self.pb_start)

        rightLayout.addStretch()
        self.splitter.addWidget(self.rightWidget)

        MainWindow.setTabOrder(self.list_presets, self.pb_save_preset)
        MainWindow.setTabOrder(self.pb_save_preset, self.pb_input_dir)
        MainWindow.setTabOrder(self.pb_input_dir, self.list_input_files)
        MainWindow.setTabOrder(self.list_input_files, self.pb_template)
        MainWindow.setTabOrder(self.pb_template, self.pb_outline)
        MainWindow.setTabOrder(self.pb_outline, self.pb_new_outline)
        MainWindow.setTabOrder(self.pb_new_outline, self.list_toEdit)
        MainWindow.setTabOrder(self.list_toEdit, self.cb_centered)
        MainWindow.setTabOrder(self.cb_centered, self.spin_size)
        MainWindow.setTabOrder(self.spin_size, self.spin_x)
        MainWindow.setTabOrder(self.spin_x, self.spin_y)
        MainWindow.setTabOrder(self.spin_y, self.spin_rot)
        MainWindow.setTabOrder(self.spin_rot, self.spin_cards_x)
        MainWindow.setTabOrder(self.spin_cards_x, self.spin_cards_y)
        MainWindow.setTabOrder(self.spin_cards_y, self.pb_font)
        MainWindow.setTabOrder(self.pb_font, self.te_export_dir)
        MainWindow.setTabOrder(self.te_export_dir, self.pb_export_dir)
        MainWindow.setTabOrder(self.pb_export_dir, self.te_leer)
        MainWindow.setTabOrder(self.te_leer, self.te_bus)
        MainWindow.setTabOrder(self.te_bus, self.cb_fill)
        MainWindow.setTabOrder(self.te_bus, self.pb_start)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ticket Generator"))
