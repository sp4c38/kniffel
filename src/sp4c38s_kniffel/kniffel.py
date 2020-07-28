#!/usr/bin/env python3

import sys
import getpass
import os
import pygame
import random
import time

from sp4c38s_kniffel.lib import window_code, utils, tablesec, informationsec, player
from sp4c38s_kniffel.etc import settings as set

if "-v" in sys.argv:
    # When verbose output is enabled extra information about the game running is outputed
    verbose = True
else:
    verbose = False

def main():
    resources_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    settings = set.main(resources_path)

    verbose = False

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

    players = player.init_players(pygame, player_number, table_sec, information_sec, settings)

    if settings["play_music"]:
        # Play nice background music if activated
        window_code.play_music(pygame, settings)

    current_player = player.get_current(player.switch_turn(players, None))

    first_run = True

    while True:
        # The following must be run in a while-loop because
        # these steps could be influenced by the user (e.g. input/output)

        window_updated = False

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
                    screen, window, table_sec, information_sec = window_code.resize_window(pygame, players, e, settings)
                    players = player.recalculate_positions(pygame, players, table_sec, information_sec)
                    window_updated = True

            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1: # A left-click on the mouse
                    if verbose: print("Recoginzed left mousbutton-down click.")
                    updated, updated_achievement, players = player.validate_click(pygame, e, current_player, players, information_sec, settings)

                    if updated:
                        window_updated = True

                    if updated_achievement:
                        current_player = player.get_current(players)
                        if verbose: print("Switched the current player.")

        if first_run or window_updated:
            tablesec.draw(pygame, screen, players, table_sec, settings)
            informationsec.draw(pygame, screen, information_sec, current_player, settings)

            pygame.display.flip()

        first_run = False

        time.sleep(settings["update_time"])


if __name__ == '__main__':
    if verbose:
        main()
    elif not verbose:
        try:
            main()
        except:
            print("The game exited.")
