# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#
#     autor       :  luka fricker
#     description :  pyqt5 program to create ticket sheets of a template
#                    combined with a export file from ticketleo
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

from mainWindow import Ui_MainWindow
from myConfig import myConfig
from mySettings import mySettings
from loadTicketLeoExport import loadTicketLeoExport as leoImport
from ticketGenerator import ticketGenerator
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys
from PIL.ImageQt import ImageQt
import os


class myMain(Ui_MainWindow):
    def __init__(self):
        self.cwd = os.getcwd()
        super(myMain, self).__init__()
        self.app_config = myConfig()
        self.settings = mySettings()
        self.creator = ticketGenerator()
        self.creator.setDate("00.00.")
        self.dataBrowser = leoImport()
        self.creator.setCardsPerPage(2, 6)
        self.full_seats = 0
        self.extra_seats = 0
        self.currentSetting = "name"
        self.input_dir = ""
        self.current_input_file = ""
        self.updating_controls = False
        self.dataAvailable = False
        self.templateAvailable = False
        self.settingsAvailable = False

        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.MainWindow)
        self.MainWindow.showMaximized()
        self.load_logo()

        # connect callbacks
        self.pb_input_dir.clicked.connect(self.pb_input_dir_clicked)
        self.pb_template.clicked.connect(self.pb_template_clicked)
        self.pb_start.clicked.connect(self.pb_start_clicked)
        self.pb_outline.clicked.connect(self.pb_outline_clicked)
        self.pb_new_outline.clicked.connect(self.pb_new_outline_clicked)
        self.list_toEdit.itemClicked.connect(self.selection_changed)
        self.list_input_files.itemClicked.connect(self.input_file_selected)
        self.pb_font.clicked.connect(self.pb_font_clicked)
        self.pb_save_preset.clicked.connect(self.pb_save_preset_clicked)
        self.list_presets.itemClicked.connect(self.preset_selected)
        self.pb_export_dir.clicked.connect(self.pb_export_clicked)

        self.spin_x.valueChanged.connect(self.field_controls_changed)
        self.spin_y.valueChanged.connect(self.field_controls_changed)
        self.spin_rot.valueChanged.connect(self.field_controls_changed)
        self.spin_size.valueChanged.connect(self.field_controls_changed)
        self.cb_centered.toggled.connect(self.field_controls_changed)
        self.spin_cards_x.valueChanged.connect(self.cards_changed)
        self.spin_cards_y.valueChanged.connect(self.cards_changed)
        self.spin_cards_x.setValue(2)
        self.spin_cards_y.setValue(6)

        # load persisted config
        self.config = self.app_config.get_config()
        self.presets = self.config.get("tickets", [])
        self.load_presets()
        if "last_export_dir" in self.config:
            self.te_export_dir.setText(self.config["last_export_dir"])
        if "input" in self.config:
            # backward compatibility: path to file
            in_file = self.config["input"]
            self.input_dir = os.path.dirname(in_file)
            self.input_dir_updated(self.input_dir, preselect=os.path.basename(in_file))
        elif "input_dir" in self.config:
            self.input_dir_updated(self.config["input_dir"], preselect=self.config.get("input_file", ""))
        if "template" in self.config.keys():
            self.template_updated(self.config["template"])
        if "outline" in self.config.keys():
            self.outline_updated(self.config["outline"])
        self.update_export_name()

        # initial selection
        if self.list_toEdit.count() > 0:
            self.list_toEdit.setCurrentRow(0)
            self.selection_changed(self.list_toEdit.item(0))

        sys.exit(self.app.exec_())

    def load_logo(self):
        try:
            logo_path = os.path.join(self.cwd, "config", "TheaterLogo_icon.png")
            if os.path.exists(logo_path):
                pix = QtGui.QPixmap(logo_path)
                if not pix.isNull():
                    target_height = max(60, min(120, self.leftWidget.height() // 6))
                    pix = pix.scaledToHeight(target_height, QtCore.Qt.SmoothTransformation)
                    self.logo_label.setPixmap(pix)
        except Exception as e:
            print("Logo load failed:", e)

    def load_presets(self):
        self.list_presets.clear()
        for preset in self.presets:
            self.list_presets.addItem(preset.get("name", ""))

    def pb_save_preset_clicked(self):
        name = self.le_preset_name.text().strip()
        if name == "":
            name = f"Ticket {len(self.presets)+1}"
        preset = {
            "name": name,
            "input_dir": self.input_dir,
            "input_file": self.current_input_file,
            "template": self.te_template.text(),
            "outline": self.te_outline.text(),
            "export_dir": self.te_export_dir.text(),
        }
        updated = False
        for idx, p in enumerate(self.presets):
            if p.get("name") == name:
                self.presets[idx] = preset
                updated = True
                break
        if not updated:
            self.presets.append(preset)
        self.config["tickets"] = self.presets
        self.app_config.set_config(self.config)
        self.load_presets()

    def preset_selected(self, item):
        name = item.text()
        preset = next((p for p in self.presets if p.get("name") == name), None)
        if not preset:
            return
        if preset.get("input_dir"):
            self.input_dir_updated(
                preset["input_dir"], preselect=preset.get("input_file", "")
            )
        elif preset.get("input"):
            # backward compatibility
            self.input_dir = os.path.dirname(preset["input"])
            self.input_dir_updated(self.input_dir, preselect=os.path.basename(preset["input"]))
        if preset.get("template"):
            self.template_updated(preset["template"])
        if preset.get("outline"):
            self.outline_updated(preset["outline"])
        if preset.get("export_dir"):
            self.export_dir_updated(preset["export_dir"])

    def input_updated(self, file):
        try:
            if file == "":
                return
            self.current_input_file = os.path.basename(file)
            # tell the data browser where to read the file contents
            self.dataBrowser.openExport(file)
            self.creator.setDate(self.dataBrowser.getDate())

            # collect the amount of total and empty tickets
            self.te_leer.setText("0")
            self.te_leer.setEnabled(True)
            self.tb_anzahl.setText(str(self.dataBrowser.getTicketCnt()))
            self.full_seats = self.dataBrowser.getTicketCnt()
            self.update_preview()
            # highlight current file in list
            matches = self.list_input_files.findItems(
                self.current_input_file, QtCore.Qt.MatchExactly
            )
            if matches:
                self.list_input_files.setCurrentItem(matches[0])
            self.config["input_dir"] = self.input_dir
            self.config["input_file"] = self.current_input_file
            self.app_config.set_config(self.config)
            self.dataAvailable = True
            self.update_export_name()
        except Exception as e:
            print("Update input failed:")
            print(e)

    def input_dir_updated(self, folder, preselect=""):
        if folder == "":
            return
        self.input_dir = folder
        self.te_input_dir.setText(folder)
        self.config["input_dir"] = folder
        self.app_config.set_config(self.config)
        files = []
        try:
            for f in os.listdir(folder):
                if f.lower().endswith((".xlsx", ".xls")):
                    files.append(f)
        except Exception as e:
            print("Listing input dir failed:", e)
        self.list_input_files.clear()
        for f in sorted(files):
            self.list_input_files.addItem(f)
        # preselect
        if preselect and preselect in files:
            items = self.list_input_files.findItems(preselect, QtCore.Qt.MatchExactly)
            if items:
                self.list_input_files.setCurrentItem(items[0])
                self.input_file_selected(items[0])
        elif files:
            self.list_input_files.setCurrentRow(0)
            self.input_file_selected(self.list_input_files.item(0))

    def pb_input_dir_clicked(self):
        start_dir = self.config.get("input_dir", os.path.join(self.cwd, "Samples"))
        folder = QFileDialog.getExistingDirectory(
            self.MainWindow,
            "TicketLeo Ordner wählen",
            start_dir,
        )
        if folder:
            self.input_dir_updated(folder)

    def input_file_selected(self, item):
        if not item or not self.input_dir:
            return
        file = os.path.join(self.input_dir, item.text())
        self.input_updated(file)

    def template_updated(self, file):
        try:
            if file == "":
                return
            self.te_template.setText(file)
            self.creator.setBaseImage(file)
            self.update_preview()
            self.config["template"] = file
            self.app_config.set_config(self.config)
            self.templateAvailable = True
        except Exception as e:
            print("Update template failed:")
            print(e)

    def pb_template_clicked(self):
        start_dir = (
            self.config.get("template")
            if "template" in self.config
            else os.path.join(self.cwd, "Samples")
        )
        fname = QFileDialog.getOpenFileName(
            self.MainWindow,
            "Open File",
            start_dir,
            "PNG (*.png)",
        )
        if fname[0] != "":
            self.template_updated(fname[0])

    def outline_updated(self, file):
        try:
            if file == "":
                return
            self.te_outline.setText(file)
            self.settings.openSettings(file)
            self.creator.setPositions(self.settings)
            self.update_preview()
            self.refresh_field_controls()
            self.update_font_label()
            self.config["outline"] = file
            self.app_config.set_config(self.config)
            self.settingsAvailable = True
        except Exception as e:
            print("Update outline failed:")
            print(e)

    def pb_outline_clicked(self):
        start_dir = (
            self.config.get("outline")
            if "outline" in self.config
            else os.path.join(self.cwd, "Samples")
        )
        fname = QFileDialog.getOpenFileName(
            self.MainWindow,
            "Open File",
            start_dir,
            "Settings (*.json)",
        )
        if fname[0] != "":
            self.outline_updated(fname[0])

    def pb_new_outline_clicked(self):
        fname = QFileDialog.getSaveFileName(
            self.MainWindow,
            "Save File",
            os.path.join(self.cwd, "Samples"),
            "Settings (*.json)",
        )

        if fname[0] != "":
            self.settingsAvailable = True
            self.settings.createSettings(fname[0])
            self.te_outline.setText(fname[0])
            self.creator.setPositions(self.settings)
            self.update_preview()
            self.refresh_field_controls()
            self.update_font_label()

    def pb_export_clicked(self):
        start_dir = self.config.get("last_export_dir", os.path.join(self.cwd, "Samples"))
        folder = QFileDialog.getExistingDirectory(
            self.MainWindow,
            "Export-Ordner wählen",
            start_dir,
        )
        if folder:
            self.export_dir_updated(folder)

    def export_dir_updated(self, folder):
        self.te_export_dir.setText(folder)
        try:
            self.config["last_export_dir"] = folder
            self.app_config.set_config(self.config)
        except Exception:
            pass
        self.update_export_name()

    def update_export_name(self):
        export_path = self.compute_export_path()
        if export_path:
            self.l_export_name.setText(os.path.basename(export_path))
        else:
            self.l_export_name.setText("Ticket_YYYYMMDD1.pdf")

    def compute_export_path(self):
        export_dir = self.te_export_dir.text()
        if not export_dir:
            return ""
        date_str = getattr(self.creator, "date", "00.00.")
        date_digits = "".join(ch for ch in date_str if ch.isdigit())
        if len(date_digits) == 8:
            # assume ddmmyyyy
            day = date_digits[0:2]
            month = date_digits[2:4]
            year = date_digits[4:8]
            date_clean = f"{year}-{month}-{day}"
        else:
            date_clean = date_digits if date_digits else "0000"
        counter = 1
        while True:
            filename = f"Ticket_{date_clean}_{counter}.pdf"
            path = os.path.join(export_dir, filename)
            if not os.path.exists(path):
                return path
            counter += 1

    def pb_start_clicked(self):
        if self.te_export_dir.text() == "":
            self.pb_export_clicked()
        export_path = self.compute_export_path()
        if (
            self.settingsAvailable == True
            and self.dataAvailable == True
            and self.templateAvailable == True
            and export_path != ""
        ):
            self.update_status("Reading")
            try:
                self.extra_seats = int(self.te_bus.text())
            except ValueError:
                self.extra_seats = 0
            self.creator.setCardsPerPage(
                int(self.spin_cards_x.value()), int(self.spin_cards_y.value())
            )
            cards_per_page = self.spin_cards_x.value() * self.spin_cards_y.value()

            # create the tickets
            tickets = []
            for i in range(self.full_seats):
                tickets.append(self.creator.createCard(self.dataBrowser.getCustomer(i)))
                self.update_status(
                    ("Creating\n" + str(i) + " of " + str(self.full_seats))
                )

            for i in range(self.extra_seats):
                tickets.append(self.creator.createBlanco())
                self.update_status(("Creating\n" + str(i) + " of " + str(self.extra_seats)))

            if self.cb_fill.isChecked():
                total = self.full_seats + self.extra_seats
                fill_needed = (cards_per_page - (total % cards_per_page)) % cards_per_page
                for i in range(fill_needed):
                    tickets.append(self.creator.createBlanco())
                    self.update_status(
                        ("Filling\n" + str(i + 1) + " of " + str(fill_needed))
                    )

            self.update_status("Storing")

            # save the tickets
            try:
                self.creator.createOutput(tickets, export_path)
                self.export_dir_updated(os.path.dirname(export_path))
                self.update_status("Done")
                # update label to next free name
                self.update_export_name()
            except Exception as e:
                print("Export failed:", e)
                self.update_status("Error")

    def cards_changed(self):
        self.creator.setCardsPerPage(
            int(self.spin_cards_x.value()), int(self.spin_cards_y.value())
        )
        self.update_preview()

    def refresh_field_controls(self):
        if not self.settingsAvailable:
            return
        try:
            self.updating_controls = True
            toEdit = self.settings.getItemValue("positionen")
            if toEdit and self.currentSetting in toEdit:
                self.spin_x.setValue(int(toEdit[self.currentSetting].get("x", 0)))
                self.spin_y.setValue(int(toEdit[self.currentSetting].get("y", 0)))
                self.spin_rot.setValue(int(toEdit[self.currentSetting].get("r", 0)))
                self.cb_centered.setChecked(bool(toEdit[self.currentSetting].get("c", False)))
            fonts = self.settings.getItemValue("fonts") or {}
            default_font = self.creator.default_fonts.get(
                self.currentSetting, {"size": 12}
            )
            font_entry = fonts.get(self.currentSetting, default_font)
            self.spin_size.setValue(int(font_entry.get("size", default_font.get("size", 12))))
            self.updating_controls = False
        except Exception as e:
            print("refresh_field_controls failed:", e)
            self.updating_controls = False

    def field_controls_changed(self, *args):
        if self.updating_controls or not self.settingsAvailable:
            return
        try:
            toEdit = self.settings.getItemValue("positionen")
            if not toEdit or self.currentSetting not in toEdit:
                return
            toEdit[self.currentSetting]["x"] = int(self.spin_x.value())
            toEdit[self.currentSetting]["y"] = int(self.spin_y.value())
            toEdit[self.currentSetting]["r"] = int(self.spin_rot.value())
            toEdit[self.currentSetting]["c"] = bool(self.cb_centered.isChecked())
            self.settings.setItemValue("positionen", toEdit)

            fonts = self.settings.getItemValue("fonts") or {}
            font_entry = fonts.get(self.currentSetting, {})
            if "family" not in font_entry:
                font_entry["family"] = self.creator.default_fonts.get(
                    self.currentSetting, {"family": "Arial"}
                )["family"]
            if "file" not in font_entry:
                font_entry["file"] = self.creator.default_fonts.get(
                    self.currentSetting, {"file": ""}
                ).get("file", "")
            font_entry["size"] = int(self.spin_size.value())
            fonts[self.currentSetting] = font_entry
            self.settings.setItemValue("fonts", fonts)

            self.settings.saveSettings()
            self.creator.setPositions(self.settings)
            self.update_font_label()
            self.update_preview()
        except Exception as e:
            print("field_controls_changed failed:", e)

    def update_preview(self):
        if (self.settingsAvailable == True) and (self.templateAvailable == True):
            self.creator.setPositions(self.settings)
            dummy_customer = {"name": "Mary Mustermann", "place": "000"}
            template = self.creator.createCard(dummy_customer)
            qim = ImageQt(template)
            pix = QtGui.QPixmap.fromImage(qim)
            target_size = self.ticket_preview.contentsRect().size()
            if target_size.width() > 0 and target_size.height() > 0:
                pix = pix.scaled(
                    target_size,
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation,
                )
            self.ticket_preview.setPixmap(pix)

    def selection_changed(self, item):
        self.currentSetting = item.text()
        self.refresh_field_controls()
        self.update_font_label()

    def update_status(self, text):
        self.l_status.setText(text)
        self.l_status.adjustSize()
        QApplication.processEvents()

    def pb_font_clicked(self):
        if not self.settingsAvailable:
            print("No settings file loaded")
            return

        current_font = self.__get_current_font()
        qfont, ok = QtWidgets.QFontDialog.getFont(
            QtGui.QFont(current_font["family"], current_font["size"]),
            self.MainWindow,
            "Schrift auswählen",
        )
        if ok:
            fonts = self.settings.getItemValue("fonts")
            if fonts == 0 or fonts is None:
                fonts = {}
            font_entry = {
                "family": qfont.family(),
                "size": qfont.pointSize(),
                "file": current_font.get("file", ""),
            }
            pick_file = QtWidgets.QMessageBox.question(
                self.MainWindow,
                "Font-Datei wählen?",
                "Soll eine Schriftdatei (.ttf/.otf) für den PDF-Export gewählt werden?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No,
            )
            if pick_file == QtWidgets.QMessageBox.Yes:
                fpath, _ = QtWidgets.QFileDialog.getOpenFileName(
                    self.MainWindow,
                    "Schriftdatei auswählen",
                    self.cwd,
                    "Font Files (*.ttf *.otf)",
                )
                if fpath:
                    font_entry["file"] = fpath

            fonts[self.currentSetting] = font_entry
            self.settings.setItemValue("fonts", fonts)
            self.settings.saveSettings()
            self.creator.setPositions(self.settings)
            self.update_font_label()
            self.refresh_field_controls()
            self.update_preview()

    def update_font_label(self):
        try:
            fonts = self.settings.getItemValue("fonts")
            if fonts and self.currentSetting in fonts:
                font_entry = fonts[self.currentSetting]
                file_hint = (
                    f" ({os.path.basename(font_entry['file'])})" if font_entry.get("file") else ""
                )
                self.l_font.setText(
                    f"{self.currentSetting}: {font_entry['family']} {font_entry['size']} pt{file_hint}"
                )
            else:
                self.l_font.setText(f"{self.currentSetting}: -")
        except Exception:
            self.l_font.setText(f"{self.currentSetting}: -")

    def __get_current_font(self):
        try:
            fonts = self.settings.getItemValue("fonts")
            if fonts and self.currentSetting in fonts:
                return fonts[self.currentSetting]
        except Exception:
            pass
        if self.currentSetting in self.creator.default_fonts:
            return self.creator.default_fonts[self.currentSetting]
        return {"family": "Arial", "size": 12, "file": ""}


myApp = myMain()
