import pygame
import unittest

from game.constant_values import WIN_WIDTH, WIN_HEIGHT, BLACK, WHITE
from game.game import Game
from game.pawn import JustPawn, KingPawn


class EnglishCheckersTest(unittest.TestCase):
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    testBoard = [[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, JustPawn(2, 3, BLACK), 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, JustPawn(4, 1, BLACK), 0, 0, 0, 0, 0, 0],
                 [JustPawn(5, 0, WHITE), 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]]

    def test_shouldReturnTrue_forTwoMovesPerPlay(self):
        # given
        game = Game(self.window)
        moves = []
        # when
        game.select(5, 2)
        moves.append(game.select(4, 1))
        game.select(2, 1)
        moves.append(game.select(3, 2))
        game.select(6, 3)
        moves.append(game.select(5, 2))
        game.select(1, 2)
        moves.append(game.select(2, 1))
        # then
        self.assertEqual(moves, [True, True, True, True])

    def test_shouldReturnFalse_whenSelectedMoveIsIncorrect(self):
        # given
        game = Game(self.window)
        # when
        game.select(5,2)
        move = game.select(2, 3)
        # then
        self.assertFalse(move)

    def test_shouldReturnTrue_whenSkippedOnePawnSuccessfully(self):
        game = Game(self.window)
        testBoard = [[0, JustPawn(0, 1, BLACK), 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, JustPawn(4, 3, BLACK), 0, 0, 0, 0],
                     [0, 0, JustPawn(5, 2, WHITE), 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0]]
        game.setUpCustomGame(testBoard, WHITE)

        game.select(5, 2)
        skip = game.select(3, 4)

        self.assertTrue(skip)

    def test_shouldRemovePawnFromBoard_afterSkipping(self):
        game = Game(self.window)
        testBoard = [[0, JustPawn(0, 1, BLACK), 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, JustPawn(4, 3, BLACK), 0, 0, 0, 0],
                     [0, 0, JustPawn(5, 2, WHITE), 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0]]
        game.setUpCustomGame(testBoard, WHITE)

        game.select(5, 2)
        skip = game.select(3, 4)

        self.assertEqual(game.board.getPawnFromCoords(4, 3), 0)

    def test_shouldReturnTrue_whenSkippedManyPawnsSuccessfully(self):
        game = Game(self.window)
        testBoard = [[0, JustPawn(0, 1, BLACK), 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, JustPawn(2, 5, BLACK), 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, JustPawn(4, 3, BLACK), 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, JustPawn(6, 1, BLACK), 0, 0, 0, 0, 0, 0],
                     [JustPawn(7, 0, WHITE), 0, 0, 0, 0, 0, 0, 0]]
        game.setUpCustomGame(testBoard, WHITE)

        game.select(7,0)
        skip = game.select(1,6)

        self.assertTrue(skip)

    def test_shouldRemovePawnsFromBoard_afterMultiSkipping(self):
        game = Game(self.window)
        testBoard = [[0, JustPawn(0, 1, BLACK), 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, JustPawn(2, 5, BLACK), 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, JustPawn(4, 3, BLACK), 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, JustPawn(6, 1, BLACK), 0, 0, 0, 0, 0, 0],
                     [JustPawn(7, 0, WHITE), 0, 0, 0, 0, 0, 0, 0]]
        game.setUpCustomGame(testBoard, WHITE)

        game.select(7,0)
        game.select(1,6)
        squaresWithBlackPawns = [game.board.getPawnFromCoords(6, 1),
                                 game.board.getPawnFromCoords(4, 3),
                                 game.board.getPawnFromCoords(2, 5)]

        self.assertEqual(squaresWithBlackPawns, [0, 0, 0])

    def test_shouldChangeInstanceToKingPawn_whenLastRowGetsReached(self):
        game = Game(self.window)
        testBoard = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, JustPawn(1, 4, WHITE), 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [JustPawn(3, 0, BLACK), 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0]]
        game.setUpCustomGame(testBoard, WHITE)

        game.select(1, 4)
        game.select(0, 5)
        pawn = game.board.getPawnFromCoords(0, 5)

        self.assertIsInstance(pawn, KingPawn)

    def test_shouldReturnTrue_whenSkippedWithKingPawnSuccessfully(self):
        game = Game(self.window)
        testBoard = [[0, JustPawn(0, 1, BLACK), 0, 0, 0, 0, 0, 0],
                     [0, 0, JustPawn(1, 2, WHITE), 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, KingPawn(4, 3, WHITE), 0, 0, 0, 0],
                     [0, 0, JustPawn(5, 2, BLACK), 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0]]
        game.setUpCustomGame(testBoard, WHITE)

        game.select(4, 3)
        skip = game.select(6, 1)  # wykonuje bicie "do tyłu", niewykonalne normalnym pionkiem

        self.assertTrue(skip)

    def test_shouldRemovePawnFromBoard_afterSkippingWithKingPawn(self):
        game = Game(self.window)
        testBoard = [[0, JustPawn(0, 1, BLACK), 0, 0, 0, 0, 0, 0],
                     [0, 0, JustPawn(1, 2, WHITE), 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, KingPawn(4, 3, WHITE), 0, 0, 0, 0],
                     [0, 0, JustPawn(5, 2, BLACK), 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0]]
        game.setUpCustomGame(testBoard, WHITE)

        game.select(4, 3)
        skip = game.select(6, 1)  # wykonuje bicie "do tyłu", niewykonalne normalnym pionkiem

        self.assertEqual(game.board.getPawnFromCoords(5, 2), 0)

    def test_shouldReturnTrue_whenBlackWins(self):
        game = Game(self.window)
        testBoard = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, JustPawn(4, 3, BLACK), 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, JustPawn(6, 1, WHITE), 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0]]
        game.setUpCustomGame(testBoard, WHITE)

        game.select(6, 1)
        game.select(5, 2)  # ruszam biały pion do czarnego
        game.select(4, 3)
        game.select(6, 1)  # zbijam czarnym pionem białego i kończę grę

        self.assertIsNotNone(game.returnWinner())

    def test_shouldStartNewGame_afterWinning(self):
        game = Game(self.window)
        testBoard = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, JustPawn(4, 3, BLACK), 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, JustPawn(6, 1, WHITE), 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0]]
        game.setUpCustomGame(testBoard, WHITE)

        game.select(6, 1)
        game.select(5, 2)  # ruszam biały pion do czarnego
        game.select(4, 3)
        game.select(6, 1)  # zbijam czarnym pionem białego i kończę grę
        game.reset()  # resetuje grę, normalnie dzieje się to przez kliknięcie przycisku enter

        self.assertIsNone(game.returnWinner())  # sprawdzam flagę _winner w klasie Game (to ona decyduje o tym,
        # czy gra się dalej toczy, czy pokazuje ekran końcowy)

if __name__ == '__main__':
    unittest.main()