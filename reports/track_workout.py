import cv2
import mediapipe as mp
import openai
import django
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AiHealth.settings")
django.setup()

from reports.models import WorkoutTracking
from django.contrib.auth.models import User

# Mediapipe setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# OpenAI API Key (securely fetched)
OPENAI_API_KEY = os.getenv( "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")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API Key is missing! Check your .env file.")

openai.api_key = OPENAI_API_KEY

def analyze_pose(landmarks):
    """Convert pose landmarks to a structured format and request AI feedback."""
    pose_data = {f"point_{i}": (lm.x, lm.y, lm.z) for i, lm in enumerate(landmarks.landmark)}

    try:
        # Send pose data to GPT for analysis
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a fitness coach analyzing workout form."},
                {"role": "user", "content": f"Here is the user's workout posture data: {pose_data}. Provide feedback."}
            ]
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "Error generating AI feedback."

def track_workout(user_id):
    """Track user's workout using webcam, analyze movement, and store feedback in the database."""
    cap = cv2.VideoCapture(0)  # Open webcam
    if not cap.isOpened():
        print("Error: Could not access webcam.")
        return
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        print("Error: User not found in the database.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            # Draw pose landmarks
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # AI analysis
            feedback = analyze_pose(results.pose_landmarks)

            # Save to database
            WorkoutTracking.objects.create(
                user=user, 
                feedback=feedback, 
                calories_burned=100  # Placeholder value
            )
            print("AI Feedback:", feedback)

        cv2.imshow("Workout Tracking", frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            print("Workout tracking stopped by user.")
            break

    cap.release()
    cv2.destroyAllWindows()
