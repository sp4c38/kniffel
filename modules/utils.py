import sys

def get_font_by_size(pygame, box_size, text, list_length, settings):
    # This finds the font size which is needed to make a text fit into a specific width and height / returns font_size
    # box_size are the width and the height where the text shall fit in (as tuple)
    # list_length is the length of the list which is needed for making the text also fit in height

    font_size_found = False
    font_size = 1
    previouse_font_size = font_size

    while not font_size_found:
        font = pygame.font.Font(settings["font"], font_size)
        size = font.size(text)
        text_size = (size[0], font.get_height()*list_length)

        if text_size[0] <= box_size[0] and text_size[1] <= box_size[1]:
            previouse_font_size = font_size
        elif not text_size[0] <= box_size[0] or not text_size[1] <= box_size[1] and previouse_font_size:
            font_size_found = True
        else:
            print(f"A good font size couldn't be found because the font size 1 already didn't match.")
            sys.exit(1)
            font_size_found = True

        font_size += 1

    if previouse_font_size == None:
        import IPython;IPython.embed();import sys;sys.exit()
    return previouse_font_size

def center_obj_width(pygame, obj_width, list_length, window_width):
    # Only works if obj_width is always the same (outside this function)
    # Finds the position on the x axis to center some object

    # obj_width ... the width of the object
    # list_length ... a integer which shows how many objects there to center

    start_point = (window_width / 2) - ((obj_width / 2)*list_length)
    summand = obj_width

    return start_point, summand

def center_obj_height(pygame, obj_height, list_length, window_height):
    # This function calculates certain stuff to make it possible to center multi-line (or single-line) objects by height
    # ! Only for height
    # Returns values start_point and summand -> start_point: start coordinates from where to print the top left corner of the text
    #                                        -> summand: what to add to start_point for the next text print (only height)
    text_height = obj_height * list_length # The height of all text
    summand = text_height / list_length # Yeah, but need text_height for other reasons <- faster to do it this way for the computer (think so)
    start_point = (window_height / 2) - (text_height / 2)

    return start_point, summand

def get_dice_size(width, max_height, dices):
    # This function returns a size for each dice so that the site a doesn't overgo the maximal height definied in settings for the dice section
    # width ... width of the information page
    # dices ... how many dices do we have

    width_divided = width / dices

    if width_divided < max_height: 
        return (width_divided, width_divided)
    elif max_height < width_divided: 
        return (max_height, max_height)
    elif max_height == width_divided: 
        return (max_height, max_height)