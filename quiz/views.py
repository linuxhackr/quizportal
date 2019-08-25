from django.shortcuts import render, redirect
from .models import Round, Category, Question, Attempt, BzrAttempt, Phase
from .models import Team
from django.db.models import Q
from django.http import JsonResponse


def categories(request):
    if request.user.is_authenticated:
        team = request.user.team_set.first()
        team.category = None
        team.save()
        if team.category:
            return redirect('/quiz/rounds')
        categories = Category.objects.all()
        return render(request, 'categories.html', {'categories': categories, 'team': team})


def rounds(request):
    if request.user.is_authenticated:
        rounds = Round.objects.all()
        team = request.user.team_set.first()
        if not team.category:
            return redirect('/quiz/categories')
        return render(request, 'rounds.html', {'rounds': rounds, 'team': team})


def set_category(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            if request.method == "POST":
                category_pk = request.POST.get('category_pk', None)
                if category_pk:
                    try:
                        category = Category.objects.get(id=category_pk)
                    except Category.DoesNotExist:
                        category = None
                    if category:
                        team = request.user.team_set.first()
                        team.category = category
                        team.save()
                        return JsonResponse({'msg': 'success'})


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
                    elif round.is_completed:
                        return redirect('score')
                    else:
                        return render(request, 'round.html', {'team': team, 'round': round})
            elif round.round is 2:
                if team in round.eligible_teams.all():
                    if not round.is_completed and round.is_live:
                        if team in round.eligible_teams.all():
                            if request.is_ajax():
                                query_questions = round.get_question_set(team)
                                questions = []
                                for q in query_questions:
                                    file_url = str(q.get_file_url())
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
                                            'file': file_url,
                                            'pk': q.pk,
                                        }
                                    )
                                return JsonResponse({'questions': questions})

                            elif round.is_completed:
                                return redirect('score')
                            else:
                                return render(request, 'round.html', {'team': team, 'round': round})
                        return redirect('/')

            elif round.round == 3:
                if team in round.eligible_teams.all():
                    phase = request.GET.get('phase', None)
                    if phase:
                        if phase == "1":
                            print('phase is 1')
                            phase = Phase.objects.get(phase=1)
                        elif phase == "2":
                            print('phase 2')
                            phase = Phase.objects.get(phase=2)
                            question = round.get_question_set(team)
                            if question is not None:
                                options = question.get_options()
                            else:
                                options = []
                            return render(request, 'round3p2.html', {'team': team, 'round': round, 'question': question,'options':options})
                        elif round.is_completed:
                            return redirect('score')
                        else:
                            return render(request, 'round.html', {'team': team, 'round': round})
                    if Round.objects.get(round=1).is_completed and Round.objects.get(round=2).is_completed:
                        if not round.is_completed and round.is_live:
                            return render(request, 'round.html', {'team': team, 'round': round, 'phase': phase})
        return redirect('/')


def score(request, round_pk):
    if request.user.is_authenticated:
        try:
            round = Round.objects.get(pk=round_pk)
        except Round.DoesNotExist:
            round = None
        if round:
            score = round.get_scores()
            team = request.user.team_set.first()
            myscore = round.score_set.filter(team=team).first()
            return render(request, 'score.html', {'team':team,'score': score, 'my_score': myscore})
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
                    attempt = Attempt(team=team, question=question, round=question.round)
                    attempt.save()
                    print('attempt save')
                    return JsonResponse({'msg': 'success'})


def set_rank(request, round_pk):
    if request.user.is_authenticated:
        try:
            round = Round.objects.get(pk=round_pk)
        except Round.DoesNotExist:
            round = None
        if round:
            scores = round.score_set.all()
            for score in scores:
                score.set_rank()
            scoress = []
            scores = round.score_set.all()
            for score in scores:
                scoress.append({
                    'team_pk': score.team.pk,
                    'team_name': score.team.name,
                    'score': score.score,
                    'rank': score.rank,
                })

        return JsonResponse({'msg': 'success'})


def start_round(request):
    if request.user.is_superuser:
        if request.is_ajax():
            round_pk = request.POST.get('round_pk', None)
            try:
                round = Round.objects.get(pk=round_pk)
            except Round.DoesNotExist:
                round = None
            if round:
                if not round.is_completed:
                    if round.round is 1:
                        if round.is_live:
                            return JsonResponse({'msg': 'Round 1 already started!', 'res': 'success'})
                        else:
                            round.is_live = True
                            round.save()
                            return JsonResponse({'msg': 'Round 1 has been started', 'res': 'success'})
                    elif round.round is 2:
                        round1 = Round.objects.get(round=1)
                        if not round1.is_completed and not round1.is_live:
                            return JsonResponse({'msg': 'Complete Round 1 first'})
                        elif round.is_live:
                            return JsonResponse({'msg': 'Round 2 already started!', 'res': 'success'})
                        else:
                            round.is_live = True
                            round.save()
                            return JsonResponse({'msg': 'Round 2 has been started', 'res': 'success'})
                    elif round.round is 3:
                        round2 = Round.objects.get(round=2)

                        if not round2.is_completed and round2.is_live:
                            return JsonResponse({'msg': 'Complete Round 2 first'})
                        elif round2.is_live:
                            return JsonResponse({'msg': 'Round 3 already started!', 'res': 'success'})
                        else:
                            round.is_live = True
                            round.save()
                            return JsonResponse({'msg': 'Round 3 has been started', 'res': 'success'})


