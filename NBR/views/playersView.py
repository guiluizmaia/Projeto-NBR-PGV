import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from NBR.models import players, team, userTeam, user
# import NBR.utils.findPlayer import findPlayer


@login_required(login_url="login")
def player(request):
    userLogged = user.objects.get(loginId=request.user.id)
    userLoggedTeam = userTeam.objects.get(userId=userLogged.id)

    headers = {
        'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
        'x-rapidapi-key': "42db5e1fc2msh9001f8c14520362p122851jsn17206bd81aed"
    }

    if request.method == "POST":
        name = request.POST["name"]
        url = f"https://api-nba-v1.p.rapidapi.com/players/firstName/{name}"
        response = requests.request("GET", url, headers=headers)
        responseJson = response.json()

        if(len(responseJson["api"]["players"]) == 0):
            return render(request, "players.html", context={"message": "jogador não encontrado"})

        context = {"players": []}

        for player in responseJson["api"]["players"]:
            headers = {
                'x-rapidapi-host': "nba-player-individual-stats.p.rapidapi.com",
                'x-rapidapi-key': "42db5e1fc2msh9001f8c14520362p122851jsn17206bd81aed"
            }
            firstName = player["firstName"]
            lastName = player["lastName"]

            url = f"https://nba-player-individual-stats.p.rapidapi.com/players/fullname?name={firstName}_{lastName}"
            response = requests.request("GET", url, headers=headers)
            responseJson = response.json()
            image = ""
            team = ""

            if(responseJson):
                image = responseJson["headShotUrl"]
                team = responseJson["team"]

            sameName = False
            if(userLogged.firstName == player["firstName"]):
                sameName = True
            sameHeight = False
            if(userLogged.height == player["heightInMeters"]):
                sameHeight = True
            sameWeight = False
            if(userLogged.weight == player["weightInKilograms"]):
                sameWeight = True
            base = {
                "playerId": player["playerId"],
                "firstName": player["firstName"],
                "lastName": player["lastName"],
                "country": player["country"],
                "dateOfBirth": player["dateOfBirth"],
                "startNba": player["startNba"],
                "heightInMeters": player["heightInMeters"],
                "weightInKilograms": player["weightInKilograms"],
                "image": image,
                "team": team,
                "sameName": sameName,
                "sameHeight": sameHeight,
                "sameWeight": sameWeight
            }
            context["players"].append(base)

        return render(request, "players.html", context=context)

    else:
        url = f"https://api-nba-v1.p.rapidapi.com/teams/nickName/{userLoggedTeam.teamId.nickName}"

        response = requests.request("GET", url, headers=headers)
        responseJson = response.json()

        teamId = responseJson["api"]["teams"][0]["teamId"]

        url = f"https://api-nba-v1.p.rapidapi.com/players/teamId/{teamId}"
        response = requests.request("GET", url, headers=headers)
        responseJson = response.json()
        context = {"players": []}
        numberBase = 0

        for player in responseJson["api"]["players"]:
            if (numberBase < 5):
                headers = {
                    'x-rapidapi-host': "nba-player-individual-stats.p.rapidapi.com",
                    'x-rapidapi-key': "42db5e1fc2msh9001f8c14520362p122851jsn17206bd81aed"
                }
                firstName = player["firstName"]
                lastName = player["lastName"]

                url = f"https://nba-player-individual-stats.p.rapidapi.com/players/fullname?name={firstName}_{lastName}"
                response = requests.request("GET", url, headers=headers)
                responseJson = response.json()
                image = ""
                team = ""

                if(responseJson):
                    image = responseJson["headShotUrl"]
                    team = responseJson["team"]

                sameName = False
                if(userLogged.firstName == player["firstName"]):
                    sameName = True

                sameHeight = False

                if(userLogged.height == player["heightInMeters"]):
                    sameHeight = True

                sameWeight = False
                if(userLogged.weight == player["weightInKilograms"]):
                    sameWeight = True

                base = {
                    "playerId": player["playerId"],
                    "firstName": player["firstName"],
                    "lastName": player["lastName"],
                    "country": player["country"],
                    "dateOfBirth": player["dateOfBirth"],
                    "startNba": player["startNba"],
                    "heightInMeters": player["heightInMeters"],
                    "weightInKilograms": player["weightInKilograms"],
                    "image": image,
                    "team": team,
                    "sameName": sameName,
                    "sameHeight": sameHeight,
                    "sameWeight": sameWeight
                }
                context["players"].append(base)
                numberBase = numberBase + 1

        return render(request, "players.html", context=context)


