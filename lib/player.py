from lib import check_rules

import random

def recalculate_positions(pygame, players, table, infopg):
    width_pointer = table.detail_column_size[0]

    for p in players:
        p.calc_dice_button(pygame, infopg)
        for a in p.progress:
            p.update_progress(a, pygame, table, width_pointer)

        width_pointer += table.one_player_column[0]

    return players


class Player:
    def __init__(self, name):
        self.is_current_player = False # Indicates if this player is the one which currently has the turn
        self.current_dices = [] # Stores the dices currently thrown or selected by the player
        self.player_name = name # The name of the player

    class Event:
        # Event holds attributes for one single achievement a player can reach
        # For each player a set of this Event classes is created

        def __init__(self, name, position, height_multiplicator):
            self.name = name # Name of achievement
            self.position = position # Position of achievement
            self.value = None # Value of achievement (is set when player reached it)
            #self.height_multiplicator = height_multiplicator # This is

        def change_value(self, newvalue):
            # Update/Change a value
            self.value = newvalue

    def add_progress(self, pygame, table, width_start):
        self.progress = {
        "aces": self.Event("aces", pygame.Rect(width_start, (1*table.one_line_height), table.one_player_column[0], table.one_line_height), 1), # Aces
        "twos": self.Event("twos", pygame.Rect(width_start, (2*table.one_line_height), table.one_player_column[0], table.one_line_height), 2), # Twos
        "threes": self.Event("threes", pygame.Rect(width_start, (3*table.one_line_height), table.one_player_column[0], table.one_line_height), 3), # Threes
        "fours": self.Event("fours", pygame.Rect(width_start, (4*table.one_line_height), table.one_player_column[0], table.one_line_height), 4), # Fours
        "fives": self.Event("fives", pygame.Rect(width_start, (5*table.one_line_height), table.one_player_column[0], table.one_line_height), 5), # Fives
        "sixes": self.Event("sixes", pygame.Rect(width_start, (6*table.one_line_height), table.one_player_column[0], table.one_line_height), 6), # Sixes
        "toak": self.Event("toak", pygame.Rect(width_start, (7*table.one_line_height), table.one_player_column[0], table.one_line_height), 7), # Three of a kind
        "foak": self.Event("foak", pygame.Rect(width_start, (8*table.one_line_height), table.one_player_column[0], table.one_line_height), 8), # Four of a kind
        "fh": self.Event("fh", pygame.Rect(width_start, (9*table.one_line_height), table.one_player_column[0], table.one_line_height), 9), # Full House
        "smstraight": self.Event("smstraight", pygame.Rect(width_start, (10*table.one_line_height), table.one_player_column[0], table.one_line_height), 10), # Small Straight
        "lgstraight": self.Event("lgstraight", pygame.Rect(width_start, (11*table.one_line_height), table.one_player_column[0], table.one_line_height), 11), # Long Straight
        "kniffel": self.Event("kniffel", pygame.Rect(width_start, (12*table.one_line_height), table.one_player_column[0], table.one_line_height), 12), # Kniffel
        "chance": self.Event("chance", pygame.Rect(width_start, (13*table.one_line_height), table.one_player_column[0], table.one_line_height), 13), # Chance
        }

    def add_dice_button(self, pygame, information_sec):
        # Adds attributes for the dice button
        dice_button_size = (information_sec.width, information_sec.dice_button_height)
        self.dice_button_rect = pygame.Rect(information_sec.start_width, information_sec.height - dice_button_size[1], dice_button_size[0], dice_button_size[1]) # left, top, width, height

    def update_progress(self, name, pygame, table, width_start):
        self.progress[name].position = pygame.Rect(width_start, (self.progress[name].height_multiplicator*table.one_line_height), table.one_player_column[0], table.one_line_height)

    def remove_stored_dices(self):
        self.current_dices = []

def init_players(pygame, player_amount, table_sec, information_sec, window):
    players = [] # A list which later will hold a Player class for each player

    start_width = table_sec.detail_column_size[0] # The width from which the first player columns starts

    player_name = 1

    for p in range(player_amount):
        player = Player(str(player_name))
        player.add_progress(pygame, table_sec, start_width)
        player.add_dice_button(pygame, information_sec)
        players.append(player)

        player_name += 1 # Add one each time so that the player name is different for each player
        start_width += table_sec.one_player_column[0] # Add the width of one player column to have the start width
                                                      # of the next player column

    return players

def switch_player_turn(players, current_player):
    # Switches the turn from the current player to the next player
    # If current_player is None than the first player in the list is assigned the current turn

    if not current_player:
        # Returns the first value (first player) of the list, if no player is the current already
        players[0].is_current_player = True
        return players

    player_pointer = players.index(current_player)

    try:
        players[player_pointer+1].is_current_player = True
        players[player_pointer].is_current_player = False
    except:
        players[0].is_current_player = True
        players[player_pointer].is_current_player = False

    return players

def get_current_player(players):
    for plyr in players:
        if plyr.is_current_player:
            return plyr

    return None

def update_player_dice(player, settings):
    # This updates the dices which are assigned to a player IF there not already are any
    player.current_dices = []
    # if not player.current_dices:
    for x in range(5):
        random_number = random.randint(min(settings["dice_images"]), max(settings["dice_images"]))
        player.current_dices.append(random_number) # The number is later replaced by the image (i.e.: Dice image for 1, ...)
    print("Updated dices.")
    return

def make_action(dices, want_to_do, settings):
    # Validates and than makes the action for a click in a box (e.g. in aces)

    # dices ... the dices as list
    # want_to_do ... the box which was selected to fill
    print("Checking selection...")
    rules = check_rules.check(dices, settings)
    if rules[want_to_do.name]:
        want_to_do.change_value(rules[want_to_do.name])
        return True
    else:
        return False


def validate_click(event, player, all_players, settings):
    # event is the mouse click event
    # player is the current player
    # Validate the click

    click_position = event.pos
    point_distribution = settings["point_distribution"]
    players_dices = player.current_dices

    for p in player.progress:
        prgrs = player.progress[p]
        if prgrs.position.collidepoint(click_position):
            if players_dices:
                if point_distribution[prgrs.name]:
                    if make_action(player.current_dices, prgrs, settings):
                        player.remove_stored_dices()
                        all_players = next_player(all_players, player)

                        print("Switched user.")
                        return all_players
                else:
                    if make_action(player.current_dices, prgrs, settings):
                        player.remove_stored_dices()
                        all_players = next_player(all_players, player)

                        print("Switched user.")
                        return all_players


    if player.dice_button_rect.collidepoint(click_position):
        update_player_dice(player, settings)

    return all_players # Only return False if no collidepoints were found in the for-loop
