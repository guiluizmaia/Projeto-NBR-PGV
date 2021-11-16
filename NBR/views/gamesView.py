from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
import requests
from NBR.models import players, user, userTeam, team
import datetime
# import NBR.utils.findPlayer import findPlayer


@login_required(login_url="login")
def gamesToday(request):
    headers = {
        'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
        'x-rapidapi-key': "42db5e1fc2msh9001f8c14520362p122851jsn17206bd81aed"
    }

    date = str(datetime.datetime.now())
    date = date[0:10]

    url = f"https://api-nba-v1.p.rapidapi.com/games/date/{date}"

    response = requests.request("GET", url, headers=headers)
    responseJson = response.json()

    return render(request, "gamesToday.html", context={"games": responseJson["api"]["games"]})
