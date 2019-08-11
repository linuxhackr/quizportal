from django.shortcuts import render, redirect
from .models import Round, Category, Question, Attempt
from .models import Team
from django.http import JsonResponse


def categories(request):
    if request.user.is_authenticated:
        team = request.user.team_set.first()
        if team.category:
            return redirect('/quiz/rounds')
        categories = Category.objects.all()
        return render(request, 'categories.html', {'categories':categories,'team':team})


def rounds(request):
    if request.user.is_authenticated:
        rounds = Round.objects.all()
        team = request.user.team_set.first()
        if not team.category:
            return redirect('/quiz/categories')
        return render(request, 'rounds.html', {'rounds':rounds,'team':team})


def set_category(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            if request.method == "POST":
                category_pk = request.POST.get('category_pk', None)
                if category_pk:
                    try:
                        category = Category.objects.get(pk=category_pk)
                    except Category.DoesNotExist:
                        category = None
                    if category:
                        team = request.user.team_set.first()
                        team.category = category
                        team.save()
                        return JsonResponse({'msg':'success'})

def round(request, round_pk):
    if request.user.is_authenticated:
        team = request.user.team_set.first()
        try:
            round = Round.objects.get(pk=round_pk)
        except Round.DoesNotExist:
            round = None

        if round is not None:
            if round.round is 1:
                if not round.is_completed and round.is_live:
                    # check eligible 100%
                    if request.is_ajax():
                        query_questions = round.get_question_set(team)

                        questions = []
                        for q in query_questions:
                            options = []
                            for o in q.get_options():
                                options.append(
                                    {
                                        'title': o.title,
                                        'is_right': o.is_right,
                                        'pk': o.pk,
                                    }
                                )
                            questions.append(
                                {
                                    'title': q.title,
                                    'options': options,
                                    'pk': q.pk,
                                }
                            )
                        return JsonResponse({'questions': questions})
                    else:
                        return render(request, 'round.html', {'round':round, 'team':team})
        # elif round.round == 2:
            #     if Round.objects.get(round=1).is_completed:
            #         if not round.is_completed:
            #             pass
            #     pass
            # elif round.round == 3:
            #     if Round.objects.get(round=1).is_completed and Round.objects.get(round=2).is_completed:
            #         if not round.is_completed:
            #             pass
        return redirect('/quiz/rounds')

def score(request, round_pk):
    if request.user.is_authenticated:
        try:
            round = Round.objects.get(pk=round_pk)
        except Round.DoesNotExist:
            round = None
        if round:
            score = round.score_set.all()
            team = request.user.team_set.first()
            myscore = round.score_set.filter(team=team).first()
            return render(request, 'score.html', {'score':score, 'my_score':myscore})
    return redirect('/')


def attempt_question(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            team = request.user.team_set.first()
            question_pk = request.POST.get('question_pk', None)
            if question_pk:
                try:
                    question = Question.objects.get(pk=question_pk)
                except Question.DoesNotExist:
                    question = None
                if question:
                    attempt = Attempt(team=team, question=question)
                    attempt.save()
                    print('attempt save')
                    return JsonResponse({'msg':'success'})

