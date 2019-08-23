"""quizportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.views.static import serve
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from team.views import login_team
urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include('quiz.urls')),
    path('score/', include('score.urls')),
    path('team/', include('team.urls')),
    path('',login_team, name='team_login'),
    path('admin_panel', views.admin_panel, name='admin_panel'),
    path('qm', views.qm, name='qm'),
    path('livescore/<int:round_pk>', views.live_score, name='livescore'),


    path('add_quiz/',views.add_quiz, name='add_quiz')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

