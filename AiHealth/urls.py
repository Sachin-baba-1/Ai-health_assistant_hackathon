# AiHealth/urls.py
from django.contrib import admin
from django.urls import path, include
from reports.views import start_workout_tracking  # ✅ Correct

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("reports/", include("reports.urls")),
    path("start-workout/", start_workout_tracking, name="start_workout"),
]
