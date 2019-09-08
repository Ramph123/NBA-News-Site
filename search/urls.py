from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('latest/', views.latest, name = 'latest'),
    path('hotlist/', views.hotlist, name = 'hotlist'),
    path('result/', views.result, name = 'result'),
    path('team/<int:team_id>/', views.team, name='team'),
    path('news/<int:news_id>/', views.news, name='news'),
]