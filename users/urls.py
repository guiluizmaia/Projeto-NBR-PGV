from django.urls import path

from users.views import authenticateView, userView

urlpatterns = [
    path("", authenticateView.index, name="index"),
    path("new", userView.newUser, name="new"),
    path("login", authenticateView.login_view, name="login"),
    path("logout", authenticateView.logout_view, name="logout"),
    path("cad", userView.post, name="cad"),
    path("team", userView.teamFind, name="team")
]
