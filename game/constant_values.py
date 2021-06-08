import pygame

# stałe do rysowania planszy
WIN_WIDTH, WIN_HEIGHT = 700, 800
WIDTH, HEIGHT = 600, 600
BORDER_SIZE = 25

# plansze dotyczące pól i pionków
ROWS, COLUMNS = 8, 8
SQUARE_SIZE = int(HEIGHT/ROWS)
PAWN_SQUARE_RATIO = 0.55
PAWN_OUTLINE = 2
PAWN_ROWS_PER_COLOR = 2

# flagi modyfikujące grę
ALLOW_SKIPPING_BACKWARDS = False
ALLOW_KING_LONGJUMP = False

# stałe zmieniające parametry gry
FPS = 75

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
BIGFONT = pygame.font.Font('assets/Lato/Lato-Black.ttf', 36)

# png
CROWN = pygame.image.load('assets/crown.png')
crownScaleRatio = SQUARE_SIZE * PAWN_SQUARE_RATIO * 0.7 / CROWN.get_width()
SCALED_CROWN = pygame.transform.scale(CROWN, (int(CROWN.get_width() * crownScaleRatio), int(CROWN.get_height() * crownScaleRatio)))


