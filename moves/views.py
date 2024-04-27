import json
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from .models import Game, Move


# Create your views here.
def game(request: HttpRequest, game_id: str = "") -> JsonResponse:
    if request.method == "POST":
        request_data = json.loads(request.body)
        number_of_sides_input = request_data.get("number_of_sides", 3)
        number_of_sides = 3

        try:
            number_of_sides = int(number_of_sides_input)
        except ValueError:
            pass

        game = Game.objects.create(number_of_sides=number_of_sides)
        return JsonResponse(
            {
                "id": game.id,
                "number_of_sides": game.number_of_sides,
                "message": f"Game created with id {game.id} and {game.number_of_sides} sides.",
            },
            status=201,
        )

    elif request.method == "GET":
        if game_id:
            try:
                game = Game.objects.get(pk=game_id)

                return JsonResponse(
                    {
                        "game": game_id,
                        "number_of_sides": game.number_of_sides,
                        "winner": game.winner,
                        "x_moves_played": game.x_moves_played,
                        "o_moves_played": game.o_moves_played,
                    },
                    status=200,
                )
            except ObjectDoesNotExist:
                return JsonResponse(
                    {"message": f"Game with id {game_id} does not exist."}, status=404
                )
        else:
            return JsonResponse(
                {"message": f"There system has {Game.objects.count()} game(s) so far."},
                status=200,
            )

    return JsonResponse(
        {"message": "Only GET and POST requests allowed for this endpoint."}, status=403
    )


def play(request: HttpRequest, game_id: str) -> JsonResponse:
    if request.method == "POST":
        try:
            game = Game.objects.get(pk=game_id)

            request_data = json.loads(request.body)
            player_input = request_data.get("player", "").strip()
            row_input = request_data.get("row", "")
            column_input = request_data.get("column", "")

            column = int(column_input)
            row = int(row_input)

            if row > game.number_of_sides or column > game.number_of_sides:
                return JsonResponse(
                    {
                        "message": f"row and column must not exceed the game's number of sides ({game.number_of_sides})"
                    },
                    status=400,
                )

            winner = game.winner
            if winner:
                return JsonResponse(
                    {"message": f"Game has already been won by player {winner}."},
                    status=400,
                )

            x_moves_played = game.x_moves_played
            o_moves_played = game.o_moves_played

            if x_moves_played > o_moves_played and player_input == "X":
                return JsonResponse(
                    {"message": "It is player O's turn to play"}, status=400
                )
            elif x_moves_played <= o_moves_played and player_input == "O":
                return JsonResponse(
                    {"message": "It is player X's turn to play"}, status=400
                )

            move = Move(game=game, player=player_input, row=row, column=column)
            move.full_clean()
            move.save()

            return JsonResponse(
                {
                    "game": game_id,
                    "player": player_input,
                    "row": row,
                    "column": column,
                    "number_of_sides": game.number_of_sides,
                    "winner": game.winner,
                    "x_moves_played": game.x_moves_played,
                    "o_moves_played": game.o_moves_played,
                    "message": "Move successfully accepted.",
                },
                status=201,
            )

        except ValueError:
            return JsonResponse(
                {
                    "message": "row and column are required and should be valid integers."
                },
                status=400,
            )

        except ValidationError as ve:
            return JsonResponse({"message": ve.message_dict}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse(
                {"message": f"Game with id {game_id} does not exist."}, status=404
            )

    return JsonResponse(
        {"message": "Only POST requests allowed to this endpoint."}, status=400
    )
