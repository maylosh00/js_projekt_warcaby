import pygame
from .constant_values import BLACK, WHITE, SQUARE_SIZE, WIN_WIDTH, WIN_HEIGHT, WIDTH, HEIGHT, PAWN_SQUARE_RATIO, \
    PAWN_OUTLINE, SCALED_CROWN
from .draw_methods import drawAACircle

class Pawn:
    def __init__(self, row, column, color):
        #TODO wyjątek, gdy podamy zły row, column
        self._row = row
        self._column = column

        if color == WHITE:
            self._invColor = BLACK
        else:
            self._invColor = WHITE
        self._color = color
        #TODO wyjątek, gdy wpiszemy zły kolor

        self.x = 0
        self.y = 0
        self.calculateXY()

    def calculateXY(self):
        self.x = (WIN_WIDTH - WIDTH) / 2 + SQUARE_SIZE / 2 + self._column * SQUARE_SIZE
        self.y = (WIN_HEIGHT - HEIGHT) / 2 + SQUARE_SIZE / 2 + self._row * SQUARE_SIZE

    # ettery
    def getRow(self):
        return self._row
    def getColumn(self):
        return self._column
    def getColor(self):
        return self._color

    # prywatna metoda wydzielona z powodu duplikowania kodu
    def _drawPawnBase(self, window):
        radius = int(SQUARE_SIZE * PAWN_SQUARE_RATIO / 2)
        # obrys
        if PAWN_OUTLINE == 0:
            pass
        else:
            drawAACircle(window, self._invColor, (self.x, self.y), radius + PAWN_OUTLINE)
        # pionek
        drawAACircle(window, self._color, (self.x, self.y), radius)

    def draw(self, window):
        pass

    def move(self, newRow, newColumn):
        self._row = newRow
        self._column = newColumn
        #todo - wyjatek, gdy podamy zle wartosci row, column
        self.calculateXY()


# zwykły pionek
class JustPawn(Pawn):
    def __init__(self, row, column, color):
        super().__init__(row, column, color)

    def draw(self, window):
        self._drawPawnBase(window)

# "damka"
class KingPawn(Pawn):
    def __init__(self, row, column, color):
        super().__init__(row, column, color)

    def draw(self, window):
        self._drawPawnBase(window)
        window.blit(SCALED_CROWN, (self.x - SCALED_CROWN.get_width()//2, self.y - SCALED_CROWN.get_height()//2))

