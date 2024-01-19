import csv
import re
import pandas as pd


class loadTicketLeoExport:

   def __init__(self):
      self.exportAvailable = False

   def openExport(self, path):
      try:
         # get the date from the excel sheet
         # load the file with pandas to only extract the first row
         df = pd.read_excel (path, sheet_name=0).columns[0]
         self.date = str(re.findall("\d{2}.\d{2}.\d{4}", df)[0])

         # load excle file. Cut of the first two lines, because our indexes are in the third line
         df = pd.read_excel (path, sheet_name=0, skiprows=2)

         self.customers = []
         # interate the df and create the customers
         for idx, row in df.iterrows():
            if pd.isna(row['Nachname']): # if there is no surname skip the entry
               continue
            # check if a prename is present. If not only use the surename
            if pd.isna(row['Vorname']):
               name = row['Nachname']
            else:
               name = row['Vorname'] + " " + row['Nachname']
            self.customers.append((row['Sitznummer'], name, row['Nachname']))

         # sort the list by name to get better sorting when creating print tickets
         # here is determined in which order the tickets will be printed later. So sort carefully
         self.customers = sorted(self.customers, key=lambda x : x[2])

         self.exportAvailable = True # if the parsing was successful the export can be used
      except Exception as e:
         print(type(e), e)
         self.exportAvailable = False # if something went wrong mark as not available


   def getDate(self):
      if self.exportAvailable:
         return self.date
      else:
         return "00.00."

   def getTicketCnt(self):
      if self.exportAvailable:
         full_seats = 0
         for single in self.customers:
            if single[1] != "":
               full_seats = full_seats + 1
         return full_seats
      else:
         return 0

   def getCustomer(self, index):
      if self.exportAvailable:
         try:
            return self.customers[index]
         except IndexError as e:
            print("Customer selection out of range")
            return None
      else:
         return ("", 0)



if __name__ == "__main__":
   import os
   sample_path = os.path.join(os.getcwd(), "Samples", "Das-Klassentreffen.xlsx")

   loader = loadTicketLeoExport()
   loader.openExport(sample_path)

   print(loader.getTicketCnt())
   print(loader.getDate())