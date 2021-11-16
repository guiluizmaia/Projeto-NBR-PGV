from django.urls import path
from NBR.views.gamesView import gamesToday
from NBR.views.indexView import index

from NBR.views.playersView import find, player, playerById
from NBR.views.teamsView import teamFind


urlpatterns = [
    path("", index, name="home"),
    path("team", teamFind),
    path("games", gamesToday),
    path("players", player),
    path("players/<int:player_id>", playerById),
]
