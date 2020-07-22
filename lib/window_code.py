import sys
import time

from lib import utils, draw_table, information

class WindowClass:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def add_player_number(self, player_num):
        self.player_number = player_num

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

    screen = pygame.display.set_mode((window.width, window.height))

    pygame.display.set_caption(settings["window_name"]) # Set a window caption

    screen.fill(settings["bg_color"])
    pygame.display.flip() # Update the window

    print(f"Created window with size {window.width}px x {window.height}px!")

    return screen, window

def clear_window(pygame, screen, settings):
    # Replace the window with the background color
    screen.fill(settings["bg_color"])

def welcome_text(pygame, screen, window, user, settings):
    # Display a welcome text

    clear_window(pygame, screen, settings)

    spaced_size = (window.width*(1-settings["space_left_right"]), window.height*(1-settings["space_top_bottom"])) # The size of the window reduced to make the text look good

    welcome_text = settings["welcome_text"]

    font_size = min([utils.get_font_by_size(pygame, spaced_size, line[0], len(welcome_text), settings) for line in welcome_text])
    font = pygame.font.Font(settings["font"], font_size)

    start_height, spacing = utils.center_obj_height(font.size(welcome_text[0][0])[1], len(welcome_text), window.height)

    line_counter = 1
    for line in welcome_text:
        if line_counter == 1: # For personal greeting insert the user name
            line[0] = line[0].format(user)

        text = font.render(line[0], True, line[1])
        textpos = (utils.center_obj_width(font.size(line[0])[0], 1, window.width)[0], start_height) # The position of the text
        print(textpos)
        print(spaced_size)
        screen.blit(text, textpos) # Add the text to the screen at textpos

        start_height += spacing # Increase start_height for the next line
        line_counter += 1


    for x in range(2): # Must do 2 times because of a pygame problem on macos
        pygame.event.get()
        pygame.display.flip()

    time.sleep(5)

    return

def ask_player_number(pygame, screen, window, settings):
    clear_window(pygame, screen, settings)

    spaced_size = (window.width*(1-settings["space_left_right"]), window.height*(1-settings["space_top_bottom"]))

    player_text = settings["player_number_text"]

    font_size = min([utils.get_font_by_size(pygame, spaced_size, line[0], len(player_text), settings) for line in player_text])
    font = pygame.font.Font(settings["font"], font_size)

    start_point, spacing = utils.center_obj_height(font.size(player_text[0][0])[1], len(player_text), window.height)

    for line in player_text:
        line[0] = line[0].format(settings["max_players"])
        text = font.render(line[0], True, line[1])
        textpos = (utils.center_obj_width(font.size(line[0])[0], 1, window.width)[0], start_point)

        screen.blit(text, textpos)

        start_point += spacing

    pygame.display.flip()
    is_successful = False

    while not is_successful:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.unicode in [str(x) for x in range(settings["max_players"]+1) if not x in [0, 1]]:
                    players_to_play = int(event.unicode)
                    player_state = settings["player_number_successful"]
                    is_successful = True
                else:
                    player_state = settings["player_number_unsuccessful"]
                    is_successful = False

                font_size = min([utils.get_font_by_size(pygame, spaced_size, line[0], len(player_state), settings) for line in player_state])
                font = pygame.font.Font(settings["font"], font_size)

                clear_window(pygame, screen, settings)

                start_point, spacing = utils.center_obj_height(font.size(player_state[0][0])[1], len(player_state), window.height)

                for line in player_state:
                    if is_successful:
                        text = font.render(line[0].format(players_to_play), True, line[1])
                    elif not is_successful:
                        text = font.render(line[0].format(settings["max_players"]), True, line[1])

                    textpos = (utils.center_obj_width(font.size(line[0])[0], 1, window.width)[0], start_point)
                    screen.blit(text, textpos)


                    start_point += spacing

                for x in range(2): # Must do 2 times because of a pygame problem on macos
                    pygame.event.get()
                    pygame.display.flip()

                if is_successful:
                    time.sleep(4)
                elif not is_successful:
                    time.sleep(settings["update_time"])


        time.sleep(0.1)
    return players_to_play

def play_music(pygame, settings):
    music = pygame.mixer.music.load(settings["music"])
    pygame.mixer.music.play(loops=-1) # -1 is indefinitely
    return

def set_window_icon(pygame, settings):
    icon = pygame.image.load(settings["screen_favicon"])
    pygame.display.set_icon(icon)
