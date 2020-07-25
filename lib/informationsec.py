# The function which takes care of drawing the information page / and updating it
import random

from lib import utils

class Information:
    def __init__(self, pygame, window, settings):
        self.start_width = window.table_width # The width from which on the information section starts (because table section comes before)
        self.width = window.information_width
        self.height = window.height

        self.crt_player_height = self.height * settings["crt_player_section_height"] # The percentage of the total height for the section which displays which player currently has the turn

        self.dice_section_start = self.crt_player_height # The start height of the dice section (needed because current player section is before)
        self.dice_section_height = self.height * settings["dice_size_maximum"] # The height of the dice section
        self.dice_number = 5 # Normal Kniffel rounds use 5 dices. You could change this number without any errors.

        self.dice_size = utils.get_dice_size(self.width, self.dice_section_height, self.dice_number)

        self.dice_images = {} # The images for the different possibilities to throw the dice

        for img_index in range(min(settings["dice_images"]), max(settings["dice_images"])+1):
            image = pygame.image.load(settings["dice_images"][img_index]).convert().convert_alpha()
            self.dice_images[img_index] = pygame.transform.scale(image, self.dice_size)

        self.dice_button_height = self.height * settings["dice_button_height"]
        self.dice_button_color = settings["dice_button_color"]
        self.dice_button_rect = pygame.Rect(self.start_width, self.height - self.dice_button_height, self.width, self.dice_button_height) # left, top, width, height


def create(pygame, window, settings):
    # Init the Information class with important attributes for drawing the information section later

    information_sec = Information(pygame, window, settings)
    return information_sec

def draw_current_player_text(pygame, screen, information_sec, player, settings):
    # Draws text which shows which player has the turn

    player_text = settings["current_player_text"]
    player_text_size = (information_sec.width, information_sec.crt_player_height)
    spaced_size = (player_text_size[0] * (1-settings["space_left_right"]), player_text_size[1] * (1-settings["space_top_bottom"]))

    font_size = min(utils.get_font_by_size(pygame, spaced_size, line[0], len(player_text), settings) for line in player_text)
    font = pygame.font.Font(settings["font"], font_size)

    start_height, spacing = utils.center_obj_height(font.size(player_text[0][0])[1], len(player_text), player_text_size[1])

    for line in player_text:
        line_text = line[0].format(player.name) # Formated with the name of the player
        text = font.render(line_text, True, line[1])

        width_pos = utils.center_obj_width(font.size(line_text)[0], 1, player_text_size[0])[0] + information_sec.start_width
        textpos = (width_pos, start_height)

        start_height += spacing

        screen.blit(text, textpos)

    return


def draw_dices(pygame, screen, information_sec, player, settings):
    if player.dices[0].image == None: # If first item has no value/image assigned the dices weren't yet thrown
        return

    for dice in player.dices:
        dicepos = (dice.rectangle.left, dice.rectangle.top)

        screen.blit(dice.image, dicepos)

    return

def draw_dice_button(pygame, screen, information_sec, player, settings):
    dice_button_size = (information_sec.width, information_sec.dice_button_height)
    pygame.draw.rect(screen, information_sec.dice_button_color, information_sec.dice_button_rect) # surface, color, rectangle

    spaced_size = (dice_button_size[0] * (1-settings["space_left_right"]), dice_button_size[1] * (1-settings["space_top_bottom"])) # The size of the button reduced to make the text look good

    button_text = settings["dice_button_text"]
    font_size = min([utils.get_font_by_size(pygame, spaced_size, line[0], len(button_text), settings) for line in button_text])
    font = pygame.font.Font(settings["font"], font_size)

    start_height, spacing = utils.center_obj_height(font.size(button_text[0][0])[1], len(button_text), dice_button_size[1])

    for line in button_text:
        text = font.render(line[0], True, line[1])

        width_pos = utils.center_obj_width(font.size(line[0])[0], 1, dice_button_size[0])[0] + information_sec.dice_button_rect.left
        textpos = (width_pos, information_sec.dice_button_rect.top + start_height)

        screen.blit(text, textpos)

        start_height += spacing

    return

def draw(pygame, screen, information_sec, player, settings):
    draw_current_player_text(pygame, screen, information_sec, player, settings)
    draw_dices(pygame, screen, information_sec, player, settings)
    draw_dice_button(pygame, screen, information_sec, player, settings)
