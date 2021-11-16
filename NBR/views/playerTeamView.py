from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from NBR.models import userTeam


@login_required(login_url="login")
def post(request):
    if request.method == "POST":
        userId = request.POST["userId"]
        teamId = request.POST["teamId"]

        uT = userTeam(userId, teamId)
        uT.save()
        return uT
