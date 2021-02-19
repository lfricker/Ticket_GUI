from mainWindow import Ui_MainWindow
from mySettings import mySettings
from loadTicketLeoExport import loadTicketLeoExport
from ticketGenerator import ticketGenerator
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys
from PIL import Image, ImageFont, ImageDraw
from PIL.ImageQt import ImageQt


class myMain(Ui_MainWindow):

   def __init__(self):
      super(myMain, self).__init__()
      self.settings = mySettings()
      self.creator = ticketGenerator()
      self.creator.setDate("00.00.")
      self.dataBrowser = loadTicketLeoExport()
#      self.creator.setCardsPerPage(4,4)
      self.creator.setCardsPerPage(3,5)
      self.empty_seats = 0
      self.full_seats  = 0
      self.extra_seats = 0
      self.currentSetting = "name"
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
      self.pb_up.clicked.connect(self.pb_up_clicked)
      self.pb_down.clicked.connect(self.pb_down_clicked)
      self.pb_left.clicked.connect(self.pb_left_clicked)
      self.pb_right.clicked.connect(self.pb_right_clicked)

      # show the window
      self.MainWindow.show()
      sys.exit(self.app.exec_())


   def pb_input_clicked(self):
      print("pb_input_clicked")

      # get path to the ticketleo export file
      fname = QFileDialog.getOpenFileName(self.MainWindow, 'Open File', self.te_input.toPlainText(), 'Excel Files (*.xlsx)')

      if fname[0] != '':
         self.te_input.setText(fname[0])
         # tell the data browser where to read the file contents
         self.dataBrowser.openExport(fname[0])
         self.creator.setDate(self.dataBrowser.getDate())

         # collect the ammount of total and empty tickets
         self.te_leer.setText(str(self.dataBrowser.getEmptySeats()))
         self.empty_seats = self.dataBrowser.getEmptySeats()
         self.tb_anzahl.setText(str(self.dataBrowser.getFullSeats()))
         self.full_seats  = self.dataBrowser.getFullSeats()


   def pb_template_clicked(self):
      print("pb_template_clicked")

      fname = QFileDialog.getOpenFileName(self.MainWindow, 'Open File', './Theater GUI/Samples', 'PNG (*.png)')

      if fname[0] != '':
         self.te_template.setText(fname[0])
         self.creator.setBaseImage(fname[0])
         self.update_preview()


   def pb_outline_clicked(self):
      fname = QFileDialog.getOpenFileName(self.MainWindow, 'Open File', './Theater GUI/Samples', 'Settings (*.json)')
      if fname[0] != '':
         self.te_output.setText(fname[0])
         self.settings.openSettings(fname[0])
         self.creator.setPositions(self.settings)


   def pb_start_clicked(self):
      print("pb_outline_clicked")
      # open file dialog
      fname = QFileDialog.getSaveFileName(self.MainWindow, 'Save File', './Theater GUI/Samples', 'PDF (*.pdf)')

      if fname[0] != '':
         self.l_status.setText("Einlesen")
         self.extra_seats = int(self.te_bus.toPlainText())
         print("Besetzt: ", self.full_seats)
         print("Frei: "   , self.empty_seats)
         print("Bus: "    , self.extra_seats)
         self.creator.setCardsPerPage(int(self.te_x.toPlainText()), int(self.te_y.toPlainText()))

         # create the tickets
         tickets = []
         for i in range(self.empty_seats + self.full_seats):
            tickets.append(self.creator.createCard(self.dataBrowser.getCustomer(i)))
         for i in range(self.extra_seats):
            customer = ("Bus " + str(i+1), "")
            tickets.append(self.creator.createCard(customer))
         self.l_status.setText("Creating")

         # save the tickets
         self.creator.createOutput(tickets, fname[0])


         self.l_status.setText("Fertig")


   def pb_new_outline_clicked(self):
      print("pb_new_outline_clicked clicked")
      fname = QFileDialog.getSaveFileName(self.MainWindow, 'Save File', './Theater GUI/Samples', 'Settigns (*.json)')

      if fname[0] != '':
         self.settings.createSettings(fname[0])

   def pb_up_clicked(self):
      print("pb_up clicked")
      self.settings.setItemValue("positionen", self.settings.getItemValue("positionen")[self.currentSetting]["x"] + int(self.te_step.toPlainText()))
      self.update_preview()

   def pb_down_clicked(self):
      print("pb_down clicked")
      self.settings.setItemValue("positionen", self.settings.getItemValue("positionen")[self.currentSetting]["x"] - int(self.te_step.toPlainText()))
      self.update_preview()

   def pb_left_clicked(self):
      print("pb_left clicked")
      self.settings.setItemValue("positionen", self.settings.getItemValue("positionen")[self.currentSetting]["y"] - int(self.te_step.toPlainText()))
      self.update_preview()

   def pb_right_clicked(self):
      print("pb_right clicked")
      self.settings.setItemValue("positionen", self.settings.getItemValue("positionen")[self.currentSetting]["y"] + int(self.te_step.toPlainText()))
      self.settings.saveSettings()
      self.update_preview()

   def update_preview(self):
      self.creator.setPositions(self.settings)
      template = self.creator.createCard(("000", "Max Musterman"))
      scaleFactor = template.width / 500

      # convert the picture to pixmap and resize the label
      qim = ImageQt(template)
      pix = QtGui.QPixmap.fromImage(qim)
      self.ticket_preview.resize(template.width / scaleFactor, template.height / scaleFactor)
      self.ticket_preview.setPixmap(QtGui.QPixmap(pix))



myApp = myMain()

input("prompt: ")