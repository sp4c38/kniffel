#!/usr/bin/python

import getpass
import pygame
import random
import sys
import time

from modules import window_code, draw_table, utils, player, information

from settings import settings

def main():
    pygame.init()
    user = getpass.getuser()

    # ! screen: the pygame window class / window: a own class which keeps general mesurments
    window_code.set_window_icon(pygame, settings)
    screen, window = window_code.create_window(pygame, settings)
    # window_code.welcome_text(pygame, screen, window, user, settings) # Display a welcome text

    # player_number = window_code.ask_player_number(pygame, screen, window, settings) # How many players are there?
    player_number = 2

    table = draw_table.get_table(window, player_number, settings) # Get table information
    information_page = information.get_information_page(pygame, window, settings)

    players = player.init_players(pygame, player_number, information_page, table, window) # A list which stores player progress information
    
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
                print("Quitting program.")
                sys.exit(0)
            if settings["window_resizable"]:
                if e.type == pygame.VIDEORESIZE:
                    print("Resizing window.")
                    screen, window, table, information_page = window_code.update_window(pygame, player_number, e, settings)
                    players = player.recalculate_positions(pygame, players, table, information_page)
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1: # A left-click on the mouse
                    # This changes the value of a event of the player, if it's valid
                    # if not valid it will do nothing but to return False
                    players = player.validate_click(e, current_player, players, settings)
                    current_player = player.get_current_player(players)

        draw_table.draw(pygame, screen, table, settings)
        draw_table.draw_achievement(pygame, screen, players, settings)
        information.draw(pygame, screen, information_page, current_player, settings)

        pygame.display.flip()

        time.sleep(1)

if __name__ == '__main__':
    main()
