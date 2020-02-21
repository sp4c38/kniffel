import sys

def get_font_by_size(pygame, box_size, text, list_length, settings):
    # This finds the font size which is needed to make a text fit into a specific width and height / returns font_size
    # box_size are the width and the height where the text shall fit in (as tuple)
    # list_length is the length of the list which is needed for making the text also fit in height

    font_size_found = False
    font_size = 1
    previouse_matched = None

    while not font_size_found:
        font = pygame.font.Font(settings["font"], font_size)
        size = font.size(text)
        text_size = (size[0], font.get_height()*list_length)

        if text_size[0] <= box_size[0] and text_size[1] <= box_size[1]:
            previouse_matched = font_size
        elif not text_size[0] <= box_size[0] or not text_size[1] <= box_size[1] and previouse_matched:
            font_size_found = True
        else:
            print(f"A good font size couldn't be found because the font size 1 already didn't match.")
            sys.exit(1)
            font_size_found = True

        font_size += 1

    return previouse_matched

def center_text_width(pygame, font, text, window_width):
    # Only works for single-line
    # Finds the position on the x axis to center text

    text_width = font.size(text)[0]
    xposition = (window_width / 2) - (text_width / 2)

    return xposition

def center_text_height(pygame, font, text_list, window_height):
    # This function calculates certain stuff to make it possible to center multi-line (or single-line) text by height
    # ! Only for height
    # Returns values start_point and summand -> start_point: start coordinates from where to print the top left corner of the text
    #                                        -> summand: what to add to start_point for the next text print (only height)
    
    length = len(text_list) # How many items are in text_list
    text_height = font.get_height() * length # The height of all text
    summand = text_height / length # Yeah, but need text_height for other reasons <- faster to do it this way for the computer (think so)
    start_point = (window_height / 2) - (text_height / 2)

    return start_point, summand
