from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
import subprocess
import os
import markdown
from .models import FitnessReport, UserProfile
from .forms import FitnessReportForm

subprocess.run(["python", "C:/Users/Sachi/Desktop/QQQ/tracker/AI-Fitness-trainer/main.py"], shell=True)


def home(request):
    return HttpResponse("<h1>Welcome to AI Health!</h1>")

@login_required
def generate_report(request):
    try:
        user = request.user
        profile = UserProfile.objects.get(user=user)

        if not profile.waist_measurement or not profile.hip_measurement:
            return HttpResponse("Waist and hip measurements are required.")

        report = FitnessReport.objects.create(
            user=user,
            bmi=profile.calculate_bmi(),
            body_fat_percentage=18.5,  # Placeholder value
            waist_to_hip_ratio=profile.waist_measurement / profile.hip_measurement,
        )

        return render(request, "reports/report.html", {"report": report})

    except UserProfile.DoesNotExist:
        return HttpResponse("User profile not found.")

@login_required
def start_workout_tracking(request):
    """Start workout tracking via subprocess"""
    if request.method == "POST":
        workout_type = request.POST.get("workout_type")

        if workout_type not in ["sit-up", "pull-up", "push-up", "squat", "walk"]:
            return JsonResponse({"error": "Invalid workout type"}, status=400)

        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "AI-Fitness-trainer", "main.py")

        try:
            subprocess.Popen(["python", script_path, "-t", workout_type])
            return JsonResponse({"message": f"Workout tracking started for {workout_type}!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@login_required
def user_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('generate_report')  # Redirect to the report page
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'reports/user_profile.html', {'form': form})

@login_required
def fitness_report_view(request):
    ai_suggestions = None
    if request.method == "POST":
        form = FitnessReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)  # Do not save yet
            report.user = request.user  # Assign the logged-in user
            report.ai_suggestions = report.generate_ai_suggestions()
            report.save()  # Now save
            ai_suggestions = markdown.markdown(report.ai_suggestions)  # Convert Markdown to HTML
    else:
        form = FitnessReportForm()
    
    return render(request, "fitness_report.html", {"form": form, "ai_suggestions": ai_suggestions})
