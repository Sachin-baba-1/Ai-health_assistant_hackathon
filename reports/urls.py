# reports/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.fitness_report_view, name='fitness_report'),
    path('generate/', views.generate_report, name='generate_report'),
    path('profile/', views.user_profile, name='user_profile'),
    path('fitness-report/', views.fitness_report_view, name='fitness_report'),

]