from kniffel.lib import rules, utils

import random

class Player:
    def __init__(self, name, settings):
        self.is_current_player = False # Indicates if this player is the one which currently has the turn
        self.dices = [] # Stores the dices currently thrown or selected by the player
        self.name = name # The name of the player
        self.throws = settings["dice_throws"] # Number of throws a player has in a single round

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
        "total": self.Event("total", pygame.Rect(width_start, (14*table.one_line_height), table.player_column_size[0], table.one_line_height), 14), # The total of all achievements
        }

        self.progress["total"].change_value(0) # At beginning of game the total is 0

    def update_achievement(self, name, pygame, table, width_start):
        self.progress[name].position = pygame.Rect(width_start, (self.progress[name].achievement_counter*table.one_line_height), table.detail_column_size[0], table.one_line_height)

    class DiceField:
        # This class is created and stored for each single dice to control there level, image and position
        def __init__(self):
            # In Kniffel you can roll the dice and than put aside some of the rolled dices
            # When dices are put aside they must be drawn in an extra row
            # To indicate in which row the dice currently is level is used.
            # 0 means that it can be rolled again and 1 means that it was put aside
            self.level = 0
            self.image = None
            self.position = None
            self.value = None

        def set_value(self, new_value):
            self.value = new_value

        def set_image(self, dice_image):
            self.image = dice_image

        def set_rect(self, rect):
            self.position = rect

        def change_level(self):
            if self.level == 0:
                self.level = 1
            elif self.level == 1:
                self.level = 0

    def add_dices(self, information_sec):
        # Adds the correct number of dices as DiceField objects in the dices list

        for num in range(information_sec.dice_number):
            dice = self.DiceField()
            self.dices.append(dice)

    def update_dices(self, pygame, information_sec):
        # Calculates the rectangle position for the dices
        # Can be run the first time and when window resized
        level_distri = {0: 0, 1: 0}
        for dice in self.dices:
            if dice.level == 0:
                level_distri[0] += 1
            elif dice.level == 1:
                level_distri[1] += 1

        start_width1, dice_spacing = utils.center_obj_width(information_sec.dice_size[0], level_distri[0], information_sec.width)
        if level_distri[1] == 0:
            start_height1, line_spacing = utils.center_obj_height(information_sec.dice_size[1], 1, information_sec.dice_section_height)
        else:
            start_height1, line_spacing = utils.center_obj_height(information_sec.dice_size[1], 2, information_sec.dice_section_height)
        start_width1 += information_sec.start_width
        start_height1 += information_sec.crt_player_height

        start_width2, dice_spacing = utils.center_obj_width(information_sec.dice_size[0], level_distri[1], information_sec.width)
        start_width2 += information_sec.start_width
        start_height2 = start_height1 + line_spacing

        for dice in self.dices:
            if dice.level == 0:
                dice_rect = pygame.Rect(start_width1, start_height1, information_sec.dice_size[0], information_sec.dice_size[1])
                dice.set_rect(dice_rect)
                start_width1 += dice_spacing
            elif dice.level == 1:
                dice_rect = pygame.Rect(start_width2, start_height2, information_sec.dice_size[0], information_sec.dice_size[1])
                dice.set_rect(dice_rect)
                start_width2 += dice_spacing

            if dice.value:
                dice.set_image(information_sec.dice_images[dice.value])

    def roll_dices(self, pygame, information_sec, settings):
        for dice in self.dices:
            if dice.level == 0:
                random_number = random.randint(min(information_sec.dice_images), max(information_sec.dice_images))
                dice.set_value(random_number)

        self.throws -= 1

        self.update_dices(pygame, information_sec)

    def remove_stored_dices(self):
        # Remove the dices from the previouse round of a player
        for dice in self.dices:
            dice.value = None
            dice.image = None
            dice.level = 0 # Put all dices back in the first level

def init_players(pygame, player_amount, table_sec, information_sec, settings):
    players = [] # A list which later will hold a Player class for each player

    start_width = table_sec.detail_column_size[0] # The width from which the first player columns starts

    player_name = 1

    for p in range(player_amount):
        player = Player(str(player_name), settings)
        player.add_progress(pygame, table_sec, start_width)
        player.add_dices(information_sec)
        players.append(player)

        player_name += 1 # Add one each time so that the player name is different for each player
        start_width += table_sec.player_column_size[0] # Add the width of one player column to have the start width
                                                       # of the next player column

    return players

def recalculate_positions(pygame, players, table_sec, information_sec):
    width_pointer = table_sec.detail_column_size[0]

    for plyr in players:
        plyr.update_dices(pygame, information_sec)

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

def make_action(dices, achievement, total, settings):
    # This checks if the selected achievement to enter the value is valid

    # dices ... the dices the player threw
    # achievement ... the achievement which was selected

    checked = rules.check(dices, settings)

    if checked[achievement.name] != None: # If the achievement is valid to enter
        achievement.change_value(checked[achievement.name])
        total.change_value(total.value + checked[achievement.name])
        return True
    else:
        return False


def validate_click(pygame, event, player, all_players, information_sec, settings):
    # event ... mouse click input event
    # player ... current player

    updated = False
    updated_achievement = False

    click_position = event.pos
    point_distribution = settings["point_distribution"]

    for achievement in player.progress:
        achievement = player.progress[achievement]

        if achievement.position.collidepoint(click_position): # Check if the clicked position intervenes with the cell of a achievment
            if player.dices[0].value: # Check if the first item has any value
                                      # Because if first item has no value all other also have no value
                if not achievement.name in ["total"]: # List includes all achievements which shall be ignored if clicked
                    if make_action(player.dices, achievement, player.progress["total"], settings):
                        player.remove_stored_dices()
                        player.throws = settings["dice_throws"] # Revert the throws for the player back to 3
                                                                # that he can throw the dice again 3 times the next turn
                        all_players = switch_turn(all_players, player)
                        updated = True
                        updated_achievement = True

    if player.dices[0].value != None: # If first item has a value all others also have
        # If any dice is clicked the level is changed (dice put aside) and the dice positions
        # are updated

        for dice in player.dices:
            if dice.position.collidepoint(click_position):
                dice.change_level()

                updated = True

        player.update_dices(pygame, information_sec)

    if information_sec.dice_button_rect.collidepoint(click_position):
        if player.throws == 0: # If the player has taken up all his throws
                               # the dices can't be rolled anymore
            pass
        else:
            player.roll_dices(pygame, information_sec, settings)
            updated = True

    return updated, updated_achievement, all_players
