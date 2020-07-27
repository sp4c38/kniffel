import sys

from kniffel.lib import utils

def draw_outline(pygame, screen, table):
    # Draws the outline of the table

    pygame.draw.line(screen, table.color, (0, 0+table.thicknesshalf), (table.width, 0+table.thicknesshalf), table.thickness)
    pygame.draw.line(screen, table.color, (0+table.thicknesshalf, 0), (0+table.thicknesshalf, table.height - table.thicknesshalf), table.thickness)
    pygame.draw.line(screen, table.color, (0, table.height - table.thicknesshalf), (table.width, table.height - table.thicknesshalf), table.thickness)
    pygame.draw.line(screen, table.color, (table.width,table.height), (table.width,0), table.thickness)

    return

def draw_detail_column(pygame, screen, settings, table):
    # Draw the achievement names in the detail column and
    # draw the line on the right side of the detail column / seperating detail column from player_column
    pygame.draw.line(screen, table.color, (table.detail_column_size[0]-table.thicknesshalf, 0),
                    (table.detail_column_size[0]-table.thicknesshalf, table.detail_column_size[1]), table.thickness)

    # Draw the text in the columns of the detail section and the horizontal lines of the tabel
    detail_column_cell_size = (table.detail_column_size[0], table.one_line_height)
    spaced_size = (table.detail_column_size[0] * (1-settings["space_left_right"]), detail_column_cell_size[1]*(1-settings["space_top_bottom"]))

    start_height = 0 # The height to start writing the horizontal lines and columns
    for section in settings["table_names"]:

        font_size = min([utils.get_font_by_size(pygame, spaced_size, name[0], 1, settings) for name in section])
        font = pygame.font.Font(settings["font"], font_size)

        for name in section:
            start_point = utils.center_obj_height(font.get_height(), 1, detail_column_cell_size[1])[0]

            text = font.render(name[0], True, name[1])
            textpos = (utils.center_obj_width(text.get_width(), 1, detail_column_cell_size[0])[0], start_height+start_point)

            screen.blit(text, textpos)

            start_height += table.one_line_height

            pygame.draw.line(screen, table.color, (0, start_height-table.thicknesshalf), (table.width, start_height-table.thicknesshalf), table.thickness)

    return

def draw_player_columns(pygame, screen, players, table, settings):
    # Draw the player columns

    start_width = table.detail_column_size[0] # Start with first player column after the detail column

    player_cell_size = (table.player_column_size[0], table.one_line_height)
    spaced_size = (table.player_column_size[0]*(1-settings["space_left_right"]), table.one_line_height*(1-settings["space_top_bottom"]))

    for plyr in players:
        player_text = settings["player_text"]

        font_size = min([utils.get_font_by_size(pygame, spaced_size, line[0], len(player_text), settings) for line in player_text])
        font = pygame.font.Font(settings["font"], font_size)

        start_height, spacing = utils.center_obj_height(font.size(player_text[0][0])[1], len(player_text), table.one_line_height)

        for line in player_text:
            text = font.render(line[0].format(plyr.name), True, line[1])
            textpos = (utils.center_obj_width(font.size(line[0])[0], 1, table.player_column_size[0])[0] + start_width, start_height)
            screen.blit(text, textpos)

            start_height += spacing

        pygame.draw.line(screen, table.color, (start_width + player_cell_size[0], 0), (start_width + player_cell_size[0], table.player_column_size[1]), table.thickness)

        start_width = start_width + table.player_column_size[0]

    return

def draw_achievement(pygame, screen, players, settings):
    # Draws all reached achievements from all players in the cells of the columns of the players

    for plyr in players:
        for achieve in plyr.progress: # Go through each achievement and check if it has a value to add it to the table
            achievement = plyr.progress[achieve]

            if achievement.value != None: # Only draw if the achievement has a value

                cell_size = (achievement.position.width, achievement.position.height)
                spaced_size = (cell_size[0] * (1-settings["space_left_right"]), cell_size[1] * (1-settings["space_top_bottom"]))

                font_size = utils.get_font_by_size(pygame, spaced_size, str(achievement.value), 1, settings)
                font = pygame.font.Font(settings["font"], font_size)

                start_height, spacing = utils.center_obj_height(font.size(str(achievement.value))[1], 1, cell_size[1])

                text = font.render(str(achievement.value), True, settings["table_value_color"])
                textpos = (utils.center_obj_width(font.size(str(achievement.value))[0], 1, cell_size[0])[0] + achievement.position.left, start_height + achievement.position.top)
                screen.blit(text, textpos)

    return


def draw(pygame, screen, players, table, settings):
    draw_outline(pygame, screen, table)
    draw_detail_column(pygame, screen, settings, table)
    draw_player_columns(pygame, screen, players, table, settings)
    draw_achievement(pygame, screen, players, settings)

    return

class Table:
    def __init__(self, window, player_number, settings):
        self.player_number = player_number
        self.color = settings["table_line_color"]
        self.thickness = settings["table_line_thickness"]
        self.thicknesshalf = self.thickness/2
        self.width = window.table_width - self.thickness
        self.height = window.height

    def add_column_sizes(self, settings):
        if settings["table_name_section"] + settings["table_all_player_section"] != 1:
            print(f"\033[{settings['error_color']}mERROR:")
            print(f"The column in the table with the names of the goals takes {settings['table_name_section']*100}% and the"
                  f"all columns which show how many points single players accomplished take {settings['table_all_player_section']*100}%.\n"
                  f"The maximal width allowed for the table is 100%, but it's {settings['table_name_section']*100 + settings['table_all_player_section']*100}%.\033[0m")
            sys.exit(1)

        self.detail_column_size = (self.width * settings["table_name_section"], self.height) # The size of the column with names (e.g. Aces, Twos)
        self.player_column_size = ((self.width * settings["table_all_player_section"]) / self.player_number, self.height) # The size of a column for one single player

        # Check if there is the correct amount of names for the achievements
        counter = 0

        for section in settings["table_names"]:
            for achievement in section:
                counter += 1
        if counter < 15 or counter > 15:
            print(f"\033[{settings['error_color']}mERROR:")
            print(f"There are too many or too less names for the achievements. There are {counter}.")
            sys.exit(1)
        self.one_line_height = self.height / counter # The height of one single line in the table

def create(window, player_number, settings):
    # Init the Table class with important attributes for drawing the table later

    table = Table(window, player_number, settings)
    table.add_column_sizes(settings)

    return table
