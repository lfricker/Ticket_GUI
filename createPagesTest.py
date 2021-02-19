import sys
from PIL import Image, ImageFont, ImageDraw
from PIL.ImageQt import ImageQt

print("test creating pages")
# get sample file
empty_ticket = Image.open("Z:/Desktop/Programming Playground/Python Playground/Theater GUI/test.png")


# create the tickets and save them to the given path


# check card ammount in x and y orientation and set parameters
x_cards = 4
y_cards = 4
cards_per_page = x_cards * y_cards
height = empty_ticket.height * y_cards
width  = empty_ticket.width  * x_cards
x_spacing = width / x_cards
y_spacing = height / y_cards


print("Spacing x,y: ", x_spacing, " ", y_spacing)

# check total card ammount
cards_total = 53
# create all cards
cards = []
# TODO
for i in range(cards_total):
   cards.append(empty_ticket)

# get page cnt
pages_total = cards_total / cards_per_page
if(pages_total - int(pages_total) > 0.0):
   pages_total = int(pages_total) + 1
else:
   pages_total = int(pages_total)
print("Pages total: ", pages_total)
# TODO

pages = []
for p in range(pages_total):
   pages.append(Image.new('RGB', (width, height), (255, 255, 255)))
   # save to pages
   for x in range(x_cards):
      for y in range(y_cards):
         # add Card( card, (xpos, ypos))
         current_x = int(x * x_spacing)
         current_y = int(y * y_spacing)
         current_card = p * x_cards * y_cards + x * x_cards + y
         if current_card < cards_total:
            pages[p].paste(cards[current_card], (current_x, current_y), cards[current_card])
   # save page, done with that one, go to next
   print("page done")

# TODO temporary save the pages for debugging
for p in range(pages_total):
   pageName = "Page" + str(p) + ".pdf"
   print(pageName)
   pages[p].save(pageName, dpi=(300, 300))


