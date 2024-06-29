from django.urls import path
from . import views

app_name = "Home"
urlpatterns = [
    path("", views.home_view, name="Login"),
    path("match", views.match_view, name="Match"),
    path("logout", views.logout_view, name="Logout"),
    path("palyers", views.players_table, name="PlayerTable"),
    path("rules", views.rule_view, name="Rules"),
    path("groups", views.group_view, name="Groups"),
    path("history", views.history_view, name="History"),
    path("today", views.today_forcast, name="TodayForcast")
]
