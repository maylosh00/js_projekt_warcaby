import pygame
from .constant_values import *
from .pawn import Pawn

class Board:
    def __init__(self):
        #wirtualna plansza - przechowuje aktualna gre w postaci [[0, Pawn, 0, Pawn, ...], [...], ...]
        self.board = [[]]
        self.selectedPawn = None
        self.blackPawnsLeft = self.whitePawnsLeft = 12
        self.blackKings = self.whiteKings = 0
        self.setUpBoard()

    def drawBoard(self, window):
        #rysowanie "stołu" wraz z planszą
        window.fill(BOARD_MEDIUM)
        pygame.draw.rect(window, BOARD_BLACK, ((WIN_WIDTH - WIDTH)/2 - BORDER_SIZE, (WIN_HEIGHT - HEIGHT)/2 - BORDER_SIZE, WIDTH + BORDER_SIZE * 2, HEIGHT + BORDER_SIZE *2))
        pygame.draw.rect(window, BOARD_DARK, ((WIN_WIDTH - WIDTH)/2, (WIN_HEIGHT - HEIGHT)/2, WIDTH, HEIGHT))

        #rysowanie planszy - dodanie jasnych pól
        for row in range(ROWS):
            for column in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, BOARD_LIGHT, (row * SQUARE_SIZE + (WIN_WIDTH - WIDTH)/2, column * SQUARE_SIZE + (WIN_HEIGHT - HEIGHT)/2, SQUARE_SIZE, SQUARE_SIZE))

        #dodaje oznaczenia
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for i in range(8):
            #cyfry
            text = SMALLFONT.render(str(8-i), True, BOARD_DARK)
            x = (WIN_WIDTH - WIDTH) / 2
            y = (WIN_HEIGHT - HEIGHT) / 2
            window.blit(text, (x - BORDER_SIZE * 0.7, y + SQUARE_SIZE * i + SQUARE_SIZE * 0.3))

            #litery
            text = SMALLFONT.render(letters[i], True, BOARD_DARK)
            y += HEIGHT
            window.blit(text, (x + i * SQUARE_SIZE + SQUARE_SIZE * 0.4, y + BORDER_SIZE * 0.05))



    def setUpBoard(self):
        for row in range(ROWS):
            #tworze plansze 8 wierszy
            self.board.append([])
            for column in range(COLUMNS):
                #"czarne" kwadraty (te, na których mogą znaleźć się pionki)
                if row % 2 == ((column + 1) % 2):
                    if row in (0, 1, 2):
                        self.board[row].append(Pawn(row, column, BLACK))
                    elif row in (5, 6, 7):
                        self.board[row].append(Pawn(row, column, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def drawGame(self, window):
        self.drawBoard(window)
        for row in range(ROWS):
            for column in range(COLUMNS):
                pawn = self.board[row][column]
                if pawn != 0:
                    pawn.draw(window)


