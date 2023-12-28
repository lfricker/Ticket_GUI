import json

class mySettings():

   def __init__(self):
      print("mySettings Class created, ready to use")
      self.settingsAvailable = False

   def openSettings(self, path):
      if self.settingsAvailable == False:
         self.settingsAvailable = True
         #open the file
         print("Reading settings from ", path)
         self.path = path
         with open(path) as settingsFile:
            self.settings = json.load(settingsFile)

   def getItemValue(self, item):
      if self.settingsAvailable:
         # search for the item and return
         print ("Searching for ", item)
         print(self.settings[item])
         return self.settings[item]
      else:
         return 0

   def setItemValue(self, item, val):
      if self.settingsAvailable:
         self.settings[item] = val
         print("setting new value for", item)


   def saveSettings(self):
      if self.settingsAvailable:
         with open(self.path, 'w') as outfile:
            json.dump(self.settings, outfile, indent=4)

   def createSettings(self, path):
      self.path = path
      # create the settings structure
      newSettings = {
                        "veranstalter": "",
                        "veranstaltung": "",
                        "positionen":  {
                           "name": {
                              "x": 0,
                              "y": 0,
                              "r": 0
                           },
                           "platz": {
                              "x": 0,
                              "y": 0,
                              "r": 0
                           },
                           "datum": {
                              "x": 0,
                              "y": 0,
                              "r": 0
                           }
                        }
                     }
      with open(path, 'w') as outfile:
         json.dump(newSettings, outfile, indent=4)
      self.openSettings(path)