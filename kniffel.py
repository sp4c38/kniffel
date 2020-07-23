#!/usr/bin/python

import sys

if not int(str(sys.version_info[0]) + str(sys.version_info[1]) + str(sys.version_info[2])) < 380:
    print("Sorry! Pygame only supports python versions under 3.8. Please consider using python 3.7 to play the game.")
    sys.exit(1)

import getpass
import pygame
import random
import time

from lib import window_code, utils, tablesec, informationsec, player

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

    if verbose: print(f"{player_number} players are going to play Kniffel!")

    table_sec = tablesec.create(window, player_number, settings) # Get table class (with table attributes)
    information_sec = informationsec.create(pygame, window, settings)
    if verbose: print("Calculated table and information section sizes.")

    players = player.init_players(pygame, player_number, table_sec, information_sec, window)

    if settings["play_music"]:
        # Play nice background music if activated
        window_code.play_music(pygame, settings)

    current_player = player.get_current(player.switch_turn(players, None))

    while True:
        # The following must be run in a while-loop because
        # these steps could be influenced by the user (e.g. input/output)

        window_code.clear_window(pygame, screen, settings)

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                # Quit the game
                print("Game closed. Until next time!")
                sys.exit(0)

            if settings["window_resizable"]:
                if e.type == pygame.VIDEORESIZE:
                    # Recalculate all sizes for the elements when the window is resized
                    if verbose: print("Window resized. Resizing elements.")
                    screen, window, table_sec, information_sec = window_code.resize_window(pygame, player_number, e, settings)
                    players = player.recalculate_positions(pygame, players, table_sec, information_sec)

            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1: # A left-click on the mouse

                    updated_achievement, updated_dices, players = player.validate_click(e, current_player, players, information_sec, settings)
                    if updated_achievement:
                        current_player = player.get_current(players)
                        if verbose: print("Switched the current player.")
                    if verbose and updated_dices: print("Rolled the dices.")
                    if verbose: print("Validated mousebutton-down click.")

        tablesec.draw(pygame, screen, table_sec, settings)
        tablesec.draw_achievement(pygame, screen, players, settings)
        informationsec.draw(pygame, screen, information_sec, current_player, settings)

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
