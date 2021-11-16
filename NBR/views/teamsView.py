from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
import requests
from NBR.models import players, user, userTeam, team
# import NBR.utils.findPlayer import findPlayer


@login_required(login_url="login")
def teamFind(request):
    if request.method == "POST":
        nickName = request.POST["team"]
        t = team.objects.filter(nickName=nickName.capitalize())
        if(len(t) == 0):
            headers = {
                'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
                'x-rapidapi-key': "42db5e1fc2msh9001f8c14520362p122851jsn17206bd81aed"
            }

            url = f"https://api-nba-v1.p.rapidapi.com/teams/nickName/{nickName}"

            response = requests.request("GET", url, headers=headers)
            responseJson = response.json()
            if(len(responseJson["api"]["teams"]) > 0):
                t = team(
                    fullName=responseJson["api"]["teams"][0]["fullName"],
                    nickName=responseJson["api"]["teams"][0]["nickname"],
                    image=responseJson["api"]["teams"][0]["logo"]
                )
                t.save()
                context = {
                    "prefer": False,
                    "teamName": t.nickName,
                    "teamImage": t.image,
                }
                return render(request, "team.html", context=context)
            else:
                return render(request, "team.html", context={"message": "Time não encontrado"})
        else:
            context = {
                "prefer": False,
                "teamName": t[0].nickName,
                "teamImage": t[0].image,
            }

            return render(request, "team.html", context=context)

    else:
        userLogged = user.objects.get(loginId=request.user.id)
        userLoggedTeam = userTeam.objects.get(userId=userLogged.id)

        context = {
            "prefer": True,
            "teamName": userLoggedTeam.teamId.nickName,
            "teamImage": userLoggedTeam.teamId.image,
        }

        return render(request, "team.html", context=context)


@login_required(login_url="login")
def find(request):
    name = request.GET.get("name")
    id = request.GET.get("id")

    if(id):
        t = team.objects.get(id=id)
        print(t)
        return JsonResponse({"id": t.id})

    find = findTeam(type, name)
    print(find)
    return find


@login_required(login_url="login")
def findTeam(type: str, param: str):
    p = None

    if(type == "nickName"):
        p = team.objects.filter(
            nickName=param)

    headers = {
        'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
        'x-rapidapi-key': "42db5e1fc2msh9001f8c14520362p122851jsn17206bd81aed"
    }

    if(not(p) and type):
        url = f"https://api-nba-v1.p.rapidapi.com/teams/{type}/{param}"

        response = requests.request("GET", url, headers=headers)
        responseJson = response.json()
        print(responseJson)
        t = team(
            fullName=responseJson["api"]["teams"][0]["fullName"],
            nickName=responseJson["api"]["teams"][0]["nickname"],
            image=responseJson["api"]["teams"][0]["logo"]
        )
        t.save()

        return responseJson["api"]["teams"][0]

    return p[0]
