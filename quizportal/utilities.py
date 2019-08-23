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
            if m1 is not None:
                team.participants.add(m1)
                team.save()
            if m2 is not None:
                team.participants.add(m2)
                team.save()
            if m3 is not None:
                team.participants.add(m3)
                team.save()
            team.save()
            print("Team added", team)
    else:
        print("ERROR: Atleast 1 member required for registration")


team_list = [
    {'team_name': "TEAM 001", "m1": "11804154", "m2": None, "m3": None},
    {'team_name': "TEAM 002", "m1": "11903561", "m2": None, "m3": None},
    {'team_name': "TEAM 003", "m1": "11905234", "m2": None, "m3": None},
    {'team_name': "TEAM 004", "m1": "11903371", "m2": None, "m3": None},
    {'team_name': "TEAM 005", "m1": "11902048", "m2": None, "m3": None},
    {'team_name': "TEAM 006", "m1": "11701143", "m2": None, "m3": None},
    {'team_name': "TEAM 007", "m1": "11702014", "m2": None, "m3": None},
    {'team_name': "TEAM 008", "m1": "11705122", "m2": None, "m3": None},
    {'team_name': "TEAM 009", "m1": "11705116", "m2": None, "m3": None},
    {'team_name': "TEAM 0010", "m1": "11702291", "m2": None, "m3": None},
    {'team_name': "TEAM 0011", "m1": "11707031", "m2": None, "m3": None},
    {'team_name': "TEAM 0012", "m1": "11701703", "m2": None, "m3": None},
    {'team_name': "TEAM 0013", "m1": "11701184", "m2": None, "m3": None},
    {'team_name': "TEAM 0014", "m1": "11900328", "m2": None, "m3": None},
    {'team_name': "TEAM 0015", "m1": "11701286", "m2": None, "m3": None},
    {'team_name': "TEAM 0016", "m1": "11814248", "m2": None, "m3": None},
    {'team_name': "TEAM 0017", "m1": "11903093", "m2": None, "m3": None},
    {'team_name': "TEAM 0018", "m1": "11904644", "m2": None, "m3": None},
    {'team_name': "TEAM 0019", "m1": "11903962", "m2": None, "m3": None},
    {'team_name': "TEAM 0020", "m1": "11903970", "m2": None, "m3": None},
    {'team_name': "TEAM 0021", "m1": "11715629", "m2": None, "m3": None},
    {'team_name': "TEAM 0022", "m1": "11701462", "m2": None, "m3": None},
    {'team_name': "TEAM 0023", "m1": "11810174", "m2": None, "m3": None},
    {'team_name': "TEAM 0024", "m1": "11708846", "m2": None, "m3": None},
    {'team_name': "TEAM 0025", "m1": "11903169", "m2": None, "m3": None},
    {'team_name': "TEAM 0026", "m1": "11904790", "m2": None, "m3": None},
    {'team_name': "TEAM 0027", "m1": "11708027", "m2": None, "m3": None},
    {'team_name': "TEAM 0028", "m1": "11702152", "m2": None, "m3": None},
    {'team_name': "TEAM 0029", "m1": "11701196", "m2": None, "m3": None},
    {'team_name': "TEAM 0030", "m1": "11701588", "m2": None, "m3": None},
    {'team_name': "TEAM 0031", "m1": "11709953", "m2": None, "m3": None},
    {'team_name': "TEAM 0032", "m1": "11709773", "m2": None, "m3": None},
    {'team_name': "TEAM 0033", "m1": "11701731", "m2": None, "m3": None},
    {'team_name': "TEAM 0034", "m1": "11903488", "m2": None, "m3": None},
    {'team_name': "TEAM 0035", "m1": "11702138", "m2": None, "m3": None},
    {'team_name': "TEAM 0036", "m1": "11915809", "m2": None, "m3": None},
    {'team_name': "TEAM 0037", "m1": "11918128", "m2": None, "m3": None},
    {'team_name': "TEAM 0038", "m1": "11713325", "m2": None, "m3": None},
    {'team_name': "TEAM 0039", "m1": "11804841", "m2": None, "m3": None},
    {'team_name': "TEAM 0040", "m1": "11803638", "m2": None, "m3": None},
    {'team_name': "TEAM 0041", "m1": "11804832", "m2": None, "m3": None},
    {'team_name': "TEAM 0042", "m1": "11711837", "m2": None, "m3": None},
    {'team_name': "TEAM 0043", "m1": "11715820", "m2": None, "m3": None},
    {'team_name': "TEAM 0044", "m1": "11904931", "m2": None, "m3": None},
    {'team_name': "TEAM 0045", "m1": "11904577", "m2": None, "m3": None},
    {'team_name': "TEAM 0046", "m1": "11904972", "m2": None, "m3": None},
    {'team_name': "TEAM 0047", "m1": "11906014", "m2": None, "m3": None},
    {'team_name': "TEAM 0048", "m1": "11913341", "m2": None, "m3": None},
    {'team_name': "TEAM 0049", "m1": "11912543", "m2": None, "m3": None},
    {'team_name': "TEAM 0050", "m1": "11810184", "m2": None, "m3": None},
    {'team_name': "TEAM 0051", "m1": "11806686", "m2": None, "m3": None},
]
