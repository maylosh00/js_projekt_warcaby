import pygame
from game.constant_values import WIN_WIDTH, WIN_HEIGHT, WIDTH, HEIGHT, SQUARE_SIZE, ROWS, COLUMNS, FPS
from game.game import Game


# funkcja znajdująca położenie myszki na planszy w postaci (row, column)
def getRowColumnCoordsFromMousePos(mousePos):
    """
    Calculates coordinates in (row, column) format from given mouse position
    :param mousePos: tuple[int,int]
    :return: tuple[int,int]
    """
    x, y = mousePos
    # nie sprawdzam czy kursor znajduje się na planszy, będą o tym świadczyły koordynaty np. w postaci
    # (-1, 2) lub (8, 1)
    column = (x - (WIN_WIDTH - WIDTH) / 2) // SQUARE_SIZE
    row = (y - (WIN_HEIGHT - HEIGHT) / 2) // SQUARE_SIZE
    return int(row), int(column)


def main():
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Warcaby')

    # zmienne potrzebne do poprawnego przebiegu gry (flaga run, clock z biblioteki pygame, obiekt klasy Game)
    run = True
    clock = pygame.time.Clock()
    game = Game(window)

    while run:
        # używam metody tick do aktualizowania zegara i czekania odpowiednią ilość czasu, aby gra chodziła w podanej
        # ilości klatek na sekundę.
        clock.tick(FPS)
        # nasłuchuje zdarzeń (wyłączenia gry lub kliknięcia myszą)
        events = pygame.event.get()
        for event in events:
            # wyłączam grę gry zdarzeniem okarze się quit (wyłączenie przez naciśniecie x)
            if event.type == pygame.QUIT:
                run = False
            # gdy klikniemy, odpalam metodę select w obiekcie game, tam zaczyna się cała gama funkcjonalności
            # programu
            if event.type == pygame.MOUSEBUTTONDOWN:
                # sprawdzam w jakim rzędzie i kolumnie się znajduje po kliknięciu myszą
                mousePos = pygame.mouse.get_pos()
                row, column = getRowColumnCoordsFromMousePos(mousePos)
                # upewniam się, czy kliknięte zostało pole na planszy, czy coś poza nią
                if 0 > row or row > ROWS - 1 or 0 > column or column > COLUMNS - 1:
                    pass
                else:
                    game.select(row, column)

            if game.returnWinner():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                    if event.key == pygame.K_RETURN:
                        game.reset()
        # po sprawdzeniu czy zaszło wydarzenie, używam metody update z klasy game aby na nowo narysować planszę
        game.update()

    # jeżeli run zostało ustawione na False, wychodzę z gry
    pygame.quit()


main()
