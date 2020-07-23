from lib import rules

import random

class Player:
    def __init__(self, name):
        self.is_current_player = False # Indicates if this player is the one which currently has the turn
        self.current_dices = [] # Stores the dices currently thrown or selected by the player
        self.player_name = name # The name of the player

    class Event:
        # Event holds attributes for one single achievement a player can reach
        # For each player a set of this Event classes is created

        def __init__(self, name, position, achievement_counter):
            self.name = name # Name of achievement
            self.position = position # Position of achievement
            self.value = None # Value of achievement (is set when player reached it)
            self.achievement_counter = achievement_counter # The nth achievement from the top to the bottom
                                                           # Needed to draw the achievements correctly

        def change_value(self, newvalue):
            # Update the value of a achievement (when it was reached)
            self.value = newvalue

    def add_progress(self, pygame, table, width_start):
        self.progress = {
        "aces": self.Event("aces", pygame.Rect(width_start, (1*table.one_line_height), table.player_column_size[0], table.one_line_height), 1), # Aces
        "twos": self.Event("twos", pygame.Rect(width_start, (2*table.one_line_height), table.player_column_size[0], table.one_line_height), 2), # Twos
        "threes": self.Event("threes", pygame.Rect(width_start, (3*table.one_line_height), table.player_column_size[0], table.one_line_height), 3), # Threes
        "fours": self.Event("fours", pygame.Rect(width_start, (4*table.one_line_height), table.player_column_size[0], table.one_line_height), 4), # Fours
        "fives": self.Event("fives", pygame.Rect(width_start, (5*table.one_line_height), table.player_column_size[0], table.one_line_height), 5), # Fives
        "sixes": self.Event("sixes", pygame.Rect(width_start, (6*table.one_line_height), table.player_column_size[0], table.one_line_height), 6), # Sixes
        "toak": self.Event("toak", pygame.Rect(width_start, (7*table.one_line_height), table.player_column_size[0], table.one_line_height), 7), # Three of a kind
        "foak": self.Event("foak", pygame.Rect(width_start, (8*table.one_line_height), table.player_column_size[0], table.one_line_height), 8), # Four of a kind
        "fh": self.Event("fh", pygame.Rect(width_start, (9*table.one_line_height), table.player_column_size[0], table.one_line_height), 9), # Full House
        "smstraight": self.Event("smstraight", pygame.Rect(width_start, (10*table.one_line_height), table.player_column_size[0], table.one_line_height), 10), # Small Straight
        "lgstraight": self.Event("lgstraight", pygame.Rect(width_start, (11*table.one_line_height), table.player_column_size[0], table.one_line_height), 11), # Long Straight
        "kniffel": self.Event("kniffel", pygame.Rect(width_start, (12*table.one_line_height), table.player_column_size[0], table.one_line_height), 12), # Kniffel
        "chance": self.Event("chance", pygame.Rect(width_start, (13*table.one_line_height), table.player_column_size[0], table.one_line_height), 13), # Chance
        }

    def update_achievement(self, name, pygame, table, width_start):
        self.progress[name].position = pygame.Rect(width_start, (self.progress[name].achievement_counter*table.one_line_height), table.cell_size[0], table.one_line_height)

    def remove_stored_dices(self):
        self.current_dices = []

def init_players(pygame, player_amount, table_sec, information_sec, window):
    players = [] # A list which later will hold a Player class for each player

    start_width = table_sec.detail_column_size[0] # The width from which the first player columns starts

    player_name = 1

    for p in range(player_amount):
        player = Player(str(player_name))
        player.add_progress(pygame, table_sec, start_width)
        players.append(player)

        player_name += 1 # Add one each time so that the player name is different for each player
        start_width += table_sec.player_column_size[0] # Add the width of one player column to have the start width
                                                       # of the next player column

    return players

def recalculate_positions(pygame, players, table_sec, information_sec):
    width_pointer = table_sec.detail_column_size[0]

    for plyr in players:
        plyr.add_dice_button(pygame, information_sec)
        for achievement in plyr.progress:
            plyr.update_achievement(achievement, pygame, table_sec, width_pointer)

        width_pointer += table_sec.player_column_size[0]

    return players


def switch_turn(players, current_player):
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

def get_current(players):
    for plyr in players:
        if plyr.is_current_player:
            return plyr

    return None

def roll_dices(player, information_sec, settings):
    # Rolles the dices

    player.remove_stored_dices()

    for x in range(information_sec.dice_number):
        random_number = random.randint(min(settings["dice_images"]), max(settings["dice_images"]))
        player.current_dices.append(random_number)

    return

def make_action(dices, achievement, settings):
    # This checks if the selected achievement to enter the value is valid

    # dices ... the dices the player threw
    # achievement ... the achievement which was selected

    checked = rules.check(dices, settings)

    if checked[achievement.name] != None: # If the achievement is valid to enter
        achievement.change_value(checked[achievement.name])
        return True
    else:
        return False


def validate_click(event, player, all_players, information_sec, settings):
    # event ... mouse click input event
    # player ... current player

    updated_achievement = False
    updated_dices = False

    click_position = event.pos
    point_distribution = settings["point_distribution"]
    player_dices = player.current_dices # The dices of the current player

    for achievement in player.progress:
        achievement = player.progress[achievement]

        if achievement.position.collidepoint(click_position): # Check if the clicked position intervenes with the cell of a achievment
            if player_dices:
                if make_action(player.current_dices, achievement, settings):
                    player.remove_stored_dices()
                    all_players = switch_turn(all_players, player)
                    updated_achievement = True


    if information_sec.dice_button_rect.collidepoint(click_position):
        roll_dices(player, information_sec, settings)
        updated_duces = True

    return updated_achievement, updated_dices, all_players
