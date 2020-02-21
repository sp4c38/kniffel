import sys

from modules import utils

def draw_table_outline(pygame, screen, table):
    pygame.draw.line(screen, table.color, (0,0+table.thicknesshalf), (table.width, 0+table.thicknesshalf), table.thickness)
    pygame.draw.line(screen, table.color, (0+table.thicknesshalf,0), (0+table.thicknesshalf,table.height), table.thickness)
    pygame.draw.line(screen, table.color, (0,table.height-table.thicknesshalf), (table.width,table.height-table.thicknesshalf), table.thickness)
    pygame.draw.line(screen, table.color, (table.width,table.height), (table.width,0), table.thickness)
    return


def draw_detail_column(pygame, screen, settings, table):
    # Draws the line on the right side of the detail column / seperating detail column from player_column
    pygame.draw.line(screen, table.color, (table.detail_column_size[0], 0), table.detail_column_size, table.thickness)

    detail_column_cell_size = (table.detail_column_size[0], table.hight_divided_parts)
    spaced_size = (detail_column_cell_size[0]*(1-settings["space_left_right"]), detail_column_cell_size[1]*(1-settings["space_top_bottom"])) # The size of the window reduced to make the text look good

    height_pointer = 0 # The height_pointer indicates the current state where the program is with drawing / needed because we want text in each cell
    for section in settings["kniffel_names"]:

        font_size = []
        for cell in section:
            for name in cell:
                font_size.append(utils.get_font_by_size(pygame, spaced_size, name, len(cell), settings)) # Take the font size for the text with the smallest one -> that it looks nice

        font_size = min(font_size)
        font = pygame.font.Font(settings["font"], font_size)

        for cell in section:
            start_point, summand = utils.center_text_height(pygame, font, cell, detail_column_cell_size[1])
            for name in cell:
                text = font.render(name, True, table.text_color)
                textpos = (utils.center_text_width(pygame, font, name, detail_column_cell_size[0]), height_pointer+start_point)
                screen.blit(text, textpos)
                start_point += summand

            height_pointer += table.hight_divided_parts
            pygame.draw.line(screen, table.color, (0, height_pointer), (table.width, height_pointer), table.thickness)

    return

def draw_player_columns(pygame, screen, table):
    # Draw the player columns
    width_pointer = table.detail_column_size[0] # Start after detail column

    for p in range(table.player_amount):
        column_width_start = width_pointer + table.player_column_size[0]
        pygame.draw.line(screen, table.color, (column_width_start, 0), (column_width_start, table.player_column_size[1]), table.thickness)

        width_pointer = column_width_start

    return    

def draw(pygame, screen, table, settings):
    draw_table_outline(pygame, screen, table)
    draw_detail_column(pygame, screen, settings, table)
    draw_player_columns(pygame, screen, table)

    return

def get_table(window, player_amount, settings):
    # Calculate and draw the table
    class Table:
        def __init__(self):
            self.player_amount = player_amount
            self.width = window.table_width
            self.height = window.table_height
            self.color = settings["table_color"]
            self.text_color = settings["table_text_color"]
            self.thickness = settings["table_line_thickness"]
            self.thicknesshalf = self.thickness/2
            self.sectionthickness = settings["section_line_thickness"] # The thickness of the section line which divides sections
        def add_column_sizes(self):
            if settings["detail_colum"] + settings["all_players_colum"] != 1:
                print(f"All columns of the table together to not sum up as 1, but as {settings['detail_colum'] + settings['all_players_colum']}.")
                print("Aborting.")
                sys.exit(1)
            self.detail_column_size = (self.width * settings["detail_colum"], self.height) # The size of the detail column
            self.player_column_size = ((self.width * settings["all_players_colum"]) / self.player_amount, self.height) # The size of one player column
            x = 0
            # Get the number of arrays in array
            for s in settings["kniffel_names"]:
                for e in s:
                    x += 1
            if x == 0:
                print("At least one division in parts is required (in height).")
                sys.exit(1)
            self.hight_divided_parts = self.height / x # The size of one part in which the height is divided (each line)


    table = Table()
    table.add_column_sizes()

    return table