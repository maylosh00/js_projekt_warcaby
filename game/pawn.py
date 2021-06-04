import pygame
from pygame import gfxdraw
from .constant_values import BLACK, WHITE, SQUARE_SIZE, WIN_WIDTH, WIN_HEIGHT, WIDTH, HEIGHT, PAWN_SQUARE_RATIO, PAWN_RADIUS

#metoda do rysowania wypełnionych okręgów po antialiasingu
def drawAACircle(surface, color, coords, radius):
    x, y = coords
    gfxdraw.aacircle(surface, int(x), int(y), int(radius), color)
    gfxdraw.filled_circle(surface, int(x), int(y), int(radius), color)

class Pawn:
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color

        if self.color == WHITE:
            self.invColor = BLACK
            self.dir = 1
        elif self.color == BLACK:
            self.invColor = WHITE
            self.dir = -1
        #TODO wyjątek, gdy wpiszemy zły kolor

        self.x = 0
        self.y = 0
        self.calculatePos()

    def calculatePos(self):
        self.x = (WIN_WIDTH - WIDTH) / 2 + SQUARE_SIZE / 2 + self.column * SQUARE_SIZE
        self.y = (WIN_HEIGHT - HEIGHT) / 2 + SQUARE_SIZE / 2 + self.row * SQUARE_SIZE

    def draw(self, windows):
        radius = int(SQUARE_SIZE * PAWN_SQUARE_RATIO / 2)
        #outline
        if PAWN_RADIUS == 0:
            pass
        else:
            drawAACircle(windows, self.invColor, (self.x, self.y), radius + PAWN_RADIUS)
        #pawn
        drawAACircle(windows, self.color, (self.x, self.y), radius)