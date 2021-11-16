from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from NBR.models import user


@login_required(login_url="login")
def index(request):
    userLogged = user.objects.filter(loginId=request.user.id)

    if(not(userLogged)):
        return render(request, "users/cadastro.html")
    else:
        return HttpResponseRedirect(reverse("NBR:home"))


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {
                "message": "Credenciais erradas."
            })
    else:
        return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "Deslogado"
    })
