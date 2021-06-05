import pygame
from pygame import gfxdraw
from .constant_values import BLACK, WHITE, SQUARE_SIZE, WIN_WIDTH, WIN_HEIGHT, WIDTH, HEIGHT, PAWN_SQUARE_RATIO, \
    PAWN_OUTLINE, SCALED_CROWN

#metoda do rysowania wypełnionych okręgów po antialiasingu
def drawAACircle(surface, color, coords, radius):
    x, y = coords
    gfxdraw.aacircle(surface, int(x), int(y), int(radius), color)
    gfxdraw.filled_circle(surface, int(x), int(y), int(radius), color)

class Pawn:
    #TODO: prywatne atrybuty + gettery? czy lepiej zostawić tak?

    def __init__(self, row, column, color):
        #TODO wyjątek, gdy podamy zły row, column
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
        self.calculateXY()

    def calculateXY(self):
        self.x = (WIN_WIDTH - WIDTH) / 2 + SQUARE_SIZE / 2 + self.column * SQUARE_SIZE
        self.y = (WIN_HEIGHT - HEIGHT) / 2 + SQUARE_SIZE / 2 + self.row * SQUARE_SIZE

    def draw(self, windows):
        pass

    def move(self, newRow, newColumn):
        self.row = newRow
        self.column = newColumn
        #todo - wyjatek, gdy podamy zle wartosci row, column
        self.calculateXY()


# zwykły pionek
class JustPawn(Pawn):
    def __init__(self, row, column, color):
        super().__init__(row, column, color)

    def draw(self, window):
        radius = int(SQUARE_SIZE * PAWN_SQUARE_RATIO / 2)
        # obrys
        if PAWN_OUTLINE == 0:
            pass
        else:
            drawAACircle(window, self.invColor, (self.x, self.y), radius + PAWN_OUTLINE)
        # pionek
        drawAACircle(window, self.color, (self.x, self.y), radius)

# "damka"
class KingPawn(Pawn):
    def __init__(self, row, column, color):
        super().__init__(row, column, color)

    def draw(self, window):
        radius = int(SQUARE_SIZE * PAWN_SQUARE_RATIO / 2)
        # obrys
        if PAWN_OUTLINE == 0:
            pass
        else:
            drawAACircle(window, self.invColor, (self.x, self.y), radius + PAWN_OUTLINE)
        # pionek
        drawAACircle(window, self.color, (self.x, self.y), radius)
        window.blit(SCALED_CROWN, (self.x - SCALED_CROWN.get_width()//2, self.y - SCALED_CROWN.get_height()//2))

