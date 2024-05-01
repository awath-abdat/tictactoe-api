from django.test import TestCase

from moves.helpers import (
    check_diagonal_winner,
    check_horizontal_winner,
    check_vertical_winner,
)


# Create your tests here.
class WinnerTestCase(TestCase):
    def test_check_horizontal_winner(self):
        game_board = [
            ["O", "X", None],
            ["X", "X", "X"],
            ["O", None, None],
        ]
        self.assertEqual(check_horizontal_winner(len(game_board), game_board), "X")

    def test_check_vertical_winner(self):
        game_board = [
            ["O", "X", None],
            ["X", "X", "O"],
            ["O", "X", None],
        ]
        self.assertEqual(check_vertical_winner(len(game_board), game_board), "X")

    def test_check_major_diagonal_winner_on_three_by_three(self):
        game_board = [
            ["O", "X", "X"],
            ["X", "O", "O"],
            ["X", None, "O"],
        ]
        self.assertEqual(check_diagonal_winner(len(game_board), game_board), "O")

    def test_check_minor_diagonal_winner_on_three_by_three(self):
        game_board = [
            ["O", "X", "X"],
            ["X", "X", "O"],
            ["X", None, None],
        ]
        self.assertEqual(check_diagonal_winner(len(game_board), game_board), "X")

    def test_check_major_diagonal_winner_on_four_by_four(self):
        game_board = [
            ["X", "X", "X", "O"],
            ["X", "X", "O", "X"],
            ["X", None, "X", None],
            ["O", None, None, "X"],
        ]
        self.assertEqual(check_diagonal_winner(len(game_board), game_board), "X")

    def test_check_minor_diagonal_winner_on_four_by_four(self):
        game_board = [
            ["O", "X", "X", "O"],
            ["X", "X", "O", "X"],
            ["X", "O", "X", None],
            ["O", None, None, "X"],
        ]
        self.assertEqual(check_diagonal_winner(len(game_board), game_board), "O")

    def test_check_major_diagonal_winner_on_five_by_five(self):
        game_board = [
            ["X", "X", "X", "O", None],
            ["X", "X", "O", "X", "O"],
            ["X", None, "X", None, None],
            ["O", None, None, "X", None],
            ["O", None, None, "X", "X"],
        ]
        self.assertEqual(check_diagonal_winner(len(game_board), game_board), "X")

    def test_check_minor_diagonal_winner_on_five_by_five(self):
        game_board = [
            ["X", "X", "X", "O", "O"],
            ["X", "X", "O", "O", "O"],
            ["X", None, "O", None, None],
            ["O", "O", None, "X", None],
            ["O", None, None, "X", "X"],
        ]
        self.assertEqual(check_diagonal_winner(len(game_board), game_board), "O")
