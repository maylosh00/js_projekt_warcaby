import pygame
from .board import Board
from .constant_values import WHITE, BLACK


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

    def update(self):
        self.board.drawGame(self.window)
        pygame.display.update()

    def _move(self, row, column):
        pawn = self.board.getPawnFromCoords(row, column)
        if self.selected and pawn == 0 and (row, column) in self.validMoves:
            self.board.movePawn(self.selected, row, column)
        else:
            return False
        return True

    def changeTurn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def select(self, row, column):
        # jeżeli coś było już wybrane, kliknięcie pola zadecyduje o tym, czy można przestawić tam piona
        if self.selected:
            result = self._move(row, column)
            if not result:
                self.selected = None
                self.select(row, column)
        # jeżeli nie było, zbieram to co się znajduje na klikniętym polu, sprawdzam czy to pionek i jakie ma możliwe
        # ruchy do wykonania
        else:
            pawn = self.board.getPawnFromCoords(row, column)
            if pawn != 0 and pawn.getColor() == self.turn:
                self.selected = pawn
                self.validMoves = self.board.getValidMoves()
                return True

        return False

