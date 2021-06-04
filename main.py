import pygame
from game.constant_values import WIN_WIDTH, WIN_HEIGHT
from game.board import Board

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Warcaby')

FPS = 60

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False;

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        board.drawGame(window)
        pygame.display.update()


    pygame.quit()



main()


