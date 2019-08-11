from django.shortcuts import render
from django.http import JsonResponse
from team.models import Team
from quiz.models import Round
from .models import Score


def update_score(request):
    if request.user.is_authenticated:
        team = request.user.team_set.first()

        if request.is_ajax():
            if request.method == "POST":
                question_pk = request.POST.get('question_pk', None)
                answer_pk = request.POST.get('option_pk', None)
                round_pk = int(request.POST.get('round_pk', None))
                print(question_pk, round_pk, answer_pk)
                if question_pk and answer_pk and round_pk:
                    try:
                        round = Round.objects.get(pk=round_pk)
                    except Round.DoesNotExist:
                        round = None
                else:
                    round = None
                if round is not None:
                    if round.is_live:
                        try:
                            score = Score.objects.get(team=team, round=round)
                        except:
                            score = Score(team=team, round=round)
                            score.save()
                        score.update_score(question_pk, answer_pk)
                        return JsonResponse({'msg': 'success'})
                    return JsonResponse({'msg': 'This round is not live now'})
        return JsonResponse({'msg': 'err'})
