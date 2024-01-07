from PIL import Image, ImageFont, ImageDraw, ImageOps
from PIL.ImageQt import ImageQt
import math

from mySettings import mySettings

class ticketGenerator():

   def __init__(self):
      print("ticketGenerator created")
      self.x_cards = 1
      self.y_cards = 1
      # need to correct from the dpi of the template (300) to the dpi assumed by pil (72)
      self.dpiCorrection = int(300 / 72)
      self.font = ImageFont.truetype('arial', 14 * self.dpiCorrection)
      self.black = (0,0,0)
      self.path_to_template = ""

   def setCardsPerPage(self, x, y):
      self.x_cards = x
      self.y_cards = y
      self.cards_per_page = self.x_cards * self.y_cards
      if(self.path_to_template != ""):
         self.setBaseImage(self.path_to_template)

   def setDate(self, date):
      self.date = date

   def setPositions(self, positions):
      self.namePos  = (int(positions.getItemValue("positionen")["name"]["x"])  * self.dpiCorrection, int(positions.getItemValue("positionen")["name"]["y"])  * self.dpiCorrection)
      self.platzPos = (int(positions.getItemValue("positionen")["platz"]["x"]) * self.dpiCorrection, int(positions.getItemValue("positionen")["platz"]["y"]) * self.dpiCorrection)
      self.datePos  = (int(positions.getItemValue("positionen")["datum"]["x"]) * self.dpiCorrection, int(positions.getItemValue("positionen")["datum"]["y"]) * self.dpiCorrection)
      self.nameRot =  int(positions.getItemValue("positionen")["name"]["r"]) 
      self.platzRot = int(positions.getItemValue("positionen")["platz"]["r"])
      self.dateRot =  int(positions.getItemValue("positionen")["datum"]["r"])

   def setBaseImage(self, path_to_img):
      template = Image.open(path_to_img)
      self.path_to_template = path_to_img
      self.height = template.height * self.y_cards
      self.width  = template.width  * self.x_cards
      self.x_spacing = self.width  / self.x_cards
      self.y_spacing = self.height / self.y_cards

   def __add_attribute(self, card : Image, value : str, position : tuple, rotation : int):
      # write the value to a temp text to rotate it before adding to the base
      txt = Image.new('L', (800, 50)) # 800 x 50 is the max size for text fileds... maybe do this according to text size
      d = ImageDraw.Draw(txt)
      d.text( (0,0), str(value), font = self.font, fill=255)
      w = txt.rotate(rotation, expand=1)
      card.paste(ImageOps.colorize(w, (0,0,0), (0, 0, 0)), position, w)

   def createCard(self, customer):
      # load base image and make editable
      print(customer)
      card = Image.open(self.path_to_template)
      editable = ImageDraw.Draw(card)
      # add the data to the ticket and return it
      editable.text(self.namePos,  str(customer[1]),  self.black, font = self.font)
      editable.text(self.platzPos, str(customer[0]),  self.black, font = self.font)

      self.__add_attribute(card=card, value=str(customer[1]),  position=self.namePos,  rotation=self.nameRot)
      self.__add_attribute(card=card, value=str(customer[0]),  position=self.platzPos, rotation=self.platzRot)
      self.__add_attribute(card=card, value=self.date,         position=self.datePos,  rotation=self.dateRot)
      return card

   def createBlanco(self):
      # load base image and return as blanco card
      card = Image.open(self.path_to_template)
      editable = ImageDraw.Draw(card)
      return card

   def createOutput(self, tickets, path):
      pages = []
      # get page cnt
      pages_total = len(tickets) / (self.x_cards * self.y_cards)
      pages_total = math.ceil(pages_total)

      for p in range(pages_total):
         pages.append(Image.new('RGB', (self.width, self.height), (255, 255, 255)))
         # save to pages
         for x in range(self.x_cards):
            for y in range(self.y_cards):
               # add Card( card, (xpos, ypos))
               current_x = int(x * self.x_spacing)
               current_y = int(y * self.y_spacing)
               current_card = p * self.x_cards * self.y_cards + x * self.y_cards + y
               if current_card < len(tickets):
                  print("cardNo: ", current_card, "  p: ", p, "  x: ", x, "  y: ", y)
                  pages[p].paste(tickets[current_card], (current_x, current_y), tickets[current_card])

      # save output to pdf
      pages[0].save(path, save_all=True, append_images=pages[1:], dpi=(300,300))

      # close memory intensive objects
      for p in pages:
         p.close()
      del pages[:]

      for t in tickets:
         t.close()
      del tickets[:]
