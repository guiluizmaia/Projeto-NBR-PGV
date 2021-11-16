from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UsernameField
from django.shortcuts import render
from NBR.models import userTeam, user
from django.contrib.auth.models import User


@login_required(login_url="login")
def index(request):
    userLogged = user.objects.get(loginId=request.user.id)
    userLoggedTeam = userTeam.objects.get(userId=userLogged.id)

    context = {
        "teamName": userLoggedTeam.teamId.nickName,
        "teamImage": userLoggedTeam.teamId.image,
        "userFirstName": userLogged.firstName,
        "userLastName": userLogged.lastName,
        "userHeight": userLogged.height,
        "userWeight": userLogged.weight,
        "userNationality": userLogged.nationality,
        "userDateOfBirth": userLogged.dateOfBirth,
        "userAddresseeCity": userLogged.addresseeCity
    }

    return render(request, "index.html", context=context)
