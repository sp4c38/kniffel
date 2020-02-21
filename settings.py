import os

BASE_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "code", "python", "myprograms", "kniffel")

settings = {
    "window_size": (1200, 600),
    "window_resizable": True,
    "bg_color": (0,51,0),
    "window_name": "Kniffel",

    "table_size": 0.70, # The size from the table of the total width in decimal percent
    "table_color": (255,255,0),
    "table_text_color":(255,0,0),
    "table_line_thickness": 3,
    "section_line_thickness": 5,

    "information_size": 0.30, # The size of the information section of the total width in decimal percent

    # The portions in percent as decimal of the width of certain sections of the width from the table
    "detail_colum": 0.30, # in percents <- as decimal,
    "all_players_colum": 0.70,

    # Maximal players allowed / 1 isn't included
    "max_players": 7,

    # Kniffel data
    # "kniffel_names": [[["1er", "Alle Einsen"], ["2er", "Alle Zweien"], ["3er", "Alle Dreien"], \
    #                    ["4er", "Alle Vieren"], ["5er", "Alle Fünfen"], ["6er","Alle Sechsen"]], \
    #                   [["Dreierpasch","Drei gleiche Augenzahlen"], ["Viererpasch", "Vie gleiche Augenzahlen"], ["Full House", "25 Punkte"], \
    #                    ["Small Street", "30 Punkte"], ["Big Street", "40 Punkte"], ["Kniffel", "50 Punkte"], ["Chance", "Alle Augenzahlen"]]],
    "kniffel_names": [[["1er"], ["2er"], ["3er"], \
                       ["4er"], ["5er"], ["6er"]], \
                      [["Dreierpasch"], ["Viererpasch"], ["Full House"], \
                       ["Small Street"], ["Big Street"], ["Kniffel"], ["Chance"]]],
    

    # ! All characters should have the same height in the font
    "font": os.path.join(BASE_DIR, "fonts", "cascadia.ttf"),
    # To make everything fit nicely, a space to the top and bottom is needed / in decimal percent
    "space_top_bottom": 0.1, # Space to top and bottom (together)
    "space_left_right": 0.1, # Space to left and right (together)

    # The text as array -> first value is the text and the second the color of the texts
    "welcome_text": [["Welcome, {}", (255,255,255)], ["Let's play Kniffel!", (255,255,255)]],
    "player_number_text": [["How many players want to play?", (255,255,255)], \
                           ["Please press the number on the keyboard. (max. 7)", (255,255,255)], \
                          ],

    "player_number_successful": [["Super,", (255,255,255)], ["es spielen {} Spieler mit.", (255,255,255)]],
    "player_number_unsuccessful": [["Das geht leider nicht. Probiere es nochmal.", (255,255,255)],
                                   ["Maximal 7 Spieler können mitspielen!", (255,255,255)]
                                  ],
}