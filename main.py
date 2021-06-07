import pygame
from game.constant_values import WIN_WIDTH, WIN_HEIGHT, WIDTH, HEIGHT, SQUARE_SIZE, ROWS, COLUMNS
from game.board import Board
from game.game import Game
from game.pawn import Pawn

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Warcaby')

FPS = 60


def getRowColumnCoordsFromMousePos(mousePos):
    x, y = mousePos
    # nie sprawdzam czy kursor znajduje się na planszy, będą o tym świadczyły koordynaty np. w postaci
    # (-1, 2) lub (8, 1)
    column = (x - (WIN_WIDTH - WIDTH)/2) // SQUARE_SIZE
    row = (y - (WIN_HEIGHT - HEIGHT)/2) // SQUARE_SIZE
    return int(row), int(column)


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(window)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                mousePos = pygame.mouse.get_pos()
                row, column = getRowColumnCoordsFromMousePos(mousePos)
                if 0 > row or row > ROWS-1 or 0 > column or column > COLUMNS-1:
                    pass
                else:
                    game.select(row, column)

        game.update()

    pygame.quit()


main()


