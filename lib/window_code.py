import sys
import time

from lib import utils, draw_table, information

class WindowClass:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def add_arrangement(self, settings):
        if settings["table_ratio"] + settings["information_ratio"] != 1:
            # Check ratios for correct sizes

            print(f"\033[{settings['error_color']}mERROR:")
            print(f"The table takes {settings['table_ratio']*100}% and the information section takes {settings['information_ratio']*100}% of the total width.\n"
                   f"The maximal width allowed is 100%, but it's {settings['table_ratio']*100 + settings['information_ratio']*100}%.\033[0m")

            sys.exit(1)

        self.table_width = self.width * settings["table_ratio"]
        self.information_width = self.width * settings["information_ratio"]

def update_window(pygame, player_number, event, settings):
    new_size = event.size
    window = WindowClass(new_size[0], new_size[1])
    window.add_arrangement(settings)
    screen = pygame.display.set_mode((window.width, window.height), pygame.RESIZABLE)
    screen.fill(settings["bg_color"])
    table = draw_table.get_table(window, player_number, settings)
    information_page = information.get_information_page(pygame, window, settings)

    return screen, window, table, information_page

def create_window(pygame, settings):

    window = WindowClass(settings["window_size"][0], settings["window_size"][1])
    window.add_arrangement(settings)
    # Load the window and create it

    print(f"Creating window with size {window.width} x {window.height}")

    screen = pygame.display.set_mode((window.width, window.height))

    pygame.display.set_caption(settings["window_name"])

    screen.fill(settings["bg_color"])
    pygame.display.flip()

    return screen, window

def clear_window(pygame, screen, settings):
    # Replace the window with the background color
    screen.fill(settings["bg_color"])

def welcome_text(pygame, screen, window, user, settings):
    # Display a welcome text
    clear_window(pygame, screen, settings)

    spaced_size = (window.width*(1-settings["space_left_right"]), window.height*(1-settings["space_top_bottom"])) # The size of the window reduced to make the text look good
    print(f"Welcome {user}")

    welcome_text = settings["welcome_text"]

    font_size = min([utils.get_font_by_size(pygame, spaced_size, line[0], len(welcome_text), settings) for line in welcome_text]) # Take the font size for the text with the smallest one -> that it looks nice
    font = pygame.font.Font(settings["font"], font_size)

    start_point, summand = utils.center_text_height(pygame, font, len(welcome_text), window.height)

    line_indicator = 0
    for line in welcome_text:
        line_indicator += 1
        if line_indicator == 1:
            line[0] = line[0].format(user)
        text = font.render(line[0], True, line[1])
        textpos = (utils.center_text_width(pygame, text, window.width), start_point)
        screen.blit(text, textpos)

        start_point += summand

    pygame.display.flip()
    time.sleep(5)

    return

def ask_player_number(pygame, screen, window, settings):
    clear_window(pygame, screen, settings)
    spaced_size = (window.width*(1-settings["space_left_right"]), window.height*(1-settings["space_top_bottom"])) # The size of the window reduced to make the text look good
    print("How many players are there?")

    player_text_list = settings["player_number_text"]

    font_size = min([utils.get_font_by_size(pygame, spaced_size, line[0], len(player_text_list), settings) for line in player_text_list]) # Take the font size for the text with the smallest one -> that it looks nice
    font = pygame.font.Font(settings["font"], font_size)

    start_point, summand = utils.center_text_height(pygame, font, len(player_text_list), window.height)

    line_counter = 0
    for line in player_text_list:
        line_counter += 1
        if line_counter == 2:
            line[0] = line[0].format(settings["max_players"])
        text = font.render(line[0], True, line[1])
        textpos = (utils.center_text_width(pygame, text, window.width), start_point)

        screen.blit(text, textpos)

        start_point += summand

    pygame.display.flip()
    player_number_found = False

    while not player_number_found:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.unicode in [str(x) for x in range(settings["max_players"]+1) if not x in [0, 1]]:
                    players_to_play = int(event.unicode)
                    player_number_found = True
                    print(f"{players_to_play} players are playing.")
                    player_successful = settings["player_number_successful"]
                    font_size = min([utils.get_font_by_size(pygame, spaced_size, line[0], len(player_successful), settings) for line in player_successful]) # Take the font size for the text with the smallest one -> that it looks nice
                    font = pygame.font.Font(settings["font"], font_size)

                    clear_window(pygame, screen, settings)
                    pygame.display.flip()

                    start_point, summand = utils.center_text_height(pygame, font, len(player_successful), window.height)

                    for line in settings["player_number_successful"]:
                        text = font.render(line[0].format(players_to_play), True, line[1])
                        textpos = (utils.center_text_width(pygame, text, window.width), start_point)
                        screen.blit(text, textpos)
                        pygame.display.flip()

                        start_point += summand

                    time.sleep(3)

                else:
                    player_unsuccessful = settings["player_number_unsuccessful"]
                    font_size = min([utils.get_font_by_size(pygame, spaced_size, line[0], len(player_unsuccessful), settings) for line in settings["player_number_unsuccessful"]]) # Take the font size for the text with the smallest one -> that it looks nice
                    font = pygame.font.Font(settings["font"], font_size)

                    clear_window(pygame, screen, settings)
                    pygame.display.flip()

                    start_point, summand = utils.center_text_height(pygame, font, len(player_unsuccessful), window.height)

                    line_counter = 0
                    for line in player_unsuccessful:
                        line_counter += 1
                        if line_counter == 2:
                            line[0] = line[0].format(settings["max_players"])
                        text = font.render(line[0], True, line[1])
                        textpos = (utils.center_text_width(pygame, text, window.width), start_point)
                        screen.blit(text, textpos)

                        start_point += summand

                    pygame.display.flip()


        time.sleep(0.1)
    return players_to_play

def play_music(pygame, settings):
    music = pygame.mixer.music.load(settings["music"])
    pygame.mixer.music.play(loops=-1) # -1 is indefinitely
    return

def set_window_icon(pygame, settings):
    icon = pygame.image.load(settings["screen_favicon"])
    pygame.display.set_icon(icon)
