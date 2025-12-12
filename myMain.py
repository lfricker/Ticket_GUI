# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#
#     autor       :  luka fricker
#     date        :  21.02.2021
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
from PIL import Image, ImageFont, ImageDraw
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
        self.dataAvailable = False
        self.templateAvailable = False
        self.settingsAvailable = False

        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.MainWindow)

        # add font selection controls to the existing layout
        self.l_font = QtWidgets.QLabel("Font: -")
        font_label_font = QtGui.QFont()
        font_label_font.setPointSize(12)
        self.l_font.setFont(font_label_font)
        self.pb_font = QtWidgets.QPushButton("Font")
        self.gridLayout_2.addWidget(self.l_font, 4, 0, 1, 1)
        self.gridLayout_2.addWidget(self.pb_font, 4, 1, 1, 1)

        # connect the callbacks to the buttons from the window
        self.pb_input.clicked.connect(self.pb_input_clicked)
        self.pb_template.clicked.connect(self.pb_template_clicked)
        self.pb_start.clicked.connect(self.pb_start_clicked)
        self.pb_outline.clicked.connect(self.pb_outline_clicked)
        self.pb_new_outline.clicked.connect(self.pb_new_outline_clicked)
        self.pb_up.clicked.connect(
            lambda state, axis="y", dir="sub": self.pb_dir_clicked(axis, dir)
        )
        self.pb_down.clicked.connect(
            lambda state, axis="y", dir="add": self.pb_dir_clicked(axis, dir)
        )
        self.pb_left.clicked.connect(
            lambda state, axis="x", dir="sub": self.pb_dir_clicked(axis, dir)
        )
        self.pb_right.clicked.connect(
            lambda state, axis="x", dir="add": self.pb_dir_clicked(axis, dir)
        )
        self.pb_rotate.clicked.connect(
            lambda state, axis="r", dir="add": self.pb_dir_clicked(axis, dir)
        )
        self.list_toEdit.itemClicked.connect(self.selection_changed)
        self.pb_font.clicked.connect(self.pb_font_clicked)

        # check if default values are present. If so try to load them
        self.config = self.app_config.get_config()
        if "input" in self.config.keys():
            self.input_updated(self.config["input"])
        if "template" in self.config.keys():
            self.template_updated(self.config["template"])
        if "outline" in self.config.keys():
            self.outline_updated(self.config["outline"])

        # show the window
        self.MainWindow.show()
        sys.exit(self.app.exec_())

    def input_updated(self, file):
        try:
            self.te_input.setText(file)
            # tell the data browser where to read the file contents
            self.dataBrowser.openExport(file)
            self.creator.setDate(self.dataBrowser.getDate())

            # collect the ammount of total and empty tickets
            self.te_leer.setText("-")
            self.te_leer.setEnabled(False)
            self.tb_anzahl.setText(str(self.dataBrowser.getTicketCnt()))
            self.full_seats = self.dataBrowser.getTicketCnt()
            self.update_preview()
            self.config["input"] = file
            self.app_config.set_config(self.config)
            self.dataAvailable = True
        except Exception as e:
            print("Update input failed:")
            print(e)

    def pb_input_clicked(self):
        print("pb_input_clicked")
        # get path to the ticketleo export file
        fname = QFileDialog.getOpenFileName(
            self.MainWindow,
            "Open File",
            os.path.join(self.cwd, "Samples"),
            "Excel Files (*.xlsx)",
        )
        if fname[0] != "":
            self.input_updated(fname[0])

    def template_updated(self, file):
        try:
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
        print("pb_template_clicked")
        fname = QFileDialog.getOpenFileName(
            self.MainWindow,
            "Open File",
            os.path.join(self.cwd, "Samples"),
            "PNG (*.png)",
        )
        if fname[0] != "":
            self.template_updated(fname[0])

    def outline_updated(self, file):
        try:
            self.te_output.setText(file)
            self.settings.openSettings(file)
            self.creator.setPositions(self.settings)
            self.update_preview()
            self.update_font_label()
            self.config["outline"] = file
            self.app_config.set_config(self.config)
            self.settingsAvailable = True
        except Exception as e:
            print("Update outline failed:")
            print(e)

    def pb_outline_clicked(self):
        fname = QFileDialog.getOpenFileName(
            self.MainWindow,
            "Open File",
            os.path.join(self.cwd, "Samples"),
            "Settings (*.json)",
        )
        if fname[0] != "":
            self.outline_updated(fname[0])

    def pb_new_outline_clicked(self):
        print("pb_new_outline_clicked clicked")
        fname = QFileDialog.getSaveFileName(
            self.MainWindow,
            "Save File",
            os.path.join(self.cwd, "Samples"),
            "Settigns (*.json)",
        )

        if fname[0] != "":
            self.settingsAvailable = True
            self.settings.createSettings(fname[0])
            self.te_output.setText(fname[0])
            self.creator.setPositions(self.settings)
            self.update_preview()
            self.update_font_label()

    def pb_start_clicked(self):
        print("pb_outline_clicked")
        # open file dialog
        fname = QFileDialog.getSaveFileName(
            self.MainWindow,
            "Save File",
            os.path.join(self.cwd, "Samples"),
            "PDF (*.pdf)",
        )

        if fname[0] != "":
            if (
                self.settingsAvailable == True
                and self.dataAvailable == True
                and self.templateAvailable == True
            ):
                self.update_status("Reading")
                self.extra_seats = int(self.te_bus.text())
                print("Besetzt: ", self.full_seats)
                print("Blanco: ", self.extra_seats)
                self.creator.setCardsPerPage(
                    int(self.te_x.text()), int(self.te_y.text())
                )

                # create the tickets
                tickets = []
                for i in range(self.full_seats):
                    tickets.append(
                        self.creator.createCard(self.dataBrowser.getCustomer(i))
                    )
                    self.update_status(
                        ("Creating\n" + str(i) + " of " + str(self.full_seats))
                    )

                for i in range(self.extra_seats):
                    tickets.append(self.creator.createBlanco())
                    self.update_status(
                        ("Creating\n" + str(i) + " of " + str(self.extra_seats))
                    )

                self.update_status("Storing")

                # save the tickets
                try:
                    self.creator.createOutput(tickets, fname[0])
                    self.update_status("Done")
                except Exception:
                    self.update_status("Error")

    def pb_dir_clicked(self, axis, dir):
        print("pb clicked with ", axis, dir)
        self.change_setting(axis, dir)
        self.update_preview()

    def change_setting(self, axis, operator):
        try:
            toEdit = self.settings.getItemValue("positionen")
            if operator == "add":
                toEdit[self.currentSetting][axis] += int(self.te_step.text())
            else:
                toEdit[self.currentSetting][axis] -= int(self.te_step.text())
            self.settings.setItemValue("positionen", toEdit)
            self.settings.saveSettings()
        except TypeError:
            print("Invalid field selected")
        except Exception as e:
            print(type(e), e)

    def update_preview(self):
        if (self.settingsAvailable == True) and (self.templateAvailable == True):
            self.creator.setPositions(self.settings)
            dummy_customer = {"name": "Mary Mustermann", "place": "000"}
            template = self.creator.createCard(dummy_customer)
            scaleFactor = template.width / 500
            # convert the picture to pixmap and resize the label
            qim = ImageQt(template)
            pix = QtGui.QPixmap.fromImage(qim)
            self.ticket_preview.resize(
                int(template.width / scaleFactor), int(template.height / scaleFactor)
            )
            self.ticket_preview.setPixmap(QtGui.QPixmap(pix))

    def selection_changed(self, item):
        self.currentSetting = item.text()
        print("selected: ", self.currentSetting)
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
                "file": "",
            }
            # optionally let the user pick a font file for Pillow
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
            self.update_preview()

    def update_font_label(self):
        try:
            fonts = self.settings.getItemValue("fonts")
            if fonts and self.currentSetting in fonts:
                font_entry = fonts[self.currentSetting]
                self.l_font.setText(
                    f"{self.currentSetting}: {font_entry['family']} {font_entry['size']} pt"
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
        # fallback to ticket generator defaults
        if self.currentSetting in self.creator.default_fonts:
            return self.creator.default_fonts[self.currentSetting]
        return {"family": "Arial", "size": 12, "file": ""}


myApp = myMain()
