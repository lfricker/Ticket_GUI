#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#
#     autor       :  luka fricker
#     date        :  21.02.2021
#     description :  pyqt5 program to create ticket sheets of a template
#                    combined with a export file from ticketleo
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#



from mainWindow import Ui_MainWindow
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
      self.settings = mySettings()
      self.creator = ticketGenerator()
      self.creator.setDate("00.00.")
      self.dataBrowser = leoImport()
      self.creator.setCardsPerPage(2,6)
      self.full_seats  = 0
      self.extra_seats = 0
      self.currentSetting = "name"
      self.dataAvailable = False
      self.templateAvailable = False
      self.settingsAvailable = False
      self.init()

   def init(self):
      self.app = QtWidgets.QApplication(sys.argv)
      self.MainWindow = QtWidgets.QMainWindow()
      self.setupUi(self.MainWindow)

      # connect the callbacks to the buttons from the window
      self.pb_input.clicked.connect(self.pb_input_clicked)
      self.pb_template.clicked.connect(self.pb_template_clicked)
      self.pb_start.clicked.connect(self.pb_start_clicked)
      self.pb_outline.clicked.connect(self.pb_outline_clicked)
      self.pb_new_outline.clicked.connect(self.pb_new_outline_clicked)
      self.pb_up.clicked.connect(lambda state, axis = "y", dir = "sub" : self.pb_dir_clicked(axis, dir))
      self.pb_down.clicked.connect(lambda state, axis = "y", dir = "add" : self.pb_dir_clicked(axis, dir))
      self.pb_left.clicked.connect(lambda state, axis = "x", dir = "sub" : self.pb_dir_clicked(axis, dir))
      self.pb_right.clicked.connect(lambda state, axis = "x", dir = "add" : self.pb_dir_clicked(axis, dir))
      self.pb_rotate.clicked.connect(lambda state, axis = "r", dir = "add" : self.pb_dir_clicked(axis, dir))
      self.list_toEdit.itemClicked.connect(self.selection_changed)

      # show the window
      self.MainWindow.show()
      sys.exit(self.app.exec_())

   def pb_input_clicked(self):
      print("pb_input_clicked")

      # get path to the ticketleo export file
      fname = QFileDialog.getOpenFileName(self.MainWindow, 'Open File', os.path.join(self.cwd, "Samples"), 'Excel Files (*.xlsx)')

      if fname[0] != '':
         self.dataAvailable = True
         self.te_input.setText(fname[0])
         # tell the data browser where to read the file contents
         self.dataBrowser.openExport(fname[0])
         self.creator.setDate(self.dataBrowser.getDate())

         # collect the ammount of total and empty tickets
         self.te_leer.setText("-")
         self.te_leer.setEnabled(False)
         self.tb_anzahl.setText(str(self.dataBrowser.getTicketCnt()))
         self.full_seats  = self.dataBrowser.getTicketCnt()

   def pb_template_clicked(self):
      print("pb_template_clicked")
      fname = QFileDialog.getOpenFileName(self.MainWindow, 'Open File', os.path.join(self.cwd,"Samples"), 'PNG (*.png)')
      if fname[0] != '':
         self.templateAvailable = True
         self.te_template.setText(fname[0])
         self.creator.setBaseImage(fname[0])
         self.update_preview()

   def pb_outline_clicked(self):
      fname = QFileDialog.getOpenFileName(self.MainWindow, 'Open File', os.path.join(self.cwd, "Samples"), 'Settings (*.json)')
      if fname[0] != '':
         self.settingsAvailable = True
         self.te_output.setText(fname[0])
         self.settings.openSettings(fname[0])
         self.creator.setPositions(self.settings)
         self.update_preview()

   def pb_new_outline_clicked(self):
      print("pb_new_outline_clicked clicked")
      fname = QFileDialog.getSaveFileName(self.MainWindow, 'Save File', os.path.join(self.cwd, "Samples"), 'Settigns (*.json)')

      if fname[0] != '':
         self.settingsAvailable = True
         self.settings.createSettings(fname[0])
         self.te_output.setText(fname[0])
         self.creator.setPositions(self.settings)
         self.update_preview()

   def pb_start_clicked(self):
      print("pb_outline_clicked")
      # open file dialog
      fname = QFileDialog.getSaveFileName(self.MainWindow, 'Save File', os.path.join(self.cwd, "Samples"), 'PDF (*.pdf)')

      if fname[0] != '':
         if self.settingsAvailable == True and self.dataAvailable == True and self.templateAvailable == True:
            self.update_status("Reading")
            self.extra_seats = int(self.te_bus.text())
            print("Besetzt: ", self.full_seats)
            print("Blanco: " , self.extra_seats)
            self.creator.setCardsPerPage(int(self.te_x.text()), int(self.te_y.text()))

            # create the tickets
            tickets = []
            for i in range(self.full_seats):
               tickets.append(self.creator.createCard(self.dataBrowser.getCustomer(i)))
               self.update_status(("Creating\n" + str(i) + " of " + str(self.full_seats)))

            for i in range(self.extra_seats):
               tickets.append(self.creator.createBlanco())
               self.update_status(("Creating\n" + str(i) + " of " + str(self.extra_seats)))

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
      if self.settingsAvailable == True and self.templateAvailable == True:
         self.creator.setPositions(self.settings)
         template = self.creator.createCard(("000", "Max Musterman"))
         scaleFactor = template.width / 500
         # convert the picture to pixmap and resize the label
         qim = ImageQt(template)
         pix = QtGui.QPixmap.fromImage(qim)
         self.ticket_preview.resize(template.width / scaleFactor, template.height / scaleFactor)
         self.ticket_preview.setPixmap(QtGui.QPixmap(pix))

   def selection_changed(self, item):
      self.currentSetting = item.text()
      print("selected: ", self.currentSetting)

   def update_status(self, text):
      self.l_status.setText(text)
      self.l_status.adjustSize()
      QApplication.processEvents()


myApp = myMain()
