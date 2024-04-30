from django.http.response import JsonResponse
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from moves.models import Game
from moves.serializers import (
    GameDetailSerializer,
    GameListSerializer,
    NewMoveSerializer,
)


# Create your views here.
class GameViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameDetailSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == "list":
            return GameListSerializer

        return super().get_serializer_class()

    @action(
        detail=True,
        methods=["post"],
    )
    def play(self, request: Request, pk=None) -> JsonResponse:
        request.data.update({"game": pk})
        serializer = NewMoveSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse(
            serializer.data,
            status=201,
        )
