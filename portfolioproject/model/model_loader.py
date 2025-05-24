import pickle
import numpy as np
import os
#
# # Load the trained model
# model_path = os.path.join(os.path.dirname(__file__), "models/salary.pkl")
# with open(model_path, "rb") as file:
#     model = pickle.load(file)
#
# print("Model type:", type(model))
# # Function to predict salary
# def predict_salary(features):
#     features_array = np.array([features])  # Ensure it's 2D
#     prediction = model.predict(features_array)
#     return prediction[0]  # Return a single value
#
#
from django.shortcuts import render
import pickle
import os
from django.conf import settings


import pickle
import os
from django.conf import settings

# Construct the correct path
model_path = os.path.join(settings.BASE_DIR, 'model', 'models', 'model.pkl')

if os.path.exists(model_path):
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None
else:
    print(f"Model file not found: {model_path}")
    model = None


# Load Salary model
salary_model_path = os.path.join(settings.BASE_DIR, 'model', 'models', 'salary.pkl') #adjust path to your project.

if os.path.exists(salary_model_path):
    try:
        with open(salary_model_path, 'rb') as file:
            salary_model = pickle.load(file)
        print("Salary model loaded successfully!")
    except Exception as e:
        print(f"Error loading Salary model: {e}")
        salary_model = None
else:
    print(f"Salary model file not found: {salary_model_path}")
    salary_model = None


#Spotify
# Load Salary model
spotify_model_path = os.path.join(settings.BASE_DIR, 'model', 'models', 'spotify.pkl') #adjust path to your project.

if os.path.exists(spotify_model_path):
    try:
        with open(spotify_model_path, 'rb') as file:
            spotify_model = pickle.load(file)
        print("spotify model loaded successfully!")
    except Exception as e:
        print(f"Error loading spotify model: {e}")
        spotify_model = None
else:
    print(f"spotify model file not found: {spotify_model_path}")
    spotify_model = None