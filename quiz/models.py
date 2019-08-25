from django.db import models
from team.models import Team
import math
from django.db.models import Q

from team.models import Category


class Round(models.Model):
    round = models.IntegerField(default=0)
    eligible_teams = models.ManyToManyField(Team, blank=True)
    is_live = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='images/', blank=True)

    def get_scores(self):
        return self.score_set.all().order_by("-score", "pk")

    def fill_up_eligible_teams(self):
        scores = self.score_set.all()
        print(scores)
        for s in scores:
            s.set_rank()
            print(s.rank)
        if self.round is 1:
            teams = Team.objects.all()
            for t in teams:
                self.eligible_teams.add(t)
            self.save()
        elif self.round is 2:
            # todo short on the basis of rank
            print('lets fill eligibility for 2nd round')
            round_1_score = Round.objects.get(round=1).score_set.all().order_by('score')
            num_eligibles = math.floor((round_1_score.count() / 100) * 40)
            eligible_teams = round_1_score[:num_eligibles]
            for e in eligible_teams:
                self.eligible_teams.add(e.team)
                self.save()
        elif self.round is 3:
            print("lets fill the eligibility for 3rd round")
            round_2_score = Round.objects.get(round=2).score_set.all().order_by('score')
            eligible_teams = round_2_score[:6]
            for e in eligible_teams:
                self.eligible_teams.add(e.team)
                self.save()
        pass

    def get_question_set(self, team):
        if self.round is 1:
            attempts = Attempt.objects.filter(team=team, round=self)
            print(attempts)
            a_list = []
            for a in attempts:
                a_list.append(a.question.pk)
            a_list = set(a_list)
            num_attemts = len(a_list)

            if (40 - num_attemts) > 0:
                print(team.category)
                questions = self.question_set.filter(~Q(pk__in=a_list) & Q(category=team.category))[:(40 - num_attemts)]
                print(questions)
            else:
                questions = []
            return questions
        elif self.round == 2:
            attempts = Attempt.objects.filter(team=team, round=self)
            a_list = []
            for a in attempts:
                a_list.append(a.question.pk)
            a_list = set(a_list)
            num_attemts = len(a_list)
            if (5 - num_attemts) > 0:
                questions = self.question_set.filter(~Q(pk__in=a_list))[:(5 - num_attemts)]
            else:
                questions = []
            return questions

        elif self.round == 3:
            if (Phase.objects.get(phase=2).is_live):
                attempts = Attempt.objects.filter(team=team, round=self)
                a_list = []
                for a in attempts:
                    a_list.append(a.question.pk)
                a_list = set(a_list)
                num_attemts = len(a_list)

                print(attempts)
                if (10 - num_attemts) > 0:
                    question = self.question_set.filter(~Q(pk__in=a_list))[:(10 - num_attemts)]
                    if len(question) > 0:
                        question = question[0]
                    else:
                        question = None
                else:
                    question = None
                return question
            return []

    def __str__(self):
        if self.round == 1:
            return "Round 1"
        elif self.round == 2:
            return "Round 2"
        elif self.round == 3:
            return "Round 3"
        else:
            return "xxx"


class Question(models.Model):
    TYPE_TEXT = 'Text'
    TYPE_VIDEO = 'Video'
    TYPE_IMAGE = 'Image'
    TYPE_AUDIO = 'Audio'
    TYPE_CHOICES = (
        (1, TYPE_TEXT),
        (2, TYPE_VIDEO),
        (3, TYPE_IMAGE),
        (4, TYPE_AUDIO)
    )
    title = models.CharField(max_length=500)
    type = models.IntegerField(choices=TYPE_CHOICES, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/', blank=True, null=True)

    def get_options(self):
        return self.option_set.all()

    def get_right_answer(self):
        return self.option_set.filter(is_right=True)[:1]

    def __str__(self):
        return self.title[:30]

    def get_file_url(self):
        if self.file:
            return self.file.url
        else:
            return False


class Option(models.Model):
    title = models.CharField(max_length=64)
    is_right = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Attempt(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    is_submitted = models.BooleanField(default=False)
    round = models.ForeignKey(Round, blank=True, null=True, on_delete=models.CASCADE)


class BzrAttempt(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    is_submitted = models.BooleanField(default=False)
    round = models.ForeignKey(Round, blank=True, null=True, on_delete=models.CASCADE)

    def set_team(self, team):
        if self.team is None:
            self.team = team


class Phase(models.Model):
    phase = models.IntegerField()
    is_live = models.BooleanField(default=False)


"""
CALCULATE RANK BUTTON ON QUIZMASTER
START ROUND BUTTON ON QUIZMASTER
"""