def stop_round(request):
    if request.user.is_superuser:
        if request.is_ajax():
            round_pk = request.POST.get('round_pk', None)
            try:
                round = Round.objects.get(pk=round_pk)
            except Round.DoesNotExist:
                round = None
            if round:
                if round.is_live:
                    round.is_live = False
                    round.is_completed = True
                    if round.round is 1:
                        Round.objects.get(round=2).fill_up_eligible_teams()
                    elif round.round is 2:
                        Round.objects.get(round=3).fill_up_eligible_teams()
                    round.save()

                    return JsonResponse({'res': 'success'})
                return JsonResponse({'res': 'error', 'msg': 'This round is not live'})


def set_phase_live(request):
    if request.user.is_superuser:
        if request.is_ajax():
            phase_pk = request.POST.get('phase_pk', None)
            if phase_pk:
                try:
                    phase = Phase.objects.get(pk=phase_pk)
                except Phase.DoesNotExist:
                    phase = None
                if phase is not None:
                    phase.is_live = True
                    phase.save()
                    return JsonResponse({'msg': 'success'})


def set_phase_unlive(request):
    if request.user.is_superuser:
        if request.is_ajax():
            phase_pk = request.POST.get('phase_pk', None)
            if phase_pk:
                try:
                    phase = Phase.objects.get(pk=phase_pk)
                except Phase.DoesNotExist:
                    phase = None
                if phase is not None:
                    phase.is_live = False
                    phase.save()
                    return JsonResponse({'msg': 'success'})


def check_for_provide_ques(request):
    if request.user.is_superuser:
        if request.is_ajax():
            bzrattempt = BzrAttempt.objects.last()
            if bzrattempt is not None:
                if bzrattempt.is_submitted is True:
                    return JsonResponse({'msg': 'true'})
                elif bzrattempt.team is None:
                    return JsonResponse({'msg': 'false', 'message': 'No one pressed the buzzer yet'})
                else:
                    return JsonResponse({'msg': 'false', 'message': bzrattempt.team.name + " wants to attempt"})
            return JsonResponse({'msg': 'true'})


# on provide btn click
def provide_question(request):
    if request.user.is_superuser:
        if request.is_ajax():
            bzrattempt = BzrAttempt.objects.last()
            if bzrattempt is not None:
                if bzrattempt.is_submitted is False:
                    return JsonResponse({'msg': 'Please submit the previous question'})
            # finding the question which is never provided before
            bzrattempts = BzrAttempt.objects.all()
            a_list = []
            for a in bzrattempts:
                a_list.append(a.question.pk)
            a_list = set(a_list)
            # todo change this for round3 questions
            question = Round.objects.get(round=1).question_set.filter(~Q(pk__in=a_list)).first()
            if question is not None:
                bzrattempt = BzrAttempt(round=Round.objects.get(round=3), question=question)
                bzrattempt.save()
                return JsonResponse({'msg': 'success'})
            return JsonResponse({'msg': 'question is not available in round3'})


# every 3 second
def get_ques_for_round_3p1(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            phase_pk = request.POST.get('phase_pk', None)
            if phase_pk:
                try:
                    phase = Phase.objects.get(pk=phase_pk)
                except Phase.DoesNotExist:
                    phase = None
                if phase:
                    if phase.is_live:
                        bzrattempt = BzrAttempt.objects.last()
                        if bzrattempt is not None:
                            if bzrattempt.team is None:
                                question = {
                                    'title': bzrattempt.question.title,
                                    'pk': bzrattempt.question.pk
                                }

                                return JsonResponse({'msg': 'success', 'question': question})
                            elif bzrattempt.team == request.user.team_set.first() and not bzrattempt.is_submitted:
                                option_set = bzrattempt.question.get_options()
                                options = []
                                for o in option_set:
                                    options.append({
                                        'title': o.title,
                                        'pk': o.pk,

                                    })
                                question = {
                                    'title': bzrattempt.question.title,
                                    'pk': bzrattempt.question.pk,
                                    'options': options,
                                }
                                return JsonResponse({'msg': 'unsubmitted', 'question': question})
                            else:
                                return JsonResponse({'msg': 'waiting for the next question'})
                        return JsonResponse({'msg': 'Waiting for the question provided by the quizmaster'})
                    return JsonResponse({'msg': 'end'})


def press_bzr(request):
    if request.user.is_authenticated:
        team = request.user.team_set.first()
        if request.is_ajax():
            bzrattempt = BzrAttempt.objects.last()
            if bzrattempt is not None:
                if bzrattempt.team is None:
                    bzrattempt.team = team
                    bzrattempt.save()
                    option_set = bzrattempt.question.get_options()
                    options = []
                    for o in option_set:
                        options.append({
                            'title': o.title,
                            'pk': o.pk,

                        })
                    question = {
                        'title': bzrattempt.question.title,
                        'pk': bzrattempt.question.pk,
                        'options': options,
                    }
                    return JsonResponse({'msg': 'success', 'question': question})
                return JsonResponse({'msg': 'Wait for the next question'})
