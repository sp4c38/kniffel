#!/usr/bin/python

import getpass
import pygame
import random
import sys
import time

from lib import window_code, utils, draw_table, draw_information, player

from etc.settings import settings

def main():
    verbose = False

    if "-v" in sys.argv:
        # When verbose output is enabled extra information about the game are outputed
        verbose = True

    pygame.init()
    user = getpass.getuser()

    window_code.set_window_icon(pygame, settings)

    # screen: the pygame window class / window: a own class which keeps general measurements
    screen, window = window_code.create_window(pygame, settings)
    if verbose: print(f"Initialized the window with size {window.width}px x {window.height}px.")

    #window_code.welcome_text(pygame, screen, window, user, settings) # Display a welcome text

    #player_number = window_code.ask_player_number(pygame, screen, window, settings) # How many players are there?
    player_number = 2
    window.add_player_number(player_number)
    if verbose: print(f"{player_number} players are going to play Kniffel!")

    table_sec = draw_table.get_table(window, player_number, settings) # Get table class (with table attributes)
    information_sec = draw_information.get_information(pygame, window, settings)
    if verbose: print("Calculated table and information section sizes.")
    sys.exit()
    players = player.init_players(pygame, player_number, information_sec, table_sec, window) # A list which stores player progress information

    if settings["play_music"]:
        window_code.play_music(pygame, settings)

    if settings["window_resizable"]:
        screen = pygame.display.set_mode((window.width, window.height), pygame.RESIZABLE)

    current_player = player.get_current_player(player.next_player(players, None)) # Get the inital/first player (who starts)

    while True:
        window_code.clear_window(pygame, screen, settings)

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                # Quit program if the user whishes
                print("Closing program. Until next time.")
                sys.exit(0)
            if settings["window_resizable"]:
                if e.type == pygame.VIDEORESIZE:
                    print("Window resized. Recalculating sizes.")
                    screen, window, table_sec, information_sec = window_code.update_window(pygame, player_number, e, settings)
                    players = player.recalculate_positions(pygame, players, table_sec, information_sec)
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1: # A left-click on the mouse
                    # This changes the value of a event of the player, if it's valid
                    # if not valid it will do nothing but to return False
                    players = player.validate_click(e, current_player, players, settings)
                    current_player = player.get_current_player(players)

        draw_table.draw(pygame, screen, table_sec, settings)
        draw_table.draw_achievement(pygame, screen, players, settings)
        draw_information.draw(pygame, screen, information_sec, current_player, settings)

        pygame.display.flip()

        time.sleep(settings["update_time"])


if __name__ == '__main__':
    if settings["debug"] == True:
        main()
    elif settings["debug"] == False:
        try:
            main()
        except:
            print("Game interrupted.")
