from django.db import models
from django.contrib.auth.models import User
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure API Key is loaded
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY is missing in your .env file!")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)


class UserProfile(models.Model):
    """User Profile containing essential details"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    height = models.FloatField()  # cm
    weight = models.FloatField()  # kg
    waist_measurement = models.FloatField(default=80.0)  # cm
    hip_measurement = models.FloatField(default=94.0)  # cm

    def calculate_bmi(self):
        """Calculate BMI (Body Mass Index)"""
        height_in_m = self.height / 100  # Convert cm to meters
        return round(self.weight / (height_in_m ** 2), 2)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class FitnessReport(models.Model):
    """Stores fitness-related data and AI-generated suggestions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bmi = models.FloatField()
    body_fat_percentage = models.FloatField()
    waist_to_hip_ratio = models.FloatField()
    ai_suggestions = models.TextField(blank=True, null=True)

    def generate_ai_suggestions(self):
        """Generate AI-based workout suggestions based on user's fitness data"""
        prompt = (
            f"The user has the following fitness stats:\n"
            f"- BMI: {self.bmi}\n"
            f"- Body Fat Percentage: {self.body_fat_percentage}%\n"
            f"- Waist to Hip Ratio: {self.waist_to_hip_ratio}\n\n"
            "Provide a customized workout and diet plan to improve their health for a week ."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Use the preferred AI model
                messages=[
                    {"role": "system", "content": "You are a professional fitness trainer providing personalized advice."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()

        except openai.OpenAIError as e:
            return f"⚠️ OpenAI API error: {str(e)}"

        except Exception as e:
            return f"⚠️ Unexpected error: {str(e)}"

    def save(self, *args, **kwargs):
        """Auto-generate AI suggestions on save"""
        if not self.ai_suggestions:
            self.ai_suggestions = self.generate_ai_suggestions()
        super().save(*args, **kwargs)


class WorkoutTracking(models.Model):
    """Tracks user's workout progress"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    calories_burned = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Workout for {self.user.username} on {self.recorded_at}"
