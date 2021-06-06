import pygame
from .board import Board
from .constant_values import WHITE, BLACK, BOARD_MEDIUM, SQUARE_SIZE, PAWN_SQUARE_RATIO, WIN_WIDTH, WIDTH, HEIGHT, \
    WIN_HEIGHT
from .draw_methods import drawAACircle


class Game:
    def __init__(self, window):
        self._initValues()
        self.window = window

    # prywatna metoda wydzielona z powodu duplikowania kodu
    def _initValues(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.validMoves = {}

    def reset(self):
        self._initValues()

    # metoda rysująca grę
    def update(self):
        self.board.drawGame(self.window)
        self.drawValidMoves(self.validMoves)
        pygame.display.update()

    # metoda odpowiedzialna za ruszanie pionka
    def _move(self, row, column):
        pawn = self.board.getPawnFromCoords(row, column)
        # sprawdzam czy pole na które chce przestawić jest puste i czy znajduje się w słowniku możliwych ruchów
        if self.selected and pawn == 0 and (row, column) in self.validMoves:
            self.board.movePawn(self.selected, (row, column))
        else:
            return False
        return True

    def changeTurn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    # metoda odpalana przy kliknięciu na pole na planszy
    # TODO - implementacja bicia pionków
    def select(self, row, column):
        # jeżeli coś było już wybrane, kliknięcie pola zadecyduje o tym, czy można przestawić tam piona
        if self.selected:
            result = self._move(row, column)
            if not result:
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

    def drawValidMoves(self, moves):
        for coords in moves:
            row, column = coords
            drawAACircle(self.window,BOARD_MEDIUM,(column * SQUARE_SIZE + SQUARE_SIZE // 2 + (WIN_WIDTH - WIDTH)/2,
                                                        row * SQUARE_SIZE + SQUARE_SIZE // 2 + (WIN_HEIGHT - HEIGHT)/2),
                               SQUARE_SIZE * PAWN_SQUARE_RATIO * 0.5)


