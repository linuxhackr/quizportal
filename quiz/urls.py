from django.urls import path
from . import views
urlpatterns = [
    path('categories',views.categories, name='categories'),
    path('rounds',views.rounds, name='rounds'),  # it will give the round info whether this is locked or unlocked for that particular team
    path('round/<int:round_pk>',views.round,name='round'),  # it is the interface and shows to every team
    path('round/<int:round_pk>/score',views.score, name='round_score'),

    path('attempt_question/', views.attempt_question, name='attempt_question'),

    path('set_category',views.set_category, name='set_category'),  # will take the category as input and save to the team.category
    # path('start_round/<int:pk>', name='start_round'),  # round/1|2|3 started [ it will show unlocked to the eligible teams]
    # path('stop_round/<int:pk>', name='stop_round'),  # round/1|2|3 stopped [ it will stop taking responses and updating scores after 1 seconds]
    # path('get_rank/<int:pk>', name='get_rank'),  # after round stopped we can get or set the rank
    # path('set_eligibly/<int:pk>', name='set_eligibly'),  # after getting rank we can fill the eligibly for the next round

]


"""
RANKING
TEAM FROM USER
SHUFFLE QUESTION
VERIFY ELIGIBLE TEAMS FOR A SPECIFIC ROUND
"""
