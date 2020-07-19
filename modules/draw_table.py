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
    pygame.draw.line(screen, table.color, (table.detail_column_size[0]-table.thicknesshalf, 0),
                    (table.detail_column_size[0]-table.thicknesshalf, table.detail_column_size[1]), table.thickness)

    detail_column_cell_size = (table.detail_column_size[0], table.height_divided_parts)
    spaced_size = (detail_column_cell_size[0]*(1-settings["space_left_right"]), detail_column_cell_size[1]*(1-settings["space_top_bottom"])) # The size of the window reduced to make the text look good

    height_pointer = 0 # The height_pointer indicates the current state where the program is with drawing / needed because we want text in each cell
    for section in settings["kniffel_names"]:

        font_size = min([utils.get_font_by_size(pygame, spaced_size, name[0], 1, settings) for name in section])
        font = pygame.font.Font(settings["font"], font_size)

        for name in section:
            start_point, summand = utils.center_obj_height(pygame, font.get_height(), 1, detail_column_cell_size[1])

            text = font.render(name[0], True, name[1])
            textpos = (utils.center_obj_width(pygame, text.get_width(), 1, detail_column_cell_size[0])[0], height_pointer+start_point)
            screen.blit(text, textpos)
            start_point += summand

            height_pointer += table.height_divided_parts
            pygame.draw.line(screen, table.color, (0, height_pointer-table.thicknesshalf), (table.width, height_pointer-table.thicknesshalf), table.thickness)

    return

def draw_player_columns(pygame, screen, table, settings):
    # Draw the player columns
    width_pointer = table.detail_column_size[0] # Start after detail column

    player_indent = 0

    player_cell_size = (table.player_column_size[0], table.height_divided_parts)
    spaced_size = (table.player_column_size[0]*(1-settings["space_left_right"]), table.height_divided_parts*(1-settings["space_top_bottom"]))

    for p in range(table.player_amount):
        player_indent += 1
        player_text = settings["player_text"]

        font_size = utils.get_font_by_size(pygame, spaced_size, player_text[0].format(player_indent), 1, settings) # Get font size which fits for the height and width

        font = pygame.font.Font(settings["font"], font_size)

        start_point, summand = utils.center_obj_height(pygame, font.get_height(), 1, table.height_divided_parts)

        text = font.render(player_text[0].format(player_indent), True, player_text[1])
        textpos = (utils.center_obj_width(pygame, text.get_width(), 1, table.player_column_size[0])[0]+width_pointer, start_point)
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

def get_table(window, player_amount, settings):
    # Calculate and draw the table
    class Table:
        def __init__(self):
            self.player_amount = player_amount
            self.color = settings["table_color"]
            self.thickness = settings["table_line_thickness"]
            self.thicknesshalf = self.thickness/2
            self.sectionthickness = settings["section_line_thickness"] # The thickness of the section line which divides sections
            self.width = window.table_width - self.thickness
            self.height = window.table_height
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
            self.height_divided_parts = self.height / x # The size of one part in which the height is divided (each line)


    table = Table()
    table.add_column_sizes()

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
    