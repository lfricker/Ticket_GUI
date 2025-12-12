from PIL import Image, ImageFont, ImageDraw, ImageOps
from PIL.ImageQt import ImageQt
import math

from mySettings import mySettings


class ticketGenerator:

    def __init__(self):
        print("ticketGenerator created")
        self.x_cards = 1
        self.y_cards = 1
        # need to correct from the dpi of the template (300) to the dpi assumed by pil (72)
        self.dpiCorrection = int(300 / 72)
        self.font = ImageFont.truetype("arial", 14 * self.dpiCorrection)
        self.black = (0, 0, 0)
        self.path_to_template = ""

    def setCardsPerPage(self, x, y):
        self.x_cards = x
        self.y_cards = y
        self.cards_per_page = self.x_cards * self.y_cards
        if self.path_to_template != "":
            self.setBaseImage(self.path_to_template)

    def setDate(self, date):
        self.date = date

    def setPositions(self, settings):
        # load the positions from the settings
        positionSettings = settings.getItemValue("positionen")

        # read the x and y positions and the rotation of the name attribute
        nameSettings = positionSettings["name"]
        self.namePosition = (
            int(nameSettings["x"]) * self.dpiCorrection,
            int(nameSettings["y"]) * self.dpiCorrection,
        )
        self.nameRotation = int(nameSettings["r"])
        self.nameCentered = bool(nameSettings["c"])

        # read the x and y positions and the rotation of the platz attribute
        placeSettings = positionSettings["platz"]
        self.platzPosition = (
            int(placeSettings["x"]) * self.dpiCorrection,
            int(placeSettings["y"]) * self.dpiCorrection,
        )
        self.platzRotation = int(placeSettings["r"])
        self.platzCentered = bool(placeSettings["c"])

        # read the x and y positions and the rotation of the date attribute
        dateSettings = positionSettings["datum"]
        self.datePosition = (
            int(dateSettings["x"]) * self.dpiCorrection,
            int(dateSettings["y"]) * self.dpiCorrection,
        )
        self.dateRotation = int(dateSettings["r"])
        self.dateCentered = bool(dateSettings["c"])

    def setBaseImage(self, path_to_img):
        template = Image.open(path_to_img)
        self.path_to_template = path_to_img
        self.height = int(template.height * self.y_cards)
        self.width = int(template.width * self.x_cards)
        self.x_spacing = self.width / self.x_cards
        self.y_spacing = self.height / self.y_cards

    def __add_attribute(
        self, card: Image, text: str, position: tuple, rotation: int, centered: bool
    ):
        # write the value to a temp text to rotate it before adding to the base
        # 800 x 50 is the max size for text fileds... maybe do this according to text size
        # create a dummy drawing canvas to get the needed text box size
        dmy = Image.new("L", (1, 1))
        dmyDraw = ImageDraw.Draw(dmy)
        # get the size of the text to use for centering
        _, _, w, h = dmyDraw.textbbox((0, 0), text, font=self.font)
        # create a new template matching the text size
        textImage = Image.new("L", (w, h))
        draw = ImageDraw.Draw(textImage)
        # add the text to the template image
        draw.text((0, 0), text, font=self.font, fill=255)

        # rotate the text if desired
        if centered:
            # add the centered text
            # if the text is centered use only the y information and center around x
            position = (
                int(((self.width / self.dpiCorrection) / 2) - (w / 2)) + position[0],
                position[1],
            )
            # if the text is centered do not rotate
            textImage = textImage.rotate(0, expand=1)

        else:
            # add the desired rotation to the text. This is only possible if not centered.
            textImage = textImage.rotate(rotation, expand=1)
            # if the text is not centered don't alter the position

        # add the text
        card.paste(
            ImageOps.colorize(textImage, (0, 0, 0), (0, 0, 0)), position, textImage
        )

    def createCard(self, customer):
        # load base image
        print(customer)
        card = Image.open(self.path_to_template)

        # add the data to the ticket and return it
        # set the font size for the base attributes
        self.font = ImageFont.truetype("arial", 14 * self.dpiCorrection)
        self.__add_attribute(
            card=card,
            text=str(customer["name"]),
            position=self.namePosition,
            rotation=self.nameRotation,
            centered=self.nameCentered,
        )
        # set the font size for the date
        self.font = ImageFont.truetype("arial", 9 * self.dpiCorrection)
        self.__add_attribute(
            card=card,
            text=self.date,
            position=self.datePosition,
            rotation=self.dateRotation,
            centered=self.dateCentered,
        )
        # increase the font size for the place to make it better readable
        self.font = ImageFont.truetype("arial", 20 * self.dpiCorrection)
        self.__add_attribute(
            card=card,
            text=str(customer["place"]),
            position=self.platzPosition,
            rotation=self.platzRotation,
            centered=self.platzCentered,
        )
        return card

    def createBlanco(self):
        # load base image and return as blanco card
        card = Image.open(self.path_to_template)
        editable = ImageDraw.Draw(card)
        return card

    # change this function, so that all tickets get placed in stacks instead of on one sheet.
    # therefore place one should be on page one , place 2 on page 2 and so on.

    # if the sorting should be by page, only switch up that the page counter is the outermost loop
    def createOutput(self, tickets, path):
        pages = []
        # get page cnt
        pages_total = len(tickets) / (self.x_cards * self.y_cards)
        pages_total = math.ceil(pages_total)

        # create all pages
        for p in range(pages_total):
            pages.append(Image.new("RGB", (self.width, self.height), (255, 255, 255)))

        current_card = 0
        for y in range(self.y_cards):
            for x in range(self.x_cards):
                current_x = int(x * self.x_spacing)
                current_y = int(y * self.y_spacing)
                for p in range(pages_total):
                    # save to pages
                    if current_card < len(tickets):
                        print(
                            "cardNo: ", current_card, "  p: ", p, "  x: ", x, "  y: ", y
                        )
                        pages[p].paste(
                            tickets[current_card],
                            (current_x, current_y),
                            tickets[current_card],
                        )
                        current_card += 1

        # save output to pdf
        pages[0].save(path, save_all=True, append_images=pages[1:], dpi=(300, 300))

        # close memory intensive objects
        for p in pages:
            p.close()
        del pages[:]

        for t in tickets:
            t.close()
        del tickets[:]
