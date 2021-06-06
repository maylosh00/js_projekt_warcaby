import pygame
from pygame import gfxdraw

# metoda do rysowania kółek po antialiasingu
def drawAACircle(surface, color, coords, radius):
    x, y = coords
    gfxdraw.aacircle(surface, int(x), int(y), int(radius), color)
    gfxdraw.filled_circle(surface, int(x), int(y), int(radius), color)