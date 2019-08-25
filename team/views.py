from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout
from .models import Team


def add_team(request):
    if request.user.is_superuser:
        pass


def login_team(request):
    if request.user.is_authenticated:
        return redirect('/quiz/rounds')
    else:
        if request.method == "POST":
            team_name = request.POST.get('team_name', None)
            password = request.POST.get('password', None)
            team_name = str(team_name).lower()
            try:
                team = Team.objects.get(name=team_name, password=password)
            except Team.DoesNotExist:
                team = None
            if team is not None:
                # login with the first user which is the leader of that team
                leader = team.participants.all().first()
                print(team.participants.all())
                user = leader
                login(request, user)
                context = {
                    'msg': 'login_success',
                    'team_name': team.name,
                }
                return redirect('/quiz/rounds')
            else:
                return render(request, 'login.html', {'msg':'err'})

    return render(request, 'login.html')


def logout_team(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
