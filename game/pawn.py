from .assets_constants import SCALED_CROWN
from .constant_values import BLACK, WHITE, SQUARE_SIZE, WIN_WIDTH, WIN_HEIGHT, WIDTH, HEIGHT, PAWN_SQUARE_RATIO, \
    PAWN_OUTLINE, ROWS, COLUMNS
from .draw_methods import drawAACircle
from .exceptions import incorrectCoordinatesException, incorrectColorValueException


class Pawn:
    def __init__(self, row, column, color):
        if row < 0 or row >= ROWS or column < 0 or column >= COLUMNS:
            raise incorrectCoordinatesException('Row/column value has to be in the range [0,ROWS/COLUMNS)')
        self._row = row
        self._column = column

        if color == WHITE:
            self._invColor = BLACK
        elif color == BLACK:
            self._invColor = WHITE
        else:
            raise incorrectColorValueException('Only black / white colored pawns are accepted')
        self._color = color

        self.x = 0
        self.y = 0
        self._calculateXY()

    def _calculateXY(self):
        """
        Sets x and y value to coordinates (in pixels) at which the center of a pawn is located
        """
        self.x = (WIN_WIDTH - WIDTH) / 2 + SQUARE_SIZE / 2 + self._column * SQUARE_SIZE
        self.y = (WIN_HEIGHT - HEIGHT) / 2 + SQUARE_SIZE / 2 + self._row * SQUARE_SIZE

    # gettery
    def getRow(self):
        """
        Pawn row getter
        :return: int: row
        """
        return self._row
    def getColumn(self):
        """
        Pawn column getter
        :return: int: column
        """
        return self._column
    def getColor(self):
        """
        Pawn color getter
        :return: color: representation of color in (int, int, int) format
        """
        return self._color

    # prywatna metoda wydzielona z powodu duplikowania kodu
    def _drawPawnBase(self, window):
        """
        Draws pawn without special elements in a given window
        :param window: pygame.display object
        """
        radius = int(SQUARE_SIZE * PAWN_SQUARE_RATIO / 2)
        # obrys
        if PAWN_OUTLINE == 0:
            pass
        else:
            drawAACircle(window, self._invColor, (self.x, self.y), radius + PAWN_OUTLINE)
        # pionek
        drawAACircle(window, self._color, (self.x, self.y), radius)

    # metoda do nadpisania
    def draw(self, window):
        """
        Draws pawn in a given window
        :param window: pygame.display object
        """
        pass

    def move(self, newRow, newColumn):
        """
        Changes pawn's (row, column) coordinates
        :param newRow: int: value to change pawn's row to
        :param newColumn: int: value to change pawn's column to
        """
        if newRow < 0 or newRow >= ROWS or newColumn < 0 or newColumn >= COLUMNS:
            raise incorrectCoordinatesException('Row/column value has to be in the range [0,ROWS/COLUMNS)')
        self._row = newRow
        self._column = newColumn
        self._calculateXY()


# zwyk??y pionek
class JustPawn(Pawn):
    def __init__(self, row, column, color):
        super().__init__(row, column, color)

    def draw(self, window):
        """
        Draws pawn in a given window
        :param window: pygame.display object
        """
        self._drawPawnBase(window)

# "damka"
class KingPawn(Pawn):
    def __init__(self, row, column, color):
        super().__init__(row, column, color)

    def draw(self, window):
        """
        Draws pawn in a given window
        :param window: pygame.display object
        """
        self._drawPawnBase(window)
        window.blit(SCALED_CROWN, (self.x - SCALED_CROWN.get_width()//2, self.y - SCALED_CROWN.get_height()//2))

