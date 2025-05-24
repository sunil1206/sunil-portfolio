# import os
# import re
# import string
# import pickle
#
# from django.shortcuts import render
# from django.conf import settings
#
# # Use standalone Keras
# from keras.models import load_model
# from keras.preprocessing.sequence import pad_sequences
#
# # ——————————————————————————————————————————
# # 1. Load model & tokenizer once
# # ——————————————————————————————————————————
# from analytics.models import DataScienceProject
#
# MODEL_PATH = os.path.join(settings.BASE_DIR, 'spamdetection/models/light-gru_spam_model.h5')
# TOKENIZER_PATH = os.path.join(settings.BASE_DIR, 'spamdetection/models/tokenizer.pkl')
#
# try:
#     model = load_model(MODEL_PATH)
#     with open(TOKENIZER_PATH, 'rb') as f:
#         tokenizer = pickle.load(f)
#     load_error = None
# except Exception as e:
#     model = None
#     tokenizer = None
#     load_error = str(e)
#
# # ——————————————————————————————————————————
# # 2. Spam keywords & cleaning
# # ——————————————————————————————————————————
# # spam_keywords = {
# #     'win', 'free', 'prize', 'urgent', 'winner', 'cash', 'claim', 'offer',
# #     'limited', 'credit', 'congratulations', 'click', 'now', 'money',
# #     'bonus', 'buy', 'purchase', 'subscribe', 'reward', 'instant', 'discount',
# #     'deal', 'selected', 'cheap'
# # }
#
# spam_keywords = {
#     'win', 'free', 'prize', 'urgent', 'winner', 'cash', 'claim', 'offer',
#     'limited', 'credit', 'congratulations', 'click', 'now', 'money',
#     'bonus', 'buy', 'purchase', 'subscribe', 'reward', 'instant', 'discount',
#     'deal', 'selected', 'cheap', 'exclusive', 'guaranteed', 'risk-free',
#     'act now', 'call now', 'buy now', 'apply now', 'click here', 'order now',
#     'urgent response', 'limited time', 'easy money', 'no cost', 'trial',
#     'gift card', 'get paid', 'winner selected', 'double your', 'act fast',
#     'lowest price', 'pre-approved', 'miracle', 'this won’t last', 'earn money',
#     'insurance', 'work from home', 'investment', 'earn extra', 'no obligation',
#     'luxury', 'pills', 'lottery', 'viagra', 'lose weight', 'weight loss',
#     'income', 'fast cash', '100% free', 'free access', 'exclusive deal',
#     'clearance', 'satisfaction guaranteed', 'extra income', 'no fees'
# }
#
#
# def clean_text(text: str) -> str:
#     text = text.lower()
#     text = re.sub(r"http\S+|www\S+|https\S+", '', text)
#     text = re.sub(r'@\w+|\#', '', text)
#     text = text.translate(str.maketrans('', '', string.punctuation))
#     text = re.sub(r'\d+', '', text)
#     return re.sub(r'\s+', ' ', text).strip()
#
# # ——————————————————————————————————————————
# # 3. Prediction helper
# # ——————————————————————————————————————————
# def predict_spam_message(text: str):
#     cleaned = clean_text(text)
#     seq = tokenizer.texts_to_sequences([cleaned])
#     pad = pad_sequences(seq, maxlen=100, padding='post')
#     prob = float(model.predict(pad, verbose=0)[0][0])
#     label = "Spam" if prob > 0.5 else "Not Spam"
#     confidence = round(prob * 100, 2) if label == "Spam" else round((1 - prob) * 100, 2)
#     matched = [w for w in cleaned.split() if w in spam_keywords]
#     return label, confidence, matched
#
# # ——————————————————————————————————————————
# # 4. Django view
# # ——————————————————————————————————————————
# def predict_spam(request):
#     projects = DataScienceProject.objects.all()
#     context = {
#         'prediction': None,
#         'confidence': None,
#         'matched_words': [],
#         'error': load_error,
#         'projects':projects
#     }
#
#     if load_error:
#         # If we couldn’t load the model/tokenizer, show that error immediately
#         return render(request, 'prediction/prediction_spam.html', context)
#
#     if request.method == 'POST':
#         message = request.POST.get('email', '').strip()
#         if not message:
#             context['error'] = "Please enter a message to classify."
#         else:
#             try:
#                 label, confidence, matched = predict_spam_message(message)
#                 context.update({
#                     'prediction': label,
#                     'confidence': confidence,
#                     'matched_words': matched,
#                     'error': None
#                 })
#             except Exception as e:
#                 context['error'] = f"Prediction error: {e}"
#
#     return render(request, 'prediction/prediction_spam.html', context)

