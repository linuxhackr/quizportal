from django.urls import path
from . import views
urlpatterns = [
    # path('', name='teams'),
    path('add_team',views.add_team, name='add_team'),

    path('team_logout',views.logout_team, name='team_logout'),
]