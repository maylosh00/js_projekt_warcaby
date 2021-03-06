import pygame

# flagi modyfikujące grę !!!
ALLOW_SKIPPING_BACKWARDS = True
ALLOW_KING_LONGJUMP = True

# stałe do rysowania planszy
WIN_WIDTH, WIN_HEIGHT = 700, 800
WIDTH, HEIGHT = 600, 600
BORDER_SIZE = 25

# stałe dotyczące pól i pionków !!!
ROWS = COLUMNS = 12
PAWN_ROWS_PER_COLOR = 5

PAWN_OUTLINE = 2
SQUARE_SIZE = int(HEIGHT/ROWS)
PAWN_SQUARE_RATIO = 0.55

# stałe zmieniające parametry gry
FPS = 75

# kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BOARD_LIGHT = (227, 206, 187)
BOARD_DARK = (112, 68, 53)
BOARD_MEDIUM = (161, 105, 86)
BOARD_BLACK = (36, 17, 11)

