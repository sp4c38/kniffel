import sys
import time

from modules import utils

def create_window(pygame, settings):
    class WindowClass:
        def __init__(self):
            self.width = settings["window_size"][0]
            self.height = settings["window_size"][1]
        def add_sections(self):
            if settings["table_size"] + settings["information_size"] != 1:
                print(f"The total width of the table and the information page must be 1, but is {self.table_width+self.information_width}.")
                sys.exit(1)

            self.table_width = self.width * settings["table_size"]
            self.table_height = self.height
            self.information_width = self.width * settings["information_size"]


    window = WindowClass()
    window.add_sections()
    # Load the window and create it

    print(f"Creating window with size {window.width} x {window.height}")

    if settings["window_resizable"]:
        screen = pygame.display.set_mode((window.width, window.height), pygame.RESIZABLE)
    else:
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

    start_point, summand = utils.center_text_height(pygame, font, welcome_text, window.height)

    line_indicator = 0
    for line in welcome_text:
        line_indicator += 1
        if line_indicator == 1:
            line[0] = line[0].format(user)
        text = font.render(line[0], True, line[1])
        textpos = (utils.center_text_width(pygame, font, line[0], window.width), start_point)
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

    for line in player_text_list:
        text = font.render(line[0], True, line[1])
        textpos = (utils.center_text_width(pygame, font, line[0], window.width), start_point)

        screen.blit(text, textpos)

        start_point += summand

    pygame.display.flip()
    player_number_found = False

    while not player_number_found:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode in [str(x) for x in range(settings["max_players"])]:
                    players_to_play = int(event.unicode)
                    player_number_found = True

                    player_successful = settings["player_number_successful"]
                    font_size = min([utils.get_font_by_size(pygame, spaced_size, line[0], len(player_successful), settings) for line in player_successful]) # Take the font size for the text with the smallest one -> that it looks nice
                    font = pygame.font.Font(settings["font"], font_size)

                    clear_window(pygame, screen, settings)
                    pygame.display.flip()

                    start_point, summand = utils.center_text_height(pygame, font, player_successful, window.height)

                    for line in settings["player_number_successful"]:
                        text = font.render(line[0].format(players_to_play), True, line[1])
                        textpos = (utils.center_text_width(pygame, font, line[0], window.width), start_point)
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

                    start_point, summand = utils.center_text_height(pygame, font, player_unsuccessful, window.height)

                    for line in settings["player_number_unsuccessful"]:
                        text = font.render(line[0], True, line[1])
                        textpos = (utils.center_text_width(pygame, font, line[0], window.width), start_point)
                        screen.blit(text, textpos)

                        start_point += summand
                    
                    pygame.display.flip()


        time.sleep(0.1)
    return players_to_play