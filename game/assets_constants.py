import os
import pygame

# tekst
from game.constant_values import SQUARE_SIZE, PAWN_SQUARE_RATIO

pygame.font.init()
# latoBoldPath = os.path.join(os.getcwd(), 'assets', 'Lato', 'Lato-Bold.ttf')
# latoBlackPath = os.path.join(os.getcwd(), 'assets', 'Lato', 'Lato-Black.ttf')

LATO_BOLD_18 = pygame.font.Font('assets/Lato/Lato-Bold.ttf', 18)
LATO_BLACK_36 = pygame.font.Font('assets/Lato/Lato-Black.ttf', 36)

# png
# crownPath = os.path.join(os.getcwd(), 'assets/crown.png')
CROWN = pygame.image.load('assets/crown.png')
crownScaleRatio = SQUARE_SIZE * PAWN_SQUARE_RATIO * 0.7 / CROWN.get_width()
SCALED_CROWN = pygame.transform.scale(CROWN, (int(CROWN.get_width() * crownScaleRatio), int(CROWN.get_height() * crownScaleRatio)))
