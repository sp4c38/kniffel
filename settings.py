import os

BASE_DIR = os.path.join(os.path.expanduser("~"), os.getcwd())


settings = {

    "window_size": (1200, 600),
    "window_resizable": True,
    "bg_color": (0,0,0),
    "window_name": "Kniffel",
    "play_music": False,

    "music": os.path.join(BASE_DIR, "assets", "music", "background_music.mp3"),

    "table_size": 0.70, # The size from the table of the total width in decimal percent
    "table_color": (255,255,255),
    "table_line_thickness": 3,
    "section_line_thickness": 5,
    "table_value_color": (255,255,255), # The color of entries/values in the table

    "information_size": 0.30, # The size of the information section of the total width in decimal percent

    # The portions in percent as decimal of the width of certain sections of the width from the table
    "detail_colum": 0.30, # in percents <- as decimal,
    "all_players_colum": 0.70,

    "screen_favicon": os.path.join(BASE_DIR, "assets", "window_icon.jpeg"),
    # Maximal players allowed / below 0, 0 and 1 aren't included
    "max_players": 7,

    "kniffel_names": [[["", (255,255,255)], ["Aces", (243,100,255)], ["Twos", (243,100,255)], ["Threes", (243,100,255)], \
                       ["Fours", (243,100,255)], ["Fives", (243,100,255)], ["Sixes", (243,100,255)]], \
                      [["Three Of A Kind", (128,255,9)], ["Four Of A Kind", (128,255,9)], ["Full House", (128,255,9)], \
                       ["Small Straight", (128,255,9)], ["Long Straight", (128,255,9)], ["Kniffel", (17,255,0)], \
                       ["Chance", (0,255,240)]]
                     ],

    # The text which is shown in the most top line for a player
    "player_text": ("Player {}", (255,255,255)), # No multiline allowed
    "crt_player_text": ("It's Player {}'s turn.", (255,255,255)), # The text which shows which player has the turn / No multiline allowed

    # ! All characters should have the same height in the font
    "font": os.path.join(BASE_DIR, "assets", "fonts", "cascadia.ttf"),
    # To make everything fit nicely, a space to the top and bottom is needed / in decimal percent
    "space_top_bottom": 0.1, # Space to top and bottom (together)
    "space_left_right": 0.1, # Space to left and right (together)

    # The text as array -> first value is the text and the second the color of the texts
    "welcome_text": [["Welcome {},", (255,255,255)], ["Let's play Kniffel!", (255,255,255)]],
    "player_number_text": [["How many players want to play?", (255,255,255)], \
                           ["Please press the number on the keyboard. (max. {})", (255,255,255)], \
                          ],

    "player_number_successful": [["Great,", (255,255,255)], ["there are {} players.", (255,255,255)]],
    "player_number_unsuccessful": [["Sorry, this doesn't work. Please try again", (255,255,255)],
                                   ["A maximum of {} players can play.", (255,255,255)]
                                  ],

    # The keys shouldn't be changed
    "point_distribution": {
        "aces": None, # None indicates that the point may be different
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

    "dice": {
        # Representation of the different dice numbers as images
        1: os.path.join(BASE_DIR, "assets", "dice_numbers", "one.png"),
        2: os.path.join(BASE_DIR, "assets", "dice_numbers", "two.png"),
        3: os.path.join(BASE_DIR, "assets", "dice_numbers", "three.png"),
        4: os.path.join(BASE_DIR, "assets", "dice_numbers", "four.png"),
        5: os.path.join(BASE_DIR, "assets", "dice_numbers", "five.png"),
        6: os.path.join(BASE_DIR, "assets", "dice_numbers", "six.png"),
    },

    # This is the maximum of the dice size in height from the height in decimal percent
    # No specific specification can made because: width=height - mostly wouldn't fit with width with specification
    "dice_size_maximum": 0.2,

    "crt_player_height": 0.15, # The height from all the height for the current player text section in decimal percent

    "dice_button_height": 0.1, # The size for the dice button of the height in decimal percent
    "dice_button_color": (242,255,5),
    "dice_button_text": [["Draw The Dice", (139,69,19)]],

}
