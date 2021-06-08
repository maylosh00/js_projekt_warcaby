import pygame
from pygame import gfxdraw

# metoda do rysowania kółek po antialiasingu
def drawAACircle(surface, color, coords, radius):
    """
    Draws antialiased circle
    :param surface: pygame.display object
    :param color: representation of color in tuple[int, int, int] format
    :param coords: coordinates in tuple[int, int] format of row and column
    :param radius: int
    """
    x, y = coords
    gfxdraw.aacircle(surface, int(x), int(y), int(radius), color)
    gfxdraw.filled_circle(surface, int(x), int(y), int(radius), color)