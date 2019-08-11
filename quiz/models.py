from django.db import models
from team.models import Team
from django.db.models import Q


from team.models import Category


class Round(models.Model):
    round = models.IntegerField(default=0)
    eligible_teams = models.ManyToManyField(Team, blank=True)
    is_live = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def get_scores(self):
        return self.score_set.all()


    def fill_up_eligible_teams(self):
        """
        after completing the quiz
        based on rank

        take 100% in case of round 1
        take 40 % in case of round 2
        take top 6 teams in case of round 3
        :return:
        """

        pass

    def get_question_set(self, team):
        if self.round is 1:
            attempts = Attempt.objects.filter(team=team)
            a_list = []
            for a in attempts:
                a_list.append(a.question.pk)
            a_list = set(a_list)
            questions = self.question_set.filter(Q(category=team.category) & ~Q(pk__in = a_list))[:40]


            # todo shuffle it
            print(questions)
            return questions
        elif self.round == 2:
            questions = self.question_set.all()[:30]
            return questions
        elif self.round == 3:
            # return one question
            pass



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
        (1,TYPE_TEXT),
        (2,TYPE_VIDEO),
        (3,TYPE_IMAGE),
        (4,TYPE_AUDIO)
    )
    title = models.CharField(max_length=500)
    type = models.IntegerField(choices=TYPE_CHOICES, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)

    def get_options(self):
        return self.option_set.all()

    def get_right_answer(self):
        return self.option_set.filter(is_right=True)[:1]

    def __str__(self):
        return self.title[:30]


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


"""
CALCULATE RANK BUTTON ON QUIZMASTER
START ROUND BUTTON ON QUIZMASTER
"""