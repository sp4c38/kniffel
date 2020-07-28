# The function which takes care of drawing the information page / and updating it
import random

from sp4c38s_kniffel.lib import utils

class Information:
    def __init__(self, pygame, window, settings):
        self.start_width = window.table_width # The width from which on the information section starts (because table section comes before)
        self.width = window.information_width
        self.height = window.height
        self.dice_number = 5 # Normal Kniffel rounds use 5 dices. You could change this number without any errors.

        self.crt_player_height = self.height * settings["crt_player_section_ratio"] # The percentage of the total height for the section which displays which player currently has the turn

        self.dice_section_height = self.height * settings["dice_section_ratio"] # The height of the dice section

        self.level_spacing = self.dice_section_height * settings["dice_section_level_spacing_ratio"]
        self.level_two_starting_height = None # Starting height of the second level
                                              # This is set later during the runtime of the game=
        self.border_radius_ratio = settings["border_radius_ratio"]

        self.dice_size = utils.get_dice_size(self.width, self.dice_section_height - self.level_spacing, self.dice_number, 2)

        self.dice_images = {} # The images for the different possibilities to throw the dice

        for img_index in range(min(settings["dice_images"]), max(settings["dice_images"])+1):
            image = pygame.image.load(settings["dice_images"][img_index]).convert().convert_alpha()
            self.dice_images[img_index] = pygame.transform.scale(image, self.dice_size)

        self.throws_remaining_height = self.height * settings["throws_remain_section_ratio"]

        self.dice_button_height = self.height * settings["dice_button_ratio"]
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
    if player.dices[0].value == None: # If first item has no value/image assigned the dices weren't yet thrown
        return

    if not player.only_one_level: # If multiple levels are active
        # Draw a background which indicates that the dices in the second level are selected
        # to be not thrown in the next round rolling the dices

        background_size = (information_sec.width, information_sec.dice_size[1] + information_sec.level_spacing / 2)

        background = pygame.Rect(information_sec.start_width, information_sec.level_two_starting_height - (information_sec.level_spacing / 4), # Divided through 4 because only is allowed to use half of the size of a spacing
                                 background_size[0], background_size[1])

        pygame.draw.rect(screen, (188, 52, 52), background,
                         border_radius = int((background_size[0] / background_size[1]) * information_sec.border_radius_ratio))

    for dice in player.dices:
        dicepos = (dice.position.left, dice.position.top)

        screen.blit(dice.image, dicepos)

    return

def draw_throws_left(pygame, screen, information_sec, player, settings):
    throws_remaining_size = (information_sec.width, information_sec.throws_remaining_height)

    spaced_size = (throws_remaining_size[0] * (1-settings["space_left_right"]), throws_remaining_size[1] * (1-settings["space_top_bottom"])) # The size of the button reduced to make the text look good

    text = settings["throws_remain_text"]

    font_size = min([utils.get_font_by_size(pygame, spaced_size, line[0], len(text), settings) for line in text])
    font = pygame.font.Font(settings["font"], font_size)

    start_height, spacing = utils.center_obj_height(font.size(text[0][0])[1], len(text), throws_remaining_size[1])
    start_height += information_sec.crt_player_height + information_sec.dice_section_height

    for line in text:
        text = font.render(line[0].format(player.throws), True, line[1])

        width_pos = utils.center_obj_width(font.size(line[0])[0], 1, throws_remaining_size[0])[0] + information_sec.start_width
        textpos = (width_pos, start_height)

        screen.blit(text, textpos)

        start_height += spacing

def draw_dice_button(pygame, screen, information_sec, player, settings):
    dice_button_size = (information_sec.width, information_sec.dice_button_height)

    pygame.draw.rect(screen, information_sec.dice_button_color, information_sec.dice_button_rect,
                     border_radius=int((dice_button_size[0]/dice_button_size[1])*information_sec.border_radius_ratio)) # surface, color, rectangle, border_radius

    spaced_size = (dice_button_size[0] * (1-settings["space_left_right"]), dice_button_size[1] * (1-settings["space_top_bottom"])) # The size of the button reduced to make the text look good

    button_text = settings["dice_button_text"]
    font_size = min([utils.get_font_by_size(pygame, spaced_size, line[0], len(button_text), settings) for line in button_text])
    font = pygame.font.Font(settings["font"], font_size)

    start_height, spacing = utils.center_obj_height(font.size(button_text[0][0])[1], len(button_text), dice_button_size[1])
    start_height += information_sec.height - dice_button_size[1] # Add to not intervene with previouse sections in height
                                                                 # Subtract because always shall be on bottom edge

    for line in button_text:
        text = font.render(line[0], True, line[1])

        width_pos = utils.center_obj_width(font.size(line[0])[0], 1, dice_button_size[0])[0] + information_sec.start_width
        textpos = (width_pos, start_height)

        screen.blit(text, textpos)

        start_height += spacing

    return

def draw(pygame, screen, information_sec, player, settings):
    draw_current_player_text(pygame, screen, information_sec, player, settings)
    draw_dices(pygame, screen, information_sec, player, settings)
    draw_throws_left(pygame, screen, information_sec, player, settings)
    draw_dice_button(pygame, screen, information_sec, player, settings)