#
# import os
# import re
# import string
# import pickle
#
# from django.shortcuts import render
# from django.conf import settings
# from analytics.models import DataScienceProject
#
# # Use standalone Keras
# from keras.models import load_model
# from keras.preprocessing.sequence import pad_sequences
#
# # ——————————————————————————————————————————
# # 1. Load model & tokenizer once
# # ——————————————————————————————————————————
# MODEL_PATH = os.path.join(settings.BASE_DIR, 'spamdetection/models/light-gru_spam_model.h5')
#
# TOKENIZER_PATH = os.path.join(settings.BASE_DIR, 'spamdetection/models/tokenizer.pkl')
#
# try:
#     model = load_model(MODEL_PATH)
#     with open(TOKENIZER_PATH, 'rb') as f:
#         tokenizer = pickle.load(f)
#     load_error = None
# except Exception as e:
#     model = None
#     tokenizer = None
#     load_error = str(e)
#
# # ——————————————————————————————————————————
# # 2. Spam keywords & cleaning
# # ——————————————————————————————————————————
# spam_keywords = {
#     'win', 'free', 'prize', 'urgent', 'winner', 'cash', 'claim', 'offer',
#     'limited', 'credit', 'congratulations', 'click', 'now', 'money',
#     'bonus', 'buy', 'purchase', 'subscribe', 'reward', 'instant', 'discount',
#     'deal', 'selected', 'cheap', 'exclusive', 'guaranteed', 'risk-free',
#     'act now', 'call now', 'buy now', 'apply now', 'click here', 'order now',
#     'urgent response', 'limited time', 'easy money', 'no cost', 'trial',
#     'gift card', 'get paid', 'winner selected', 'double your', 'act fast',
#     'lowest price', 'pre-approved', 'miracle', 'this won’t last', 'earn money',
#     'insurance', 'work from home', 'investment', 'earn extra', 'no obligation',
#     'luxury', 'pills', 'lottery', 'viagra', 'lose weight', 'weight loss',
#     'income', 'fast cash', '100% free', 'free access', 'exclusive deal',
#     'clearance', 'satisfaction guaranteed', 'extra income', 'no fees'
# }
#
# def clean_text(text: str) -> str:
#     text = text.lower()
#     text = re.sub(r"http\S+|www\S+|https\S+", '', text)
#     text = re.sub(r'@\w+|\#', '', text)
#     text = text.translate(str.maketrans('', '', string.punctuation))
#     text = re.sub(r'\d+', '', text)
#     return re.sub(r'\s+', ' ', text).strip()
#
# # ——————————————————————————————————————————
# # 3. Prediction helper
# # ——————————————————————————————————————————
# def predict_spam_message(text: str):
#     cleaned = clean_text(text)
#     seq = tokenizer.texts_to_sequences([cleaned])
#     pad = pad_sequences(seq, maxlen=100, padding='post')
#     prob = float(model.predict(pad, verbose=0)[0][0])
#     label = "Spam" if prob > 0.5 else "Not Spam"
#     confidence = round(prob * 100, 2) if label == "Spam" else round((1 - prob) * 100, 2)
#     matched = [w for w in cleaned.split() if w in spam_keywords]
#     return label, confidence, matched
#
# # ——————————————————————————————————————————
# # 4. Django view
# # ——————————————————————————————————————————
# def predict_spam(request):
#     projects = DataScienceProject.objects.all()
#     context = {
#         'prediction': None,
#         'confidence': None,
#         'matched_words': [],
#         'error': load_error,
#         'projects':projects
#     }
#
#     if load_error:
#         # If we couldn’t load the model/tokenizer, show that error immediately
#         return render(request, 'prediction/prediction_spam.html', context)
#
#     if request.method == 'POST':
#         message = request.POST.get('email', '').strip()
#         if not message:
#             context['error'] = "Please enter a message to classify."
#         else:
#             try:
#                 label, confidence, matched = predict_spam_message(message)
#                 context.update({
#                     'prediction': label,
#                     'confidence': confidence,
#                     'matched_words': matched,
#                     'error': None
#                 })
#             except Exception as e:
#                 context['error'] = f"Prediction error: {e}"
#
#     return render(request, 'prediction/prediction_spam.html', context)

import requests
from django.shortcuts import render
from analytics.models import DataScienceProject

FASTAPI_URL = "http://127.0.0.1:8001/spam"  # FastAPI running port

def predict_spam(request):
    projects = DataScienceProject.objects.all()
    context = {
        'prediction': None,
        'confidence': None,
        'matched_words': [],
        'error': None,
        'projects': projects
    }

    if request.method == 'POST':
        message = request.POST.get('email', '').strip()
        if not message:
            context['error'] = "Please enter a message to classify."
        else:
            try:
                # Make request to FastAPI endpoint
                response = requests.post(
                    FASTAPI_URL,
                    json={"message": message}
                )
                if response.status_code == 200:
                    result = response.json()
                    context.update({
                        'prediction': result['prediction'],
                        'confidence': result['confidence'],
                        'matched_words': result['matched_keywords'],
                        'error': None
                    })
                else:
                    context['error'] = f"API Error: {response.json().get('detail', 'Unknown error')}"
            except Exception as e:
                context['error'] = f"Request failed: {e}"

    return render(request, 'prediction/prediction_spam.html', context)
