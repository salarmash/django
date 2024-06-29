import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib import messages

from .models import Match, MatchDay, Score, User, UserForcast, Rule, UserForcastHistory
from datetime import date, time


def home_view(request):
    time = datetime.datetime.now()
    if request.user.is_authenticated:
        return redirect("Home:Match")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "با موفقیت وارد شدید")
            return redirect("Home:Match")
        else:
            messages.error(request, "ایمیل یا پسورد اشتباه است")
    return render(request, "HomeApp/login.html", context={"time": time})


def match_view(request):
    today = date.today()
    two_am = time(hour=2)
    matches = Match.objects.filter(matchday__date__day=today.day)
    if matches:
        user_forecasts_exist = UserForcast.objects.filter(user=request.user,
                                                          matchday__date__day=today.day).exists()
        matching_day = MatchDay.objects.filter(date__day=today.day).first()
        if matching_day:
            first_match_start = matching_day.first_match_start

        submission_time = timezone.now().time()
        if request.method == "POST" and not user_forecasts_exist:
            for match in matches:
                matchday = match.matchday
                user = request.user
                home_name = match.home_name
                away_name = match.away_name
                home = request.POST.get(f'home-{match.id}')
                away = request.POST.get(f'away-{match.id}')
                home_img = match.home_img
                away_img = match.away_img
                UserForcast.objects.create(user=user, home_name=home_name, away_name=away_name, matchday=matchday,
                                           home=home,
                                           away=away, home_img=home_img, away_img=away_img, match=match)
                messages.success(request, "پیش بینی شما ثبت شد")

            return redirect("Home:Logout")
        return render(request, "HomeApp/Match.html",
                      context={"matches": matches, "user_forecasts_exist": user_forecasts_exist,
                               "first_match_start": first_match_start, "two_am": two_am,
                               "submission_time": submission_time})
    else:
        return render(request, "HomeApp/Nomatch.html")


def logout_view(request):
    logout(request)
    return redirect("/")


def players_table(request):
    users = User.objects.filter(forcast__isnull=False).distinct()
    scores = Score.objects.all().order_by("-score")
    for user in users:
        forcasts = UserForcast.objects.filter(user=user)
        score, created = Score.objects.get_or_create(user=user, defaults={'score': 0})
        for forcast in forcasts:
            if forcast.match.home is not None and forcast.match.away is not None:
                final_home = int(forcast.match.home)
                final_away = int(forcast.match.away)
                user_home = int(forcast.home)
                user_away = int(forcast.away)
                final_score = f"{forcast.match.home}{forcast.match.away}"
                final_score = int(final_score)
                user_score = f"{forcast.home}{forcast.away}"
                user_score = int(user_score)
                # checking for Group Stage

                if forcast.matchday.group:
                    if final_score == user_score:
                        score.score += 10
                        score.save()
                    elif (abs(final_home - final_away) == abs(user_home - user_away)) and (
                            user_home != final_home) and (
                            user_away != final_away) and (
                            (user_home > user_away and final_home > final_away) or (
                            user_away > user_home and final_away > final_home)):
                        score.score += 7
                        score.save()
                    elif (abs(final_home - final_away) != abs(user_home - user_away)) and (
                            (user_home > user_away and final_home > final_away) or (
                            user_away > user_home and final_away > final_home)):
                        score.score += 5
                        score.save()
                    elif (user_away == user_home) and (final_away == final_home) and (user_away != final_away):
                        score.score += 7
                        score.save()
                    else:
                        score.score += 2
                        score.save()
                #         Checking For Knockout Stage

                elif forcast.matchday.knockout:
                    if final_score == user_score:
                        score.score += (10 * 3)
                        score.save()
                    elif (abs(final_home - final_away) == abs(user_home - user_away)) and (
                            user_home != final_home) and (
                            user_away != final_away) and (
                            (user_home > user_away and final_home > final_away) or (
                            user_away > user_home and final_away > final_home)):
                        score.score += (7 * 3)
                    elif (abs(final_home - final_away) != abs(user_home - user_away)) and (
                            (user_home > user_away and final_home > final_away) or (
                            user_away > user_home and final_away > final_home)):
                        score.score += (5 * 3)
                        score.save()
                    elif (user_away == user_home) and (final_away == final_home) and (user_away != final_away):
                        score.score += (7 * 3)
                        score.save()
                    else:
                        score.score += (2 * 3)
                        score.save()
                #         Checking for Semi-Final

                elif forcast.matchday.semiFinal:
                    if final_score == user_score:
                        score.score += (10 * 4)
                        score.save()
                    elif (abs(final_home - final_away) == abs(user_home - user_away)) and (
                            user_home != final_home) and (
                            user_away != final_away) and (
                            (user_home > user_away and final_home > final_away) or (
                            user_away > user_home and final_away > final_home)):
                        score.score += (7 * 4)
                    elif (abs(final_home - final_away) != abs(user_home - user_away)) and (
                            (user_home > user_away and final_home > final_away) or (
                            user_away > user_home and final_away > final_home)):
                        score.score += (5 * 4)
                        score.save()
                    elif (user_away == user_home) and (final_away == final_home) and (user_away != final_away):
                        score.score += (7 * 4)
                        score.save()
                    else:
                        score.score += (2 * 4)
                        score.save()
                #     Checking For Final Stage

                elif forcast.matchday.final:
                    if final_score == user_score:
                        score.score += (10 * 6)
                        score.save()
                    elif (abs(final_home - final_away) == abs(user_home - user_away)) and (
                            user_home != final_home) and (
                            user_away != final_away) and (
                            (user_home > user_away and final_home > final_away) or (
                            user_away > user_home and final_away > final_home)):
                        score.score += (7 * 6)
                        score.save()
                    elif (abs(final_home - final_away) != abs(user_home - user_away)) and (
                            (user_home > user_away and final_home > final_away) or (
                            user_away > user_home and final_away > final_home)):
                        score.score += (5 * 6)
                        score.save()
                    elif (user_away == user_home) and (final_away == final_home) and (user_away != final_away):
                        score.score += (7 * 6)
                        score.save()
                    else:
                        score.score += (2 * 6)
                        score.save()
                else:
                    print("ridi")
                UserForcastHistory.objects.create(user=forcast.user, away_name=forcast.away_name,
                                                  home_name=forcast.home_name, home=forcast.home, away=forcast.away,
                                                  home_img=forcast.home_img, away_img=forcast.away_img,
                                                  matchday=forcast.matchday, match=forcast.match)
                forcast.delete()
    return render(request, "HomeApp/scores.html", context={"users": users, "scores": scores})


def rule_view(request):
    rule = Rule.objects.all().last()
    return render(request, "HomeApp/rules.html", context={"rule": rule})


def group_view(request):
    return render(request, "HomeApp/groups.html")


def history_view(request):
    history = UserForcastHistory.objects.filter(user=request.user)
    return render(request, "HomeApp/history.html", context={"items": history})


def today_forcast(request):
    today = date.today()
    matches = Match.objects.filter(matchday__date__day=today.day)
    if matches:
        matching_day = MatchDay.objects.filter(date__day=today.day).first()
        if matching_day:
            first_match_start = matching_day.first_match_start
            submission_time = timezone.now().time()
            forcast = UserForcast.objects.all()
    else:
        return render(request, "HomeApp/Nomatch.html")
    return render(request, "HomeApp/today.html", context={"items": forcast, "first_match_start": first_match_start,
                                                          "submission_time": submission_time})
