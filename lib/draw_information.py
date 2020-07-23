# The function which takes care of drawing the information page / and updating it
import random

from lib import utils

class Information:
    def __init__(self, pygame, window, settings):
        self.start_width = window.table_width # The width from which on the information section starts (because table section comes before)
        self.width = window.information_width
        self.height = window.height

        self.crt_player_height = self.height * settings["crt_player_section_height"] # The percentage of the total height for the section which displays which player currently has the turn

        class DiceField:
            # This class is created and stored for each single dice to control there level, image and position
            def __init__(self):
                # In Kniffel you can roll the dice and than put aside some of the rolled dices
                # When dices are put aside they must be drawn in an extra row
                # To indicate in which row the dice currently is dice_level is used.
                # 0 means that it can be rolled again and 1 means that it was put aside
                self.dice_level = 0

            def set_dice_image(self, dice_image):
                self.dice_image = dice_image
            def set_position(self, position):
                self.position = position
            def change_dice_level(self, dice_level):
                self.dice_level = dice_level

        self.dice_section_start = self.crt_player_height # The start height of the dice section (needed because current player section is before)
        self.dice_section_height = self.height * settings["dice_size_maximum"] # The height of the dice section
        self.dice_number = 5 # Normal Kniffel rounds use 5 dices. You could change this number without any errors.
        self.dice_size = utils.get_dice_size(self.width, self.dice_section_height, self.dice_number)

        self.dice_images = {} # The images for the different possibilities to throw the dice

        for img_index in range(min(settings["dice_images"]), max(settings["dice_images"])+1):
            image = pygame.image.load(settings["dice_images"][img_index]).convert().convert_alpha()
            self.dice_images[img_index] = pygame.transform.scale(image, self.dice_size)

        self.dice_fields = [DiceField() for x in range(self.dice_number)]

        self.dice_button_height = self.height * settings["dice_button_height"]
        self.dice_button_color = settings["dice_button_color"]



def get_information(pygame, window, settings):
    # Init the Information class with important attributes for drawing the information section later

    infopg = Information(pygame, window, settings)
    return infopg

def draw_dice(pygame, screen, infopg, player, settings):
    if not player.current_dices:
        return

    player_dices = [infopg.dice.dice[x] for x in sorted(player.current_dices)]

    start_point, summmand = utils.center_obj_width(pygame, infopg.dice_size[0], infopg.dices, infopg.width)
    height_point = utils.center_obj_height(pygame, infopg.dice_size[1], 1, infopg.dice_section_height)[0] + infopg.dice_section_start

    for d in player_dices:
        dice = pygame.transform.scale(d, (int(infopg.dice_size[0]), int(infopg.dice_size[1])))
        dicepos = (infopg.start_width + start_point, height_point)

        screen.blit(dice, dicepos)

        start_point += summmand

    return

def draw_dice_button(pygame, screen, infopg, player, settings):
    dice_button_size = (infopg.width, infopg.dice_button_height)
    pygame.draw.rect(screen, infopg.dice_button_color, player.dice_button_rect) # surface, color, rectangle

    spaced_size = (dice_button_size[0]*(1-settings["space_left_right"]), dice_button_size[1]*(1-settings["space_top_bottom"])) # The size of the button reduced to make the text look good

    dice_btn_text = settings["dice_button_text"]
    font_size = min([utils.get_font_by_size(pygame, spaced_size, name[0], len(dice_btn_text), settings) for name in dice_btn_text])
    font = pygame.font.Font(settings["font"], font_size)

    start_point, summand = utils.center_obj_height(font.get_height(), len(dice_btn_text), dice_button_size[1])

    for name in dice_btn_text:
        text = font.render(name[0], True, name[1])
        textpos = (utils.center_obj_width(text.get_width(), 1, dice_button_size[0])[0]+player.dice_button_rect.left, player.dice_button_rect.top+start_point)

        screen.blit(text, textpos)

        start_point += summand

    return

def draw_current_player_text(pygame, screen, infopg, player, settings):
    # This draws a text, to indicate which player has the turn
    crt_player_text = (settings["crt_player_text"][0].format(player.player_name), settings["crt_player_text"][1])
    crt_player_text_size = (infopg.width, infopg.crt_player_height)
    spaced_size = (crt_player_text_size[0]*(1-settings["space_left_right"]), crt_player_text_size[1]*(1-settings["space_top_bottom"]))

    font_size = utils.get_font_by_size(pygame, spaced_size, crt_player_text[0], 1, settings)
    font = pygame.font.Font(settings["font"], font_size)
    text = font.render(crt_player_text[0], True, crt_player_text[1])

    height_pos = utils.center_obj_height(font.get_height(), 1, crt_player_text_size[1])[0]
    width_pos = utils.center_obj_width(text.get_width(), 1, crt_player_text_size[0])[0]+infopg.start_width

    screen.blit(text, (width_pos, height_pos))

    return

def draw(pygame, screen, infopg, player, settings):
    draw_dice_button(pygame, screen, infopg, player, settings)
    draw_dice(pygame, screen, infopg, player, settings)
    draw_current_player_text(pygame, screen, infopg, player, settings)
