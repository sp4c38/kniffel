#!/usr/bin/python

import getpass
import pygame
import sys
import time

from modules import window_code, draw_table, utils

from settings import settings

def main():
    pygame.init()
    user = getpass.getuser()

    # ! screen: the pygame window class / window: a own class which keeps general mesurments
    screen, window = window_code.create_window(pygame, settings)
    # window_code.welcome_text(pygame, screen, window, user, settings) # Display a welcome text
    # player_number = window_code.ask_player_number(pygame, screen, window, settings) # How many players are there?
    player_number = 4

    table = draw_table.get_table(window, player_number, settings) # Get table information
    time.sleep(2)
    if settings["window_resizable"]:
        screen = pygame.display.set_mode((window.width, window.height), pygame.RESIZABLE)

    while True:
        window_code.clear_window(pygame, screen, settings)

        events = pygame.event.get()

        # Quit program if the user whishes
        for e in events:
            if e.type == pygame.QUIT:
                print("Quitting program.")
                sys.exit(0)
            if settings["window_resizable"]:
                if e.type == pygame.VIDEORESIZE:
                    screen, window, table = window_code.update_window(pygame, player_number, e, settings)

        draw_table.draw(pygame, screen, table, settings)

        pygame.display.flip()

        time.sleep(1)

        
        

if __name__ == '__main__':
    main()
