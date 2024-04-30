from rest_framework.routers import DefaultRouter

from moves.views import GameViewSet

router = DefaultRouter()

router.register(r"games", GameViewSet, basename="game")

urlpatterns = router.urls
