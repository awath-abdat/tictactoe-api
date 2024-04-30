from typing import Any
from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    ValidationError,
)

from moves.models import Game, Move


# Serilaizers for the api
class GameListSerializer(ModelSerializer):

    class Meta:
        model = Game
        fields = ("id", "board_side_length", "created_at")


class GameMoveSerializer(ModelSerializer):

    class Meta:
        model = Move
        fields = ("id", "player", "row", "column", "created_at")


class GameDetailSerializer(ModelSerializer):
    winner = CharField(read_only=True)
    x_moves_played = IntegerField(read_only=True)
    y_moves_played = IntegerField(read_only=True)
    moves = GameMoveSerializer(read_only=True, many=True)

    class Meta:
        model = Game
        fields = "__all__"


class GameStatisticsSerializer(ModelSerializer):
    winner = CharField(read_only=True)
    x_moves_played = IntegerField(read_only=True)
    o_moves_played = IntegerField(read_only=True)

    class Meta:
        model = Game
        fields = "__all__"


class NewMoveSerializer(ModelSerializer):
    game_statistics = GameStatisticsSerializer(source="game", read_only=True)

    def validate(self, attrs) -> dict[str, Any]:
        validated_model_data = super().validate(attrs)

        game: Game = validated_model_data["game"]
        if validated_model_data["row"] > game.board_side_length:
            raise ValidationError(
                {
                    "row": f"This value cannot be greater than the board side length ({game.board_side_length})"
                }
            )

        if validated_model_data["row"] > game.board_side_length:
            raise ValidationError(
                {
                    "column": f"This value cannot be greater than the board side length ({game.board_side_length})"
                }
            )

        player = validated_model_data["player"]
        winner = game.winner
        if winner:
            raise ValidationError(
                {"game": f"Game has already been won by player {winner}."}
            )

        x_moves_played = game.x_moves_played
        o_moves_played = game.o_moves_played

        if x_moves_played > o_moves_played and player == "X":
            raise ValidationError({"player": "It is player O's turn to play"})
        elif x_moves_played <= o_moves_played and player == "O":
            raise ValidationError({"player": "It is player X's turn to play"})

        return validated_model_data

    class Meta:
        model = Move
        fields = "__all__"
