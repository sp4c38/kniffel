import os

BASE_DIR = os.path.join(os.path.expanduser("~"), os.getcwd())


settings = {
    "debug": True,
    "update_time": 0.1, # In which interval the window shall update (in seconds) (one update every 0.1 second would be 10 fps)

    "error_color": 91, # The ANSI color code to highlight errors in the program output

    "window_resizable": True, # Activate or deactivate window resizable option
    "window_icon": os.path.join(BASE_DIR, "assets", "window_icon.png"), # The icon of the game
    "window_size": (1400, 800),     # The size of the default window size in (width, height)
    "window_name": "Kniffel Yahtzee", # The name of the window


    "table_ratio": 0.70,            # Ratio of the table section to the total width
                                    # Number in percent, must < 1

    "information_ratio": 0.30,      # Ratio of the information section to the total width
                                    # Number in percent, must < 1

    "welcome_text": [["Welcome {},", (255,255,255)], ["Let's play Kniffel!", (255,255,255)]], # Text for welcome screen

    # A text displayed to ask how many players want to play kniffel
    "player_number_text": [["How many players want to play?", (255,255,255)], \
                           ["Please press the number on the keyboard. (max. {})", (255,255,255)], \
                          ],

    "max_players": 6, # The maximal amount of players allowed to play
    # A message displayed when the player number selection was successful
    "player_number_successful": [["Cool,", (255,255,255)], ["there are {} players.", (255,255,255)]],

    "table_line_color": (255,255,255), # The color of the lines which make up the table
    "table_line_thickness": 5, # The thickness of the lines which make up the table

    # Both must sum up to 1 (100%):
    "table_name_section": 0.30, # The ratio of the total table width for the column with the names of the goals (e.g. Aces, Twos)
    "table_all_player_section": 0.70, # The ratio of the total table width for all columns which contain the reached points of all players

    # The names of the goals to achive by the players
    "table_names": [
                      [["", (255,255,255)], ["Aces", (243,100,255)], ["Twos", (243,100,255)], ["Threes", (243,100,255)], \
                       ["Fours", (243,100,255)], ["Fives", (243,100,255)], ["Sixes", (243,100,255)]], \
                      [["Three Of A Kind", (128,255,9)], ["Four Of A Kind", (128,255,9)], ["Full House", (128,255,9)], \
                       ["Small Straight", (128,255,9)], ["Long Straight", (128,255,9)], ["Kniffel", (17,255,0)], \
                       ["Chance", (0,255,240)]]
                     ],

    "crt_player_section_height": 0.15, # The ratio of the total height for the section which displays which player currently has the turn

    "dice_images": {
        # The images for the different possibilities to throw the dice
        1: os.path.join(BASE_DIR, "assets", "dice_numbers", "one.png"),
        2: os.path.join(BASE_DIR, "assets", "dice_numbers", "two.png"),
        3: os.path.join(BASE_DIR, "assets", "dice_numbers", "three.png"),
        4: os.path.join(BASE_DIR, "assets", "dice_numbers", "four.png"),
        5: os.path.join(BASE_DIR, "assets", "dice_numbers", "five.png"),
        6: os.path.join(BASE_DIR, "assets", "dice_numbers", "six.png"),
    },
    "dice_button_height": 0.1, # The ratio of the total height of the information section assigned for the dice button
    "dice_button_color": (242,255,5), # The background color of the dice button
    "dice_button_text": [["Roll The Dice", (139,69,19)]], # The text for the dice button

    "play_music": False, # Activate or deactivate background music
    "window_music": os.path.join(BASE_DIR, "assets", "music", "background_music.mp3"), # Background music path

    # The points when reaching achievements
    # The names are hard-coded in the game and must not be changed!
    "point_distribution": {
        "aces": None, # None indicates that the point may vary for a certain achievement
        "twos": None,
        "threes": None,
        "fours": None,
        "fives": None,
        "sixes": None,
        "toak": None,
        "foak": None,
        "fh": 25,
        "smstraight": 30,
        "lgstraight": 40,
        "kniffel": 50,
        "chance": None,
    },

    "space_left_right": 0.1, # Margin to the left and right (together) to make text fit more nicely
    "space_top_bottom": 0.1, # Margin to the top and bottom (together) to make text fit more nicely

    "bg_color": (0,0,0),


    "table_value_color": (255,255,255), # The color of entries/values in the table


    # The portions in percent as decimal of the width of certain sections of the width from the table
    # Maximal players allowed / below 0, 0 and 1 aren't included

    # The text which is shown in the most top line for a player
    "player_text": ("Player {}", (255,255,255)), # No multiline allowed
    "crt_player_text": ("It's Player {}'s turn.", (255,255,255)), # The text which shows which player has the turn / No multiline allowed

    # ! All characters should have the same height in the font
    "font": os.path.join(BASE_DIR, "assets", "fonts", "cascadia.ttf"),

    # The text as array -> first value is the text and the second the color of the texts
    "player_number_unsuccessful": [["Sorry, this doesn't work. Please try again", (255,255,255)],
                                   ["A maximum of {} players can play.", (255,255,255)]
                                  ],


    # This is the maximum of the dice size in height from the height in decimal percent
    # No specific specification can made because: width=height - mostly wouldn't fit with width with specification
    "dice_size_maximum": 0.2,

}
