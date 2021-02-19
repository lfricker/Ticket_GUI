import csv
import pandas as pd


class loadTicketLeoExport():

   def __init__(self):
      self.exportAvailable = False

   def openExport(self, path):
      if self.exportAvailable == False:
         self.exportAvailable = True
      # get the date from the excel
      head = pd.read_excel (path, sheet_name=0).columns[0]
      date = head.split(' ')[3]
      self.date = date.split('.')[0] + '.' + date.split('.')[1] + '.'

      # load excle file. Cut of the first two lines, not needed
      ex = pd.read_excel (path, sheet_name=0, skiprows=2)
      # convert to usable list... excel is... 'special'
      prename = list(ex['Vorname'])
      surname = list(ex['Nachname'])
      seat    = list(ex['Sitznummer'])

      self.customers = []
      for i in range(len(seat)):
         name = str(surname[i]) + " " + str(prename[i])
         if name == "nan nan":
            name = ""
         self.customers.append((seat[i], name))


   def getDate(self):
      if self.exportAvailable:
         return self.date
      else:
         return "00.00."

   def getFullSeats(self):
      if self.exportAvailable:
         full_seats = 0
         for single in self.customers:
            if single[1] != "":
               full_seats = full_seats + 1
         return full_seats
      else:
         return 0

   def getEmptySeats(self):
      if self.exportAvailable:
         empty_seats = 0
         for single in self.customers:
            if single[1] == "":
               empty_seats = empty_seats + 1
         return empty_seats
      else:
         return -1

   def getCustomer(self, index):
      if self.exportAvailable:
         return self.customers[index]
      else:
         return ("", 0)





path = "Z:/Desktop/Programming Playground/Python Playground/Theater/Ticket_Generator/input/Das Klassentreffen-11205 (2).xlsx"

dataloader = loadTicketLeoExport()
dataloader.openExport(path)
print(dataloader.getFullSeats())
print(dataloader.getEmptySeats())