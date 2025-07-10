from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('birds/<int:bird_id>/', views.bird_detail, name='bird_detail'),
    path('upload/', views.upload_bird, name='upload_bird'),
    path('vote/', views.visitor_vote, name='visitor_vote'),
    path('evaluate/<int:bird_id>/', views.judge_evaluate, name='judge_evaluate'),
    path('judge-dashboard/', views.judge_dashboard, name='judge_dashboard'),
    path('results/', views.results, name='results'),
]
