import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .helpers import (
    check_vertical_winner,
    check_diagonal_winner,
    check_horizontal_winner,
)

PLAYER_CHOICES = (
    ("X", "Player X"),
    ("O", "Player O"),
)

MAX_SIDE_LENGTH = 5
MIN_SIDE_LENGTH = 3


# Create your models here.
class Game(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    board_side_length = models.PositiveIntegerField(
        blank=False,
        null=False,
        default=3,
        validators=[
            MaxValueValidator(MAX_SIDE_LENGTH),
            MinValueValidator(MIN_SIDE_LENGTH),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def x_moves_played(self) -> int:
        return Move.objects.filter(game=self, player="X").count()

    @property
    def o_moves_played(self) -> int:
        return Move.objects.filter(game=self, player="O").count()

    @property
    def winner(self) -> str | None:
        game_board: list[list[None | str]] = [
            [None] * self.board_side_length for _ in range(self.board_side_length)
        ]
        game_moves = Move.objects.filter(game=self).all()

        for move in game_moves:
            if (
                move.row <= self.board_side_length
                and move.column <= self.board_side_length
            ):
                game_board[move.row - 1][move.column - 1] = move.player

        return (
            check_horizontal_winner(self.board_side_length, game_board)
            or check_vertical_winner(self.board_side_length, game_board)
            or check_diagonal_winner(self.board_side_length, game_board)
        )

    @property
    def moves(self) -> models.QuerySet:
        return self.moves


class Move(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    game = models.ForeignKey(
        Game, models.DO_NOTHING, blank=False, null=False, related_name="moves"
    )
    player = models.CharField(
        max_length=1, choices=PLAYER_CHOICES, blank=False, null=False
    )
    row = models.SmallIntegerField(
        blank=False,
        null=False,
        validators=[
            MaxValueValidator(MAX_SIDE_LENGTH),
            MinValueValidator(1),
        ],
    )
    column = models.SmallIntegerField(
        blank=False,
        null=False,
        validators=[
            MaxValueValidator(MAX_SIDE_LENGTH),
            MinValueValidator(1),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "moves"
        constraints = [
            models.UniqueConstraint(
                fields=["game", "row", "column"], name="unique_position_for_game"
            )
        ]
