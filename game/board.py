import pygame
from .constant_values import *
from .pawn import JustPawn, KingPawn, Pawn

class Board:
    def __init__(self):
        # wirtualna plansza - przechowuje aktualny stan gry w postaci [[0, Pawn, 0, Pawn, ...], [...], ...]
        self._board = [[]]
        # TODO - te wartości nie mogą być hard-coded, trzeba by je obliczyć albo matematycznie albo w pętli po _board
        self._blackPawnsLeft = self._whitePawnsLeft = 12
        self._blackKings = self._whiteKings = 0
        self.setUpBoard()

    def setValueAtCoords(self, coords, value):
        row, column = coords
        self._board[row][column] = value
        # TODO - wyjątek, gdy podamy złe współrzędne

    def updatePawnCount(self, color, count):
        if color == WHITE:
            self._whitePawnsLeft += count
        elif color == BLACK:
            self._blackPawnsLeft += count
        else:
            pass
            # TODO - wyjątek gdy podamy zły kolor

    def updateKingsCount(self, color, count):
        if color == WHITE:
            self._whiteKings += count
        elif color == BLACK:
            self._blackKings += count
        else:
            pass
            #TODO - wyjątek gdy podamy zły kolor

    def setUpBoard(self):
        for row in range(ROWS):
            # tworzę plansze 8 wierszy
            self._board.append([])
            for column in range(COLUMNS):
                # "czarne" kwadraty (te, na których mogą znaleźć się pionki)
                if row % 2 == ((column + 1) % 2):
                    if row < PAWN_ROWS_PER_COLOR:
                        self._board[row].append(JustPawn(row, column, BLACK))
                    elif row > ROWS - PAWN_ROWS_PER_COLOR - 1:
                        self._board[row].append(JustPawn(row, column, WHITE))
                    else:
                        self._board[row].append(0)
                else:
                    self._board[row].append(0)

    def drawBoard(self, window):
        # rysowanie "stołu" wraz z planszą
        window.fill(BOARD_MEDIUM)
        pygame.draw.rect(window, BOARD_BLACK, ((WIN_WIDTH - WIDTH)/2 - BORDER_SIZE, (WIN_HEIGHT - HEIGHT)/2 - BORDER_SIZE, WIDTH + BORDER_SIZE * 2, HEIGHT + BORDER_SIZE *2))
        pygame.draw.rect(window, BOARD_DARK, ((WIN_WIDTH - WIDTH)/2, (WIN_HEIGHT - HEIGHT)/2, WIDTH, HEIGHT))

        # rysowanie planszy - dodanie jasnych pól
        for row in range(ROWS):
            for column in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, BOARD_LIGHT, (row * SQUARE_SIZE + (WIN_WIDTH - WIDTH)/2, column * SQUARE_SIZE + (WIN_HEIGHT - HEIGHT)/2, SQUARE_SIZE, SQUARE_SIZE))

        # dodaje oznaczenia
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for i in range(ROWS):
            # liczby
            text = SMALLFONT.render(str(ROWS-i), True, BOARD_DARK)
            x = (WIN_WIDTH - WIDTH) / 2
            y = (WIN_HEIGHT - HEIGHT) / 2
            window.blit(text, (x - BORDER_SIZE * 0.5 - text.get_width()/2, y + SQUARE_SIZE * i + SQUARE_SIZE * 0.5 - text.get_height()/2))
            # litery
            text = SMALLFONT.render(letters[i], True, BOARD_DARK)
            y += HEIGHT
            window.blit(text, (x + i * SQUARE_SIZE + SQUARE_SIZE/2 - text.get_width()/2, y + BORDER_SIZE/2 - text.get_height()/2))


    def drawGame(self, window):
        self.drawBoard(window)
        for row in range(ROWS):
            for column in range(COLUMNS):
                pawn = self._board[row][column]
                if pawn != 0:
                    pawn.draw(window)

    def getPawnFromCoords(self, row, column):
        return self._board[row][column]

    def movePawn(self, pawn, coords):
        row, column = coords
        # Obsługa wirtualnej planszy - zamiana miejscami obiektu pionka z zerem, znajdującym sie do tej pory w
        # miejscu, na które ruszamy piona
        self._board[pawn.getRow()][pawn.getColumn()], self._board[row][column] = self._board[row][column], self._board[pawn.getRow()][pawn.getColumn()]
        pawn.move(row, column)

        # Obsługa zamiany pionka w damkę, gdy dotrzemy do końca planszy.
        if row == 0 and pawn.getColor() == WHITE:
            self._board[row][column] = KingPawn(row, column, WHITE)
            self._whiteKings += 1
        if row == ROWS-1 and pawn.getColor() == BLACK:
            self._board[row][column] = KingPawn(row, column, BLACK)
            self._blackKings += 1

    # TODO - obsługa poruszania się damką
    # metody odpowiedzialne za znalezienie możliwych ruchów dla wybranego pionka
    # sprawdzanie lewej przekątnej od wybranego pionka, prawa działa analogicznie
    def _checkLeftDiagonal(self, start, end, direction, color, column, isKing, skippedPawns=[]):
        # słownik przechowujący dostępne ruchy w postaci: (3,0) = [<Pawn>, <Pawn>, ...], gdzie kluczami są dostępne
        # pola, na które możemy się ruszyć, natomiast wartościami jest lista pól przez które "przeskoczyliśmy" (zbite
        # pionki)
        moves = {}
        # ponieważ pętla może przejść przez max 2 iteracje, w tej zmiennej będę przechowywał zawartość poprzednio
        # analizowanego pola
        previousSquare = []
        # pętla sprawdzająca dostępne ruchy
        for row in range(start, end, direction):
            # jeżeli algorytm wykroczy poza plansze należy go przerwać
            if column < 0:
                break
            # sprawdzam co jest na polu, które aktualnie analizuje
            currentSquare = self.getPawnFromCoords(row, column)
            if currentSquare == 0:
                # jeżeli nic i jest to pierwsze analizowane pole po biciu, nie możemy się tu ruszyć
                if skippedPawns and not previousSquare:
                    break
                # jeżeli nic i jest to drugie analizowane pole bo biciu, dodaje ruch jako możliwy
                elif skippedPawns:
                    print(skippedPawns)
                    moves[(row, column)] = previousSquare + skippedPawns
                # jeżeli nic i nie było bicia, dodaje ruch jako możliwy
                else:
                    moves[(row, column)] = previousSquare

                if previousSquare:
                    # jeżeli nic, a na poprzednim polu był pionek innego koloru - rekurencyjnie wywołuje funkcję,
                    # aby uwzględnić możliwość wielokrotnego bicia

                    # przygotowuje nowe ograniczenia dla funkcji
                    if direction == -1:
                        newEnd = max(row - 3, -1)
                        newEndBackwards = min(row + 3, ROWS)
                    else:
                        newEnd = min(row + 3, ROWS)
                        newEndBackwards = max(row - 3, -1)

                    # sprawdzam możliwe wielokrotne bicia "do przodu"
                    moves.update(self._checkLeftDiagonal(row + direction, newEnd, direction, color, column - 1, isKing,
                                                             skippedPawns = moves[(row, column)]))
                    moves.update(self._checkRightDiagonal(row + direction, newEnd, direction, color, column + 1, isKing,
                                                              skippedPawns = moves[(row, column)]))
                    # jeżeli flaga bicia do tyłu jest ustawiona na True - sprawdzam również bicia do tyłu
                    if ALLOW_SKIPPING_BACKWARDS:
                        # możliwość bicia we wszystkie strony oznacza jednocześnie możliwość wpadnięcia w nieskończoną
                        # pętle przez algorytm, następne ify zabezpieczają program przed taką sytuacją
                        if row - direction >= 0 and row - direction < ROWS and column - 1 >= 0 and column + 1 < COLUMNS:
                            if self.getPawnFromCoords(row - direction, column - 1) not in skippedPawns:
                                moves.update(
                                    self._checkLeftDiagonal(row - direction, newEndBackwards, -direction, color, column - 1, isKing, skippedPawns = moves[(row, column)]))
                            if self.getPawnFromCoords(row - direction, column + 1) not in skippedPawns:
                                moves.update(
                                    self._checkRightDiagonal(row - direction, newEndBackwards, -direction, color, column + 1, isKing, skippedPawns = moves[(row, column)]))
                # wychodzę z pętli aby uniknąć dodawania dodatkowych ruchów po uznaniu ruchu na pierwsze puste pole
                # bez bicia (w przeciwnym wypadku, pionki mogłyby się poruszać na 2 pola do przodu, jeśli oba są wolne)
                if not isKing:
                    break
            # jeżeli pole jest pionkiem tego samego koloru, nie mogę się tu ruszyć
            elif isinstance(currentSquare, Pawn):
                if currentSquare.getColor() == color:
                    break
                # jeżeli nie jest, ustawiam obecne pole jako poprzednie i przechodzę do następnej iteracji
                else:
                    previousSquare = [currentSquare]
            column -= 1

        return moves

    def _checkRightDiagonal(self, start, end, direction, color, column, isKing, skippedPawns = []):
        moves = {}
        previousSquare = []
        for row in range(start, end, direction):
            if column > COLUMNS - 1:
                break
            currentSquare = self.getPawnFromCoords(row, column)
            if currentSquare == 0:
                if skippedPawns and not previousSquare:
                    break
                elif skippedPawns:
                    for pawn in skippedPawns:
                        print(pawn)
                        print(f'Pole pionka: {pawn.getRow()}, {pawn.getColumn()}')
                    for square in previousSquare:
                        print(f'Previous square: {square.getRow()}, {square.getColumn()}')
                    moves[(row, column)] = previousSquare + skippedPawns
                else:
                    moves[(row, column)] = previousSquare

                if previousSquare:
                    if direction == -1:
                        newEnd = max(row - 3, -1)
                        newEndBackwards = min(row + 3, ROWS)
                    else:
                        newEnd = min(row + 3, ROWS)
                        newEndBackwards = max(row - 3, -1)

                    moves.update(self._checkLeftDiagonal(row + direction, newEnd, direction, color, column - 1, isKing,
                                                         skippedPawns = moves[(row, column)]))
                    moves.update(self._checkRightDiagonal(row + direction, newEnd, direction, color, column + 1, isKing,
                                                          skippedPawns = moves[(row, column)]))

                    if ALLOW_SKIPPING_BACKWARDS:
                        if row - direction >= 0 and row - direction < ROWS and column - 1 >= 0 and column + 1 < COLUMNS:
                            if self.getPawnFromCoords(row - direction, column - 1) not in skippedPawns:
                                moves.update(
                                    self._checkLeftDiagonal(row - direction, newEndBackwards, -direction, color, column - 1, isKing, skippedPawns = moves[(row, column)]))
                            if self.getPawnFromCoords(row - direction, column + 1) not in skippedPawns:
                                moves.update(
                                    self._checkRightDiagonal(row - direction, newEndBackwards, -direction, color, column + 1, isKing, skippedPawns = moves[(row, column)]))
                if not isKing:
                    break

            elif isinstance(currentSquare, Pawn):
                if currentSquare.getColor() == color:
                    break
                else:
                    previousSquare = [currentSquare]
            column += 1

        return moves

    def getValidMoves(self, pawn):
        moves = {}
        leftColumn = pawn.getColumn() - 1
        rightColumn = pawn.getColumn() + 1
        row = pawn.getRow()

        if isinstance(pawn, KingPawn):
            moves.update(self._checkLeftDiagonal(row - 1, -1, -1, pawn.getColor(), leftColumn, True))
            moves.update(self._checkRightDiagonal(row - 1, -1, -1, pawn.getColor(), rightColumn, True))
            moves.update(self._checkLeftDiagonal(row + 1, ROWS, 1, pawn.getColor(), leftColumn, isinstance(pawn, KingPawn)))
            moves.update(self._checkRightDiagonal(row + 1, ROWS, 1, pawn.getColor(), rightColumn, isinstance(pawn, KingPawn)))

        if pawn.getColor() == WHITE:
            # zaczynam sprawdzać od pola na przód od pionka (row-1) a sprawdzam 2 pola do przodu (uwzględniam
            # możliwość bicia) lub do wiersza 0 (górny koniec planszy), poruszam się o krok -1 (wiersze maleją "do
            # góry"), ustawiam kolumnę na jedną do lewej
            moves.update(self._checkLeftDiagonal(row - 1, max(row - 3, -1), -1, pawn.getColor(), leftColumn, isinstance(pawn, KingPawn)))
            moves.update(self._checkRightDiagonal(row - 1, max(row - 3, -1), -1, pawn.getColor(), rightColumn, isinstance(pawn, KingPawn)))
            # uwzględniam możliwość bicia do tyłu - tworzę słownik ruchów do tyłu i wybieram z niego tylko te,
            # podczas których pion bije piona przeciwnika
            if ALLOW_SKIPPING_BACKWARDS:
                movesToCheck = {}
                movesToCheck.update(self._checkLeftDiagonal(row + 1, min(row + 3, ROWS), 1, pawn.getColor(), leftColumn, isinstance(pawn, KingPawn)))
                movesToCheck.update(self._checkRightDiagonal(row + 1, min(row + 3, ROWS), 1, pawn.getColor(), rightColumn, isinstance(pawn, KingPawn)))
                for move in movesToCheck:
                    if movesToCheck.get(move):
                        moves[move] = movesToCheck.get(move)

        if pawn.getColor() == BLACK:
            moves.update(self._checkLeftDiagonal(row + 1, min(row + 3, ROWS), 1, pawn.getColor(), leftColumn, isinstance(pawn, KingPawn)))
            moves.update(self._checkRightDiagonal(row + 1, min(row + 3, ROWS), 1, pawn.getColor(), rightColumn, isinstance(pawn, KingPawn)))
            if ALLOW_SKIPPING_BACKWARDS:
                movesToCheck = {}
                movesToCheck.update(self._checkLeftDiagonal(row - 1, max(row - 3, -1), -1, pawn.getColor(), leftColumn, isinstance(pawn, KingPawn)))
                movesToCheck.update(self._checkRightDiagonal(row - 1, max(row - 3, -1), -1, pawn.getColor(), rightColumn, isinstance(pawn, KingPawn)))
                for move in movesToCheck:
                    if movesToCheck.get(move):
                        moves[move] = movesToCheck.get(move)

        return moves