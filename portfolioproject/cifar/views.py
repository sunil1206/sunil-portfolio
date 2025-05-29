import os
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from keras.models import load_model
from PIL import Image
import numpy as np
#
# Load the model once
from analytics.models import DataScienceProject
#
# MODEL_PATH = os.path.join('cifar', 'models', 'cifar10_model.h5')
# try:
#     model = load_model(MODEL_PATH, compile=False)
#     load_error = None
# except Exception as e:
#     model = None
#     load_error = str(e)
#
#
# model = load_model(MODEL_PATH)
#
# class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
#                'dog', 'frog', 'horse', 'ship', 'truck']
#
# def predict_image(request):
#     projects = DataScienceProject.objects.all()
#     label = None
#     if request.method == 'POST' and request.FILES.get('image'):
#         img_file = request.FILES['image']
#
#         # Save uploaded file temporarily and get full path
#         temp_file_path = default_storage.save('temp/temp.jpg', img_file)
#         temp_full_path = default_storage.path(temp_file_path)
#
#         # Open and preprocess image
#         img = Image.open(temp_full_path).convert('RGB').resize((32, 32))
#         img = np.array(img).astype('float32') / 255.0
#         img = np.expand_dims(img, axis=0)
#
#         # Predict
#         prediction = model.predict(img)
#         label = class_names[np.argmax(prediction)]
#
#         # Optionally delete the temp file after prediction
#         default_storage.delete(temp_file_path)
#
#     return render(request, 'prediction/prediction_cifar.html', {'label': label,'projects':projects})
import requests
from django.shortcuts import render

def predict_from_fastapi(request):
    projects = DataScienceProject.objects.all()
    label = None
    confidence = None
    error = None

    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        try:
            response = requests.post(
                'http://127.0.0.1:8002/predict',
                files={'file': (image.name, image.read(), image.content_type)}
            )
            result = response.json()
            label = result.get('prediction')
            confidence = result.get('confidence')
            error = result.get('error')
        except Exception as e:
            error = str(e)

    return render(request, 'prediction/prediction_cifar.html', {
        'label': label,
        'confidence': confidence,
        'error': error,
        'projects':projects
    })



from django.shortcuts import render
import cv2
import numpy as np
import base64
#
# @csrf_exempt
# def webcam_predict(request):
#     projects = DataScienceProject.objects.all()
#     label = None
#
#     if request.method == 'POST':
#         data_uri = request.POST.get('image_data')
#         if data_uri:
#             header, encoded = data_uri.split(",", 1)
#             image_data = base64.b64decode(encoded)
#
#             # Convert to OpenCV image
#             nparr = np.frombuffer(image_data, np.uint8)
#             img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#             img = cv2.resize(img, (32, 32))
#             img = img.astype('float32') / 255.0
#             img = np.expand_dims(img, axis=0)
#
#             prediction = model.predict(img)
#             label = class_names[np.argmax(prediction)]
#
#     return render(request, 'prediction/webcam/webcam.html', {'label': label,'projects':projects})
