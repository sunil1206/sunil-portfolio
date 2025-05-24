import os
import pickle
import numpy as np
from django.conf import settings
from django.shortcuts import render
from analytics.models import DataScienceProject  # Adjust import as needed
from joblib import load

# Utility function to load models dynamically
def load_model(model_path):
    """Loads a machine learning model from a file."""
    full_path = os.path.join(settings.BASE_DIR, model_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Model file not found: {full_path}")

    with open(full_path, 'rb') as file:
        return pickle.load(file)


# Iris Prediction
def predict_iris(request):
    projects = DataScienceProject.objects.all()
    prediction = None

    if request.method == "POST":
        try:
            features = np.array([[
                float(request.POST['sepal_length']),
                float(request.POST['sepal_width']),
                float(request.POST['petal_length']),
                float(request.POST['petal_width'])
            ]])

            iris_model = load('model/models/model.joblib')  # Adjust path if needed
            prediction = iris_model.predict(features)[0]

        except Exception as e:
            prediction = f"Error: {e}"

    return render(request, 'prediction/prediction_iris.html', {'prediction': prediction, 'projects': projects})


# Salary Prediction
def predict_salary(request):
    projects = DataScienceProject.objects.all()
    prediction = None

    if request.method == "POST":
        try:
            features = np.array([[
                int(request.POST['MarriedID']),
                int(request.POST['MaritalStatusID']),
                int(request.POST['GenderID']),
                int(request.POST['EmpStatusID']),
                int(request.POST['DeptID']),
                int(request.POST['PerfScoreID']),
                int(request.POST['FromDiversityJobFairID']),
                int(request.POST['Position']),
                int(request.POST['State']),
                int(request.POST['CitizenDesc']),
                int(request.POST['PerformanceScore']),
                float(request.POST['EngagementSurvey']),
                int(request.POST['SpecialProjectsCount']),
                int(request.POST['Experience']),
                float(request.POST['carrierbreak']),
                int(request.POST['AgeGroup'])
            ]])

            salary_model = load_model('model/models/salary.pkl')  # Adjust path if needed
           # prediction = salary_model.predict(features)[0]
            prediction = int(round(salary_model.predict(features)[0]))
        except Exception as e:
            prediction = f"Error: {e}"

    return render(request, "prediction/predict.html", {"prediction": prediction, "projects": projects})


# Spotify Prediction
def predict_spotify(request):
    projects = DataScienceProject.objects.all()
    predict_spotify = None

    if request.method == "POST":
        try:
            features = np.array([[
                float(request.POST['name']),
                float(request.POST['speechiness']),
                float(request.POST['loudness']),
                float(request.POST['artists']),
                float(request.POST['danceability']),
                float(request.POST['energy'])
            ]])

            spotify_model = load_model('model/models/spotify.pkl')  # Adjust path if needed
            predict_spotify = spotify_model.predict(features)[0]

        except Exception as e:
            predict_spotify = f"Error: {e}"

    return render(request, 'prediction/prediction_spotify.html',
                  {'predict_spotify': predict_spotify, 'projects': projects})
