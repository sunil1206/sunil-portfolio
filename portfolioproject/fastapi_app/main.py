from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from keras.models import load_model
from PIL import Image
import numpy as np
import io

app = FastAPI()

# Load the model once
MODEL_PATH = "model/cifar10_model.h5"
model = load_model(MODEL_PATH)
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

@app.get("/")
def root():
    return {"message": "CIFAR-10 FastAPI Model Ready!"}

@app.post("/predict/")
async def predict_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image = image.resize((32, 32))
        img_array = np.array(image).astype("float32") / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)
        label = class_names[np.argmax(prediction)]
        confidence = round(np.max(prediction) * 100, 2)

        return JSONResponse(content={
            "prediction": label,
            "confidence": confidence
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
