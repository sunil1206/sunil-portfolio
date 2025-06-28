
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import shutil, os
app = FastAPI()
# Allow frontend to access backend

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods =["*"],
    allow_headers =["*"],
)

model = YOLO('model/trash.pt')  # Trained YOLOv8 model

@app.post("/trash/")
async  def predict(file:UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    file_location =f"temp/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = model.predict(source=file_location)
    boxes =results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    confidences = results[0].boxes.conf.tolist()

    os.remove(file_location)
    return JSONResponse({
        "predictions": [
            {"class": int(cls), "box": box, "confidence": float(conf)}
            for cls, box, conf in zip(classes, boxes, confidences)
        ]
    })

plant_disease_model = YOLO('model/plant.pt')
# Plant disease prediction endpoint
@app.post("/plant-disease/")
async def predict_plant_disease(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = plant_disease_model.predict(source=file_location)
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    confidences = results[0].boxes.conf.tolist()

    os.remove(file_location)
    return JSONResponse({
        "predictions": [
            {"class": int(cls), "box": box, "confidence": float(conf)}
            for cls, box, conf in zip(classes, boxes, confidences)
        ]
    })

