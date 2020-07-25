import sys

def get_font_by_size(pygame, box_size, text, list_length, settings):
    # This finds the font size which is needed to make a text fit into a specific width and height / returns font_size

    # box_size are the width and the height of the window section the text shall fit in (as tuple)
    # list_length is the length of the list which is needed for making the text also fit in height

    font_size_found = False
    font_size = 1
    previouse_font_size = font_size

    while not font_size_found:
        # Iterate until a font size was found that fits into the box size

        font = pygame.font.Font(settings["font"], font_size) # init the font
        size = font.size(text)
        text_size = (size[0], font.get_height()*list_length)

        if text_size[0] <= box_size[0] and text_size[1] <= box_size[1]:
            previouse_font_size = font_size
        elif not text_size[0] <= box_size[0] or not text_size[1] <= box_size[1] and previouse_font_size:
            font_size_found = True
        else:
            print(f"\033[{settings['error_color']}mERROR:")
            print(f"No font size could be found which fits the box_size.\033[0m\n")

            sys.exit(1)

        font_size += 1

    return previouse_font_size

def center_obj_width(obj_width, list_length, box_width):
    # Finds the position on the x axis to center some object
    # This works for a single object in a line or for multiple objects in a line

    # the width of the section to center the objects in (can be whole window or just a section of the window)
    # obj_width ... the width of the object
    # list_length ... a integer which shows how many objects there to center

    start_width = (box_width / 2) - ((obj_width / 2)*list_length)
    spacing = obj_width

    return start_width, spacing

def center_obj_height(obj_height, list_length, box_height):
    # Calculates a start_height from which objects can be drawn in lines under each other with spacing

    # Returns values start_height and spacing -> start_height: start height from where to print the first line of text
    #                                        -> spacing: The spacing between two lines (added to the y coordinate of start_height)

    text_height = obj_height * list_length # The total amount of height needed by all lines
    spacing = obj_height
    start_height = (box_height / 2) - (text_height / 2)

    return start_height, spacing

def get_dice_size(max_width, max_height, dices, levels):
    # Returns the size for one dice to not overgo the max width and the max height of the section
    # max_width ... width of the section
    # max_height ... height of the section
    # dices ... number of dices
    # levels ... number of levels of how many dices can be placed under each other

    # Dices must be squares

    max_height /= levels

    width_divided = max_width / dices

    if width_divided <= max_height:
        return (int(width_divided), int(width_divided))
    elif width_divided > max_height:
        return (int(max_height), int(max_height))
