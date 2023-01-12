# Ticket Class
# All Tickets should have same Positions for Attributes but different attribute value
# For example: all names at the same Positions, but each name value is different
# number of attributes should be variable

import random as rand

class Info:
   def __init__(self, value = "", position = {0,0}, visibility = False):
      self.position = position
      self.value = value
      self.visibility = visibility
   
   def __repr__(self):
      return self.value + " at: " + str(self.position)


class Ticket:

   # path to background image
   background = ""
   # list of attributes and their positions
   fields = []

   def __init__(self):
      # create dictionary to store the values
      self.values = {}
      for field in self.fields:
         self.values[field.value] = ""

   def __repr__(self):
      return "Ticket->"

   # adds a new field for all Tickets, that can be used from there on
   def addField(self, name, position):
      self.fields.append(Info(name, position, True))

   def populate(self, items):
      for i in items:
         key, = i.keys()
         self.values[key] = i[key]


   def render(self):
      # load background image and place attributes on it
      for info in self.fields:
         if info.visibility:
            pass
            print(self.values[info.value] + " @ " + str(info.position))



if __name__ == "__main__":

   Ticket.addField(Ticket, "name", {10,30})
   Ticket.addField(Ticket, "datum", {30, 30})
   Ticket.addField(Ticket, "sitz", {50,30})

   test = []
   for i in range(10):
      nT = Ticket()
      nT.populate([{"name": "Luka Fricker"}, {"datum":"01.01.2022"}, {"sitz":str(rand.randint(0, 200))}])
      test.append(nT)

   for tick in test:
      tick.render()
