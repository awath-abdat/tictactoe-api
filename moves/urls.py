from django.urls import path
from .views import game, play

urlpatterns = [
    path("games/", game),
    path("games/<uuid:game_id>/", game),
    path("play/<uuid:game_id>/", play),
]
