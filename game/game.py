import pygame
from .board import Board
from .constant_values import WHITE, BLACK, BOARD_MEDIUM, SQUARE_SIZE, PAWN_SQUARE_RATIO, WIN_WIDTH, WIDTH, HEIGHT, \
    WIN_HEIGHT, BIGFONT, BORDER_SIZE
from .draw_methods import drawAACircle
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
        #self.drawTurnInfo(WHITE)
        self.validMoves = {}

    def reset(self):
        self._initValues()

    # metoda rysująca grę
    def update(self):
        self.board.drawGame(self.window)
        self.drawValidMoves(self.validMoves)
        self.drawTurnInfo()
        if self.selected:
            self.drawSelectedPawn(self.selected)
        pygame.display.update()

    # metoda odpowiedzialna za ruszanie pionka
    def _move(self, row, column):
        pawn = self.board.getPawnFromCoords(row, column)
        # sprawdzam czy pole na które chce przestawić jest puste i czy znajduje się w słowniku możliwych ruchów
        if self.selected and pawn == 0 and (row, column) in self.validMoves:
            self.board.movePawn(self.selected, (row, column))

            skippedSquare = self.validMoves[(row, column)]
            if skippedSquare:
                self.board.remove(skippedSquare)

            self.changeTurn()

        else:
            return False
        return True

    def remove(self, pawns):
        for pawn in pawns:
            self.board.setValueAtCoords((pawn.getRow(), pawn.getColumn()), 0)
            self.board.updatePawnCount(pawn.getColor(), -1)
            if isinstance(pawn, KingPawn):
                self.board.updateKingsCount(pawn.getColor(), -1)

    def changeTurn(self):
        # zeruje słownik możliwych ruchów, aby nie przestał się wyświetlać na ekranie
        self.validMoves = {}
        self.selected = None
        if self.turn == WHITE:
            self.turn = BLACK
            #self.drawTurnInfo(BLACK)
        else:
            self.turn = WHITE
            #self.drawTurnInfo(WHITE)


    # metoda odpalana przy kliknięciu na pole na planszy
    # TODO - implementacja bicia pionków
    def select(self, row, column):
        # jeżeli coś było już wybrane, kliknięcie pola zadecyduje o tym, czy można przestawić tam piona
        if self.selected:
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
        row = pawn.getRow()
        column = pawn.getColumn()
        pygame.draw.rect(self.window, BOARD_MEDIUM, (
        column * SQUARE_SIZE + (WIN_WIDTH - WIDTH) / 2, row * SQUARE_SIZE + (WIN_HEIGHT - HEIGHT) / 2, SQUARE_SIZE,
        SQUARE_SIZE))
        pawn.draw(self.window)

    def drawValidMoves(self, moves):
        for coords in moves:
            row, column = coords
            drawAACircle(self.window,BOARD_MEDIUM,(column * SQUARE_SIZE + SQUARE_SIZE // 2 + (WIN_WIDTH - WIDTH)/2,
                                                        row * SQUARE_SIZE + SQUARE_SIZE // 2 + (WIN_HEIGHT - HEIGHT)/2),
                               SQUARE_SIZE * PAWN_SQUARE_RATIO / 2 * PAWN_SQUARE_RATIO)

    def drawTurnInfo(self):
        if self.turn == WHITE:
            text = BIGFONT.render("Tura BIAŁYCH", True, WHITE)
            self.window.blit(text, ((WIN_WIDTH - WIDTH)/2 + WIDTH/2 - text.get_width()/2,
                                    (WIN_HEIGHT - HEIGHT - BORDER_SIZE) / 2 - ((WIN_HEIGHT - HEIGHT - BORDER_SIZE) / 2) / 2 - text.get_height()/2))
        else:
            text = BIGFONT.render("Tura CZARNYCH", True, BLACK)
            self.window.blit(text, ((WIN_WIDTH - WIDTH)/2 + WIDTH/2 - text.get_width()/2,
                                    (WIN_HEIGHT - HEIGHT - BORDER_SIZE) / 2 - ((WIN_HEIGHT - HEIGHT - BORDER_SIZE) / 2) / 2 - text.get_height()/2))
