# The function which takes care of drawing the information page / and updating it
import random

from lib import utils

class InformationPage:
    def __init__(self, pygame, window, settings):
        # -- main information
        self.start_width = window.table_width # The start width is after the table_width ends
        self.width = window.information_width
        self.height = window.height

        # -- current player section
        self.crt_player_start = 0 # The start height of the current player text
        self.crt_player_height = self.height * settings["crt_player_height"]

        # -- dice section
        class DiceField:
            def __init__(self):
                # dice_level: There are 2 rows. One for showing the dices that you did roll and the other
                #             for showing the dices you selected to keep, to not roll them again.
                self.dice_level = 0

            def set_dice_image(self, dice_image):
                self.dice_image = dice_image
            def set_position(self, position):
                # This attribute is set when the Dice Field is beeing drawed
                self.position = position
            def change_dice_level(self, dice_level):
                self.dice_level = dice_level

        self.dice_section_start = self.crt_player_height # The start height of the dice section (section with only dices, not dice button included)
        self.dice_section_height = self.height * settings["dice_size_maximum"] # The height of the dice section
        self.dice_number = 5 # Normal Kniffel rounds use 5 dices. It would not be a problem to change this number, but isn't a option in the settings file
        self.dice_size = utils.get_dice_size(self.width, self.dice_section_height, self.dice_number)

        self.dice_showings = {} # This array includes the Images to show a certain dice number
        for x in range(min(settings["dice"]), max(settings["dice"])+1):
            image = pygame.image.load(settings["dice"][x]).convert().convert_alpha()
            self.dice_showings[x] = pygame.transform.scale(image, self.dice_size)

        self.dice_fields = [DiceField() for x in range(self.dice_number)] # Dicefields are placeholders for dice showings, a dice field can include max. one dice showing

        # -- dice button section
        self.dice_button_height = self.height * settings["dice_button_height"]
        self.dice_button_color = settings["dice_button_color"]



def get_information_page(pygame, window, settings):
    infopg = InformationPage(pygame, window, settings)
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

    height_pos = utils.center_obj_height(font.get_height(), 1, crt_player_text_size[1])[0]+infopg.crt_player_start
    width_pos = utils.center_obj_width(text.get_width(), 1, crt_player_text_size[0])[0]+infopg.start_width

    screen.blit(text, (width_pos, height_pos))

    return

def draw(pygame, screen, infopg, player, settings):
    draw_dice_button(pygame, screen, infopg, player, settings)
    draw_dice(pygame, screen, infopg, player, settings)
    draw_current_player_text(pygame, screen, infopg, player, settings)
