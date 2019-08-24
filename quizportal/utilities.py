from quiz.models import *
from score.models import Score
from team.models import Team
from django.contrib.auth.models import User


def reset_quiz():
    rounds = Round.objects.all()
    for r in rounds:
        r.is_live = False
        r.is_completed = False
        r.eligible_teams.set([])
        r.save()
        print(r, "reset")

    attempts = Attempt.objects.all()
    attempts.delete()
    print("all attempts deleted")

    bzrattempts = BzrAttempt.objects.all()
    bzrattempts.delete()
    print("all bzrattempts deleted")

    scores = Score.objects.all()
    scores.delete()
    print("scores deleted")

    teams = Team.objects.all()
    for t in teams:
        t.category = None
        t.save()
        print('team', t, ' category reset')

    phases = Phase.objects.all()
    for p in phases:
        p.is_live = False
        p.save()
        print("phase", p.phase, "reseted")


def add_member_team(team_name, member1, member2, member3):
    m1 = None
    m2 = None
    m3 = None
    if member1 is not None:
        try:
            m1 = User.objects.get(username=member1)
        except User.DoesNotExist:
            m1 = User(username=member1, password='luckyme7')
            m1.save()
    if member2 is not None:
        try:
            m2 = User.objects.get(username=member2)
        except User.DoesNotExist:
            m2 = User(username=member2, password='luckyme7')
            m2.save()
    if member3 is not None:
        try:
            m3 = User.objects.get(username=member3)
        except User.DoesNotExist:
            m3 = User(username=member3, password='luckyme7')
            m3.save()
    if m1 is not None:
        try:
            team = Team.objects.get(name=m1.username)
        except Team.DoesNotExist:
            team = None
        if not team:
            team = Team(name=m1.username, password='luckyme7', team_name=team_name)
            team.save()
            if m1 != '':
                team.participants.add(m1)
                team.save()
            if m2 != '':
                team.participants.add(m2)
                team.save()
            if m3 != '':
                team.participants.add(m3)
                team.save()
            team.save()
            print("Team added", team)
    else:
        print("ERROR: Atleast 1 member required for registration")


team_list = [
    {'team_name': "TEAM 001", "m1": "11804154", "m2": None, "m3": None},
]

def team_import():
    csv_path = "/home/elysian/PycharmProjects/quizportal/quizportal/static/team.csv"
    a = []
    with open(csv_path) as myfile:
        firstline = True
        for line in myfile:
            if firstline:
                mykeys = "".join(line.split()).split(',')
                firstline = False
            else:
                values = "".join(line.split()).split(',')
                a.append({mykeys[n]: values[n] for n in range(0, len(mykeys))})
            for w in a:
                regno = w['reg.no']
                team_name = w['Teamname']
                add_member_team(team_name,regno, w['member1'], w['member2'])