def playerById(request, player_id):
    userLogged = user.objects.get(loginId=request.user.id)
    userLoggedTeam = userTeam.objects.get(userId=userLogged.id)

    headers = {
        'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
        'x-rapidapi-key': "42db5e1fc2msh9001f8c14520362p122851jsn17206bd81aed"
    }

    url = f"https://api-nba-v1.p.rapidapi.com/players/playerId/{player_id}"
    response = requests.request("GET", url, headers=headers)
    responseJson = response.json()

    if(len(responseJson["api"]["players"]) == 0):
        return render(request, "player.html", context={"message": "jogador não encontrado"})

    player = responseJson["api"]["players"][0]

    headers = {
        'x-rapidapi-host': "nba-player-individual-stats.p.rapidapi.com",
        'x-rapidapi-key': "42db5e1fc2msh9001f8c14520362p122851jsn17206bd81aed"
    }
    firstName = player["firstName"]
    lastName = player["lastName"]
    url = f"https://nba-player-individual-stats.p.rapidapi.com/players/fullname?name={firstName}_{lastName}"
    response = requests.request("GET", url, headers=headers)
    responseJsonSpecificPlayer = response.json()

    sameName = False
    if(userLogged.firstName == player["firstName"]):
        sameName = True

    sameHeight = False
    if(userLogged.height == player["heightInMeters"]):
        sameHeight = True

    sameWeight = False
    if(userLogged.weight == player["weightInKilograms"]):
        sameWeight = True

    headers = {
        'x-rapidapi-host': "free-nba.p.rapidapi.com",
        'x-rapidapi-key': "42db5e1fc2msh9001f8c14520362p122851jsn17206bd81aed"
    }
    url = f"https://free-nba.p.rapidapi.com/players?page='0'&search={firstName} {lastName}"
    response = requests.request("GET", url, headers=headers)
    responseJson = response.json()

    position = ""

    if(len(responseJson["data"])):
        position = responseJson["data"][0]["position"]

    context = {
        "playerId": player["playerId"],
        "firstName": player["firstName"],
        "lastName": player["lastName"],
        "country": player["country"],
        "dateOfBirth": player["dateOfBirth"],
        "startNba": player["startNba"],
        "heightInMeters": player["heightInMeters"],
        "weightInKilograms": player["weightInKilograms"],
        "image": responseJsonSpecificPlayer["headShotUrl"],
        "team": responseJsonSpecificPlayer["team"],
        "careerPoints": responseJsonSpecificPlayer["careerPoints"],
        "careerBlocks": responseJsonSpecificPlayer["careerBlocks"],
        "carrerAssists": responseJsonSpecificPlayer["carrerAssists"],
        "careerRebounds": responseJsonSpecificPlayer["careerRebounds"],
        "careerTurnovers": responseJsonSpecificPlayer["careerTurnovers"],
        "careerPercentageThree": responseJsonSpecificPlayer["careerPercentageThree"],
        "careerPercentageFreethrow": responseJsonSpecificPlayer["careerPercentageFreethrow"],
        "careerPercentageFieldGoal": responseJsonSpecificPlayer["careerPercentageFieldGoal"],
        "position": position,
        "sameName": sameName,
        "sameHeight": sameHeight,
        "sameWeight": sameWeight
    }
    return render(request, "player.html", context={"player": context})


@login_required(login_url="login")
def find(request):
    print(request.user)
    fName = request.GET.get("firstName")
    lName = request.GET.get("lastName")
    country = request.GET.get("country")
    id = request.GET.get("id")

    type = ""
    param = ""

    if(fName):
        type = "firstName"
        param = fName

    if(lName):
        type = "lastName"
        param = lName

    if(country):
        type = "country"
        param = country

    if(id):
        p = players.objects.get(id=id)
        print(request.user)
        return JsonResponse({"id": p.id})

    find = findPlayer(type, param)
    print(find)
    return find


def findPlayer(type: str, param: str):
    p = None

    if(type == "firstName"):
        p = players.objects.filter(
            firstName=param)

    if(type == "lastName"):
        p = players.objects.filter(
            lastName=param)

    if(type == "country"):
        p = players.objects.filter(
            country=param)

    headers = {
        'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
        'x-rapidapi-key': "42db5e1fc2msh9001f8c14520362p122851jsn17206bd81aed"
    }

    if(not(p) and type):

        url = f"https://api-nba-v1.p.rapidapi.com/players/{type}/{param}"

        response = requests.request("GET", url, headers=headers)
        responseJson = response.json()
        print(responseJson)
        if(len(responseJson["api"]["players"]) > 0):
            for player in responseJson["api"]["players"]:
                teamId = player["teamId"]
                urlTeam = f"https://api-nba-v1.p.rapidapi.com/teams/teamId/{teamId}"
                responseTeamId = requests.request(
                    "GET", urlTeam, headers=headers)
                responseTeamIdJson = responseTeamId.json()
                t = team.objects.filter(
                    nickName=responseTeamIdJson["api"]["teams"][0]["nickname"])
                t = t[0]
                if(not(t)):
                    t = team(
                        fullName=responseTeamIdJson["api"]["teams"][0]["fullName"],
                        nickName=responseTeamIdJson["api"]["teams"][0]["nickname"],
                        image=responseTeamIdJson["api"]["teams"][0]["logo"]
                    )
                    t.save()
                p = players(firstName=player["firstName"],
                            lastName=player["lastName"],
                            height=player["heightInMeters"],
                            weight=player["weightInKilograms"],
                            nationality=player["country"],
                            dateOfBirth=player["dateOfBirth"],
                            teamId=t
                            )
                p.save()
            return responseJson["api"]["players"][0]

    return p[0]
