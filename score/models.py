from django.db import models
from team.models import Team
from quiz.models import Round, Attempt, Question, Option


class Score(models.Model):
    score = models.IntegerField(default=0)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)

    def set_rank(self):
        self.rank = [i + 1 for i, x in enumerate(self.round.score_set.all().order_by('score')) if x == self]
        self.save()

    def update_score(self, question_pk, option_pk):
        try:
            question = Question.objects.get(pk=question_pk)
        except Question.DoesNotExist:
            question = None
        try:
            option = Option(pk = option_pk)
        except Option.DoesNotExist:
            option = None
        if question and option:
            if self.round.round is 1:
                category = self.team.category
                # in case of round 1
                if category:
                    if question.category == category and self.round.is_live and not self.round.is_completed:
                        try:
                            attempt = Attempt.objects.get(question=question, team=self.team, is_submitted=True)
                        except Attempt.DoesNotExist:
                            attempt = None
                        if attempt is None:
                            if option.is_right:
                                self.score += 1  # updating the score
                                self.save()
                            attempt = Attempt(team=self.team, question=question, is_submitted=True)
                            attempt.save()
                        return True
            elif self.round.round is 2:
                pass
            elif self.round.round is 3:
                pass

    def __str__(self):
        return self.team.name + " scores " + str(self.score) + " in round"+ str(self.round.round)





