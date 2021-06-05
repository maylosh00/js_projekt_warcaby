import pygame

# TODO - stałe potrzebne tylko dla konkretnych klas wrzuć do tych klas

# stałe do rysowania planszy
WIN_WIDTH, WIN_HEIGHT = 700, 800
WIDTH, HEIGHT = 600, 600
BORDER_SIZE = 25

# plansze dotyczące pól i pionków
ROWS, COLUMNS = 8, 8
SQUARE_SIZE = int(HEIGHT/ROWS)
PAWN_SQUARE_RATIO = 0.55
PAWN_OUTLINE = 2

# kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BOARD_LIGHT = (227, 206, 187)
BOARD_DARK = (112, 68, 53)
BOARD_MEDIUM = (161, 105, 86)
BOARD_BLACK = (36, 17, 11)

# tekst
pygame.font.init()
SMALLFONT = pygame.font.Font('assets/Lato/Lato-Bold.ttf', 18)

# png
# TODO - posprzątaj tu
CROWN = pygame.image.load('assets/crown.png')
CROWN_SCALE_RATIO = SQUARE_SIZE * PAWN_SQUARE_RATIO * 0.7 / CROWN.get_width()
SCALED_CROWN = pygame.transform.scale(CROWN, (int(CROWN.get_width() * CROWN_SCALE_RATIO), int(CROWN.get_height() * CROWN_SCALE_RATIO)))


