import pygame
from .board import Board
from .constant_values import WHITE, BLACK, BOARD_MEDIUM, SQUARE_SIZE, PAWN_SQUARE_RATIO, WIN_WIDTH, WIDTH, HEIGHT, \
    WIN_HEIGHT, BIGFONT, BORDER_SIZE, BOARD_BLACK, SMALLFONT, ROWS, COLUMNS
from .draw_methods import drawAACircle
from .exceptions import incorrectColorValueException, incorrectCoordinatesException
from .pawn import KingPawn


class Game:
    def __init__(self, window):
        self.window = window
        self._initValues()

    # prywatna metoda wydzielona z powodu duplikowania kodu
    def _initValues(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.validMoves = {}
        self._winner = None

    def setUpCustomGame(self, board, color):
        """
        Sets up custom game with given board and color which starts
        :param board: list of lists of integers / Pawn objects
        :param color: representation of color in tuple[int, int, int] format
        :return:
        """
        if color != WHITE or color != BLACK:
            raise incorrectColorValueException('Only black / white colored pawns are accepted')
        self._initValues()
        self.board.setUpCustomBoard(board)
        self.turn = color

    def reset(self):
        self._initValues()

    # metoda rysująca grę / ekran końcowy
    def update(self):
        """
        Method drawing the game / winner screen
        """
        self._winner = self.returnWinner()
        if self._winner:
            self._drawWinnerMessage(self._winner)
        else:
            self.board.drawGame(self.window)
            self.drawValidMoves(self.validMoves)
            self.drawTurnInfo()
            if self.selected:
                self.drawSelectedPawn(self.selected)

        pygame.display.update()

    # metoda odpowiedzialna za ruszanie pionka
    def _move(self, row, column):
        """
        Method checking if selected pawn can be moved to (row, column)
        :param row: int
        :param column: int
        :return: boolean - True if pawn has been moved, False if not
        """
        pawn = self.board.getPawnFromCoords(row, column)
        # sprawdzam czy pole na które chce przestawić jest puste i czy znajduje się w słowniku możliwych ruchów
        if self.selected and pawn == 0 and (row, column) in self.validMoves:
            self.board.movePawn(self.selected, (row, column))

            skippedSquares = self.validMoves[(row, column)]
            if skippedSquares:
                self.remove(skippedSquares)

            self.changeTurn()
        else:
            return False
        return True

    # metoda odpowiedzialna za usunięcie pionków
    def remove(self, pawns):
        """
        Method removing pawns from a board
        :param pawns: list of Pawn objects
        """
        for pawn in pawns:
            self.board.setValueAtCoords((pawn.getRow(), pawn.getColumn()), 0)
            self.board.updatePawnCount(pawn.getColor(), -1)
            if isinstance(pawn, KingPawn):
                self.board.updateKingsCount(pawn.getColor(), -1)

    def returnWinner(self):
        """
        checks if game has been finished and returns winner
        :return: color in tuple[int,int,int] format or None
        """
        if self.board.getPawnsLeft(WHITE) <= 0:
            return BLACK
        elif self.board.getPawnsLeft(BLACK) <= 0:
            return WHITE
        return None

    def changeTurn(self):
        """
        Changes turn from one color to another, clears selected pawn and it's valid moves
        """
        # zeruje słownik możliwych ruchów, aby nie przestał się wyświetlać na ekranie
        self.validMoves = {}
        self.selected = None
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    # metoda odpalana przy kliknięciu na pole na planszy
    def select(self, row, column):
        """
        Selects pawn from a given row, column
        If something has already been selected checks if it can be moved to a given row, column
        If row, column is the same as selected pawn's row, column, clear select
        :param row: int
        :param column: int
        """

        if row < 0 or row >= ROWS or column < 0 or column >= COLUMNS:
            raise incorrectCoordinatesException('Row/column value has to be in the range [0,ROWS/COLUMNS)')

        # jeżeli coś było już wybrane, kliknięcie pola zadecyduje o tym, czy można przestawić tam piona
        if self.selected:
            # jeżeli wybieramy drugi raz to samo pole, odznaczamy je
            if self.selected.getRow() == row and self.selected.getColumn() == column:
                self.selected = None
                self.validMoves = {}
                return False

            result = self._move(row, column)
            if not result:
                # zeruje słownik możliwych ruchów, aby nie przestał się wyświetlać na ekranie
                self.validMoves = {}
                self.selected = None
                self.select(row, column)
        # zbieram to co się znajduje na klikniętym polu, sprawdzam czy to pionek odpowiedniego koloru i jakie ma
        # możliwe ruchy
        pawn = self.board.getPawnFromCoords(row, column)
        if pawn != 0 and pawn.getColor() == self.turn:
            self.selected = pawn
            self.validMoves = self.board.getValidMoves(pawn)
            return True

        return False

    def drawSelectedPawn(self, pawn):
        """
        Highlights given pawn on a board
        :param pawn: Pawn object
        """
        row = pawn.getRow()
        column = pawn.getColumn()
        pygame.draw.rect(self.window, BOARD_MEDIUM, (
        column * SQUARE_SIZE + (WIN_WIDTH - WIDTH) / 2, row * SQUARE_SIZE + (WIN_HEIGHT - HEIGHT) / 2, SQUARE_SIZE,
        SQUARE_SIZE))
        pawn.draw(self.window)

    def drawValidMoves(self, moves):
        """
        Highlights valid moves as little circles on a board
        :param moves: list of tuple[int,int] objects
        """
        for coords in moves:
            row, column = coords
            if row < 0 or row >= ROWS or column < 0 or column >= COLUMNS:
                raise incorrectCoordinatesException('Row/column value has to be in the range [0,ROWS/COLUMNS)')
            drawAACircle(self.window,BOARD_MEDIUM,(column * SQUARE_SIZE + SQUARE_SIZE // 2 + (WIN_WIDTH - WIDTH)/2,
                                                        row * SQUARE_SIZE + SQUARE_SIZE // 2 + (WIN_HEIGHT - HEIGHT)/2),
                               SQUARE_SIZE * PAWN_SQUARE_RATIO / 2 * PAWN_SQUARE_RATIO)

    def drawTurnInfo(self):
        """
        Draws text information about which color's turn is it now above the board
        """
        if self.turn == WHITE:
            text = BIGFONT.render("Tura BIAŁYCH", True, WHITE)
            self.window.blit(text, ((WIN_WIDTH - WIDTH)/2 + WIDTH/2 - text.get_width()/2,
                                    (WIN_HEIGHT - HEIGHT - BORDER_SIZE) / 2 - ((WIN_HEIGHT - HEIGHT - BORDER_SIZE) / 2) / 2 - text.get_height()/2))
        else:
            text = BIGFONT.render("Tura CZARNYCH", True, BLACK)
            self.window.blit(text, ((WIN_WIDTH - WIDTH)/2 + WIDTH/2 - text.get_width()/2,
                                    (WIN_HEIGHT - HEIGHT - BORDER_SIZE) / 2 - ((WIN_HEIGHT - HEIGHT - BORDER_SIZE) / 2) / 2 - text.get_height()/2))

    def _drawWinnerMessage(self, color):
        """
        Draws information about winner and asks to play again / quit the game after winning
        :param color: color in tuple[int,int,int] format or None
        """
        self.window.fill(BOARD_MEDIUM)
        pygame.draw.rect(self.window, BOARD_BLACK, (
            (WIN_WIDTH - WIDTH) / 2 - BORDER_SIZE, (WIN_HEIGHT - HEIGHT) / 2 - BORDER_SIZE, WIDTH + BORDER_SIZE * 2,
            HEIGHT + BORDER_SIZE * 2))
        if color == WHITE:
            text = BIGFONT.render("Wygrały BIAŁE!", True, WHITE)
        else:
            text = BIGFONT.render("Wygrały CZARNE!", True, WHITE)
        self.window.blit(text, ((WIN_WIDTH - WIDTH)/2 + WIDTH/2 - text.get_width()/2,
                                    WIN_HEIGHT/2 - text.get_height()/2 - HEIGHT/4))

        longtext1 = SMALLFONT.render("Aby rozpocząć nową grę - wciśnij ENTER", True, WHITE)
        longtext2 = SMALLFONT.render("Aby wyjść - wciśnij Q", True, WHITE)

        self.window.blit(longtext1, ((WIN_WIDTH - WIDTH)/2 + WIDTH/2 - longtext1.get_width()/2,
                                    WIN_HEIGHT/2 - text.get_height()/2 - HEIGHT/4 + text.get_height()*1.5))
        self.window.blit(longtext2, ((WIN_WIDTH - WIDTH)/2 + WIDTH/2 - longtext2.get_width()/2,
                                    WIN_HEIGHT/2 - text.get_height()/2 - HEIGHT/4 + text.get_height()*1.5 + longtext1.get_height()*1.5))
