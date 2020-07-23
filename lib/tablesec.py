import sys

from lib import utils

def draw_table_outline(pygame, screen, table):
    pygame.draw.line(screen, table.color, (0,0+table.thicknesshalf), (table.width, 0+table.thicknesshalf), table.thickness)
    pygame.draw.line(screen, table.color, (0+table.thicknesshalf,0), (0+table.thicknesshalf,table.height), table.thickness)
    pygame.draw.line(screen, table.color, (0,table.height-table.thicknesshalf), (table.width,table.height-table.thicknesshalf), table.thickness)
    pygame.draw.line(screen, table.color, (table.width,table.height), (table.width,0), table.thickness)
    return


def draw_detail_column(pygame, screen, settings, table):
    # Draws the line on the right side of the detail column / seperating detail column from player_column
    pygame.draw.line(screen, table.color, (table.detail_column_size[0]-table.thicknesshalf, 0),
                    (table.detail_column_size[0]-table.thicknesshalf, table.detail_column_size[1]), table.thickness)

    detail_column_cell_size = (table.detail_column_size[0], table.one_line_height)
    spaced_size = (detail_column_cell_size[0]*(1-settings["space_left_right"]), detail_column_cell_size[1]*(1-settings["space_top_bottom"])) # The size of the window reduced to make the text look good

    height_pointer = 0 # The height_pointer indicates the current state where the program is with drawing / needed because we want text in each cell
    for section in settings["table_names"]:

        font_size = min([utils.get_font_by_size(pygame, spaced_size, name[0], 1, settings) for name in section])
        font = pygame.font.Font(settings["font"], font_size)

        for name in section:
            start_point, summand = utils.center_obj_height(font.get_height(), 1, detail_column_cell_size[1])

            text = font.render(name[0], True, name[1])
            textpos = (utils.center_obj_width(text.get_width(), 1, detail_column_cell_size[0])[0], height_pointer+start_point)
            screen.blit(text, textpos)
            start_point += summand

            height_pointer += table.one_line_height
            pygame.draw.line(screen, table.color, (0, height_pointer-table.thicknesshalf), (table.width, height_pointer-table.thicknesshalf), table.thickness)

    return

def draw_player_columns(pygame, screen, table, settings):
    # Draw the player columns
    width_pointer = table.detail_column_size[0] # Start after detail column

    player_indent = 0

    player_cell_size = (table.one_player_column[0], table.one_line_height)
    spaced_size = (table.one_player_column[0]*(1-settings["space_left_right"]), table.one_line_height*(1-settings["space_top_bottom"]))

    for p in range(table.player_number):
        player_indent += 1
        player_text = settings["player_text"]

        font_size = utils.get_font_by_size(pygame, spaced_size, player_text[0].format(player_indent), 1, settings) # Get font size which fits for the height and width

        font = pygame.font.Font(settings["font"], font_size)

        start_point, summand = utils.center_obj_height(font.get_height(), 1, table.one_line_height)

        text = font.render(player_text[0].format(player_indent), True, player_text[1])
        textpos = (utils.center_obj_width(text.get_width(), 1, table.one_player_column[0])[0]+width_pointer, start_point)
        screen.blit(text, textpos)
        start_point += summand

        column_end = width_pointer + player_cell_size[0]
        pygame.draw.line(screen, table.color, (column_end, 0), (column_end, table.height), table.thickness)


        width_pointer = column_end

    return

def draw(pygame, screen, table, settings):
    draw_table_outline(pygame, screen, table)
    draw_detail_column(pygame, screen, settings, table)
    draw_player_columns(pygame, screen, table, settings)

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
        self.one_player_column = ((self.width * settings["table_all_player_section"]) / self.player_number, self.height) # The size of a column for one single player

        # Check if there is the correct amount of names for the achievements
        counter = 0

        for section in settings["table_names"]:
            for achievement in section:
                counter += 1
        if counter < 14 or counter > 14:
            print(f"\033[{settings['error_color']}mERROR:")
            print(f"There are too many or too less names for the achievements. There are {counter}.")
            sys.exit(1)
        self.one_line_height = self.height / counter # The height of one single line in the table

def create(window, player_number, settings):
    # Init the Table class with important attributes for drawing the table later

    table = Table(window, player_number, settings)
    table.add_column_sizes(settings)

    return table

def draw_achievement(pygame, screen, players, settings):
    # This draws ALL achievements from ALL players which were made

    for player in players:
        for a in player.progress:
            achievement = player.progress[a]

            if achievement.value:
                achievementrect = achievement.position # The position of the cell as a rectangle
                widthheightcell = (achievementrect.width, achievementrect.height) # The width and height of the cell
                spaced_size = (widthheightcell[0]*(1-settings["space_left_right"]), widthheightcell[1]*(1-settings["space_top_bottom"]))

                text_value = str(achievement.value)

                font_size = utils.get_font_by_size(pygame, spaced_size, text_value, 1, settings)
                font = pygame.font.Font(settings["font"], font_size)

                start_point, summand = utils.center_obj_height(pygame, font.get_height(), 1, widthheightcell[1])

                text = font.render(text_value, True, settings["table_value_color"])
                textpos = (utils.center_obj_width(pygame, text.get_width(), 1, widthheightcell[0])[0]+achievementrect.left, start_point+achievementrect.top)
                screen.blit(text, textpos)

    return
