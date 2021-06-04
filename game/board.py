import pygame
from game.constant_values import BOARD_LIGHT, BOARD_DARK, BOARD_MEDIUM, BOARD_BLACK, ROWS, COLUMNS, SQUARE_SIZE, \
    WIN_WIDTH, WIDTH, WIN_HEIGHT, HEIGHT, BORDER_SIZE, BLACK, WHITE
from .pawn import Pawn

class Board:
    def __init__(self):
        #wirtualna plansza - przechowuje aktualna gre w postaci [[0, PION, 0, PION, ...], [...], ...]
        self.board = [[]]
        self.blackPawnsLeft = self.whitePawnsLeft = 12
        self.blackKings = self.whiteKings = 0
        self.setUpBoard()

    def drawSquares(self, window):
        #drawing table
        window.fill(BOARD_MEDIUM)
        #drawing border
        pygame.draw.rect(window, BOARD_BLACK, ((WIN_WIDTH - WIDTH)/2 - BORDER_SIZE, (WIN_HEIGHT - HEIGHT)/2 - BORDER_SIZE, WIDTH + BORDER_SIZE * 2, HEIGHT + BORDER_SIZE *2))
        #drawing board - dark squares
        pygame.draw.rect(window, BOARD_DARK, ((WIN_WIDTH - WIDTH)/2, (WIN_HEIGHT - HEIGHT)/2, WIDTH, HEIGHT))
        #drawing board - light squares
        for row in range(ROWS):
            for column in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, BOARD_LIGHT, (row * SQUARE_SIZE + (WIN_WIDTH - WIDTH)/2, column * SQUARE_SIZE + (WIN_HEIGHT - HEIGHT)/2, SQUARE_SIZE, SQUARE_SIZE))

    def setUpBoard(self):
        for row in range(ROWS):
            #tworze plansze 8 wierszy
            self.board.append([])
            for column in range(COLUMNS):
                #"czarne" kwadraty (te, na których mogą znaleźć się pionki)
                if column % 2 == ((row + 1) % 2):
                    if row in (0, 1, 2):
                        self.board[row].append(Pawn(row, column, BLACK))
                    elif row in (5, 6, 7):
                        self.board[row].append(Pawn(row, column, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def drawGame(self, window):
        self.drawSquares(window)
        for row in range(ROWS):
            for column in range(COLUMNS):
                pawn = self.board[row][column]
                if pawn != 0:
                    pawn.draw(window)


