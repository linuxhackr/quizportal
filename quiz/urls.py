from django.urls import path
from . import views
urlpatterns = [
    path('categories',views.categories, name='categories'),
    path('rounds',views.rounds, name='rounds'),  # it will give the round info whether this is locked or unlocked for that particular team
    path('round/<int:round_pk>',views.round,name='round'),  # it is the interface and shows to every team
    path('round/<int:round_pk>/score',views.score, name='round_score'),

    path('attempt_question/', views.attempt_question, name='attempt_question'),

    path('set_category',views.set_category, name='set_category'),  # will take the category as input and save to the team.category
    path('start_round',views.start_round, name='start_round'),  # round/1|2|3 started [ it will show unlocked to the eligible teams]
    path('stop_round',views.stop_round, name='stop_round'),  # round/1|2|3 stopped [ it will stop taking responses and updating scores after 1 seconds]
    path('set_rank/<int:pk>',views.set_rank, name='set_rank'),  # after round stopped we can get or set the rank
    # path('get_eligibles/<int:pk>', name='set_eligibly'),  # after getting rank we can fill the eligibly for the next round

    # ROUND 3

    path('set_phase_live', views.set_phase_live, name='set_phase_live'),
    path('check_for_provide_ques', views.check_for_provide_ques, name='check_for_provide_question'),
    path('provide_ques', views.provide_question, name='provide_question'),
    path('set_phase_unlive',views.set_phase_unlive, name='set_phase_unlive'),

    path('get-ques-for-round-3p1', views.get_ques_for_round_3p1, name='get_ques_r3p1'),
    path('press-bzr', views.press_bzr, name='press_bzr'),

]


"""
RANKING
TEAM FROM USER
SHUFFLE QUESTION
VERIFY ELIGIBLE TEAMS FOR A SPECIFIC ROUND
"""
