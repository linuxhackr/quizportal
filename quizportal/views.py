from django.shortcuts import render
from django.http import JsonResponse
from quiz.models import Question, Option, Category, Round, Phase, BzrAttempt
from team.models import Team

def admin_panel(request):
    rounds = Round.objects.all()
    categories = Category.objects.all()
    return render(request, 'admin.html',{'rounds':rounds, 'categories':categories})

def add_quiz(request):
    if request.is_ajax():
        if request.method == "POST":
            data = request.POST
            question_text = data.get('question_text', None)
            option_1 = data.get('option_1', None)
            option_2 = data.get('option_2', None)
            option_3 = data.get('option_3', None)
            option_4 = data.get('option_4', None)
            category = data.get('category', None)
            right_option = data.get('right_option', None)
            round = data.get('round', None)
            if question_text and right_option and option_1 and option_2 and option_3 and option_4 and category and round:
                try:
                    category = Category.objects.get(pk=category)
                except category.DoesNotExist:
                    category = None
                try:
                    round = Round.objects.get(pk=round)
                except Round.DoesNotExist:
                    round = None
                if category and round:
                    question = Question(
                        category=category,
                        round=round,
                        title=question_text,
                    )
                    question.save()
                    option1 = Option(
                        question=question,
                        title=option_1,
                    )

                    if right_option is '1':
                        option1.is_right = True
                        print(right_option)
                    option1.save()
                    option2 = Option(
                        question=question,
                        title=option_2,
                    )
                    if right_option is '2':
                        option2.is_right = True
                    option2.save()
                    option3 = Option(
                        question=question,
                        title=option_3,
                    )
                    if right_option is '3':
                        option3.is_right = True
                    option3.save()
                    option4 = Option(
                        question=question,
                        title=option_4,
                    )
                    if right_option is '4':
                        option4.is_right = True
                    option4.save()

                return JsonResponse({'msg':'success, we have' + str(Question.objects.count()) + " questions ... Add more"})


def qm(request):
    if request.user.is_superuser:
        rounds = Round.objects.all()
        teams = Team.objects.all()
        phase1 = Phase.objects.get(phase=1)
        phase2 = Phase.objects.get(phase=2)
        return render(request, 'qm.html', {'rounds':rounds, 'teams':teams, 'phase1':phase1, 'phase2':phase2})


def live_score(request, round_pk):
    if round_pk:
        try:
            round = Round.objects.get(pk=round_pk)
        except Round.DoesNotExist:
            round = None
        if round is not None:
            scores_q = round.get_scores()

            return render(request, 'live_score.html', {'scores':scores_q, 'round':round})




