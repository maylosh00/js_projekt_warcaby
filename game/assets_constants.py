import pygame

# tekst
from game.constant_values import SQUARE_SIZE, PAWN_SQUARE_RATIO

pygame.font.init()

LATO_BOLD_18 = pygame.font.Font('assets/Lato-Bold.ttf', 18)
LATO_REGULAR_18 = pygame.font.Font('assets/Lato-Regular.ttf', 18)
LATO_BLACK_36 = pygame.font.Font('assets/Lato-Black.ttf', 36)

# png
CROWN = pygame.image.load('assets/crown.png')
crownScaleRatio = SQUARE_SIZE * PAWN_SQUARE_RATIO * 0.7 / CROWN.get_width()
SCALED_CROWN = pygame.transform.scale(CROWN, (int(CROWN.get_width() * crownScaleRatio),
                                              int(CROWN.get_height() * crownScaleRatio)))
