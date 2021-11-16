from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from NBR.models import team, user, userTeam
import requests


def newUser(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        newUser = User(username=username, email=email)
        newUser.set_password(password)
        newUser.save()

        return render(request, "users/login.html")
    else:
        return render(request, "users/newUser.html")


@login_required(login_url="login")
def post(request):
    if (request.method == "POST"):
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        height = request.POST["height"]
        weight = request.POST["weight"]
        nationality = request.POST["nationality"]
        addresseeCity = request.POST["addresseeCity"]

        u = user.objects.filter(loginId=request.user.id)

        if (len(u) == 0):
            dateOfBirth = request.POST["dateOfBirth"]

            u = user(firstName=firstName, lastName=lastName, height=height, weight=weight,
                     nationality=nationality, dateOfBirth=dateOfBirth, addresseeCity=addresseeCity, loginId=request.user.id)
            u.save()
        else:
            u[0].firstName = firstName
            u[0].lastName = lastName
            u[0].height = height
            u[0].weight = weight
            u[0].nationality = nationality
            u[0].addresseeCity = addresseeCity

            u[0].save()

        return render(request, "users/preferTeam.html")
    else:
        u = user.objects.filter(loginId=request.user.id)
        context = {}
        if (len(u) > 0):
            context = {
                "firstName": u[0].firstName,
                "lastName": u[0].lastName,
                "height": u[0].height,
                "weight": u[0].weight,
                "addresseeCity": u[0].addresseeCity,
                "nationality": u[0].nationality,
                "disabled": "disabled"
            }
        return render(request, "users/cadastro.html", context)


@login_required(login_url="login")
def teamFind(request):
    userLogged = user.objects.filter(loginId=request.user.id)

    if(not(userLogged)):
        return render(request, "users/cadastro.html")
    else:
        if request.method == "POST":
            name = request.POST["team"]

            t = team.objects.filter(
                nickName=name.capitalize())

            headers = {
                'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
                'x-rapidapi-key': "42db5e1fc2msh9001f8c14520362p122851jsn17206bd81aed"
            }
            if(len(t) == 0):
                url = f"https://api-nba-v1.p.rapidapi.com/teams/nickName/{name}"

                response = requests.request("GET", url, headers=headers)
                responseJson = response.json()
                if(len(responseJson["api"]["teams"]) > 0):
                    t = team(
                        fullName=responseJson["api"]["teams"][0]["fullName"],
                        nickName=responseJson["api"]["teams"][0]["nickname"],
                        image=responseJson["api"]["teams"][0]["logo"]
                    )
                    t.save()

                    ut = userTeam.objects.filter(userId=userLogged[0])

                    if(len(ut) == 0):
                        ut = userTeam(userId=userLogged[0], teamId=t)
                        ut.save()
                    else:
                        ut[0].teamId = t

                        ut[0].save()

                    return HttpResponseRedirect(reverse("NBR:home"))

                else:
                    return render(request, "users/preferTeam.html", {
                        "message": "Time não encontrado.",
                    })
            else:
                ut = userTeam.objects.filter(userId=userLogged[0])

                if(len(ut) == 0):
                    ut = userTeam(userId=userLogged[0], teamId=t[0])
                    ut.save()
                else:
                    ut[0].teamId = t[0]
                    ut[0].save()
                return HttpResponseRedirect(reverse("NBR:home"))
        else:
            return render(request, "users/preferTeam.html")
