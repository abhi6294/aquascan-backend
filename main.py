import os
import io
import base64
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from huggingface_hub import hf_hub_download
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input

app = FastAPI(title="AquaScan Cloud Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REPO_ID = "abhimishra001/fish-disease-weights"
WEIGHT_FILE = "weights_efficientnetb0.weights.h5"

CLASSES = [
    'Bacterial Red disease',
    'Bacterial diseases - Aeromoniasis',
    'Bacterial gill disease',
    'Fungal diseases - Saprolegniasis',
    'Healthy Fish',
    'Parasitic diseases',
    'Viral diseases'
]

def build_efficientnet():
    inputs = tf.keras.Input(shape=(224, 224, 3))
    base = EfficientNetB0(include_top=False, weights=None, input_tensor=inputs)
    x = tf.keras.layers.GlobalAveragePooling2D()(base.output)
    x = tf.keras.layers.Dense(512, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.5)(x)
    x = tf.keras.layers.Dense(256, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(len(CLASSES), activation='softmax')(x)
    return tf.keras.Model(inputs=inputs, outputs=outputs), base

print("Building EfficientNetB0...")
model, base_model = build_efficientnet()

print("Downloading weights from Hugging Face...")
weights_path = hf_hub_download(repo_id=REPO_ID, filename=WEIGHT_FILE)
model.load_weights(weights_path)
print("EfficientNetB0 weights loaded successfully.")

# Setup Grad-CAM model targeting the final top activation block of EfficientNet
last_conv_layer = [layer for layer in base_model.layers if isinstance(layer, tf.keras.layers.Conv2D) or 'top_conv' in layer.name or 'conv' in layer.name][-1]
cam_model = tf.keras.models.Model(inputs=[model.inputs], outputs=[last_conv_layer.output, model.output])

@app.get("/")
def health_check():
    return {"status": "AquaScan AI Server Online (EfficientNetB0)"}

@app.post("/predict")
async def predict_api(file: UploadFile = File(...)):
    contents = await file.read()
    pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
    orig_np = np.array(pil_img)

    # Preprocessing
    resized = cv2.resize(orig_np, (224, 224))
    x = preprocess_input(np.expand_dims(resized.astype(np.float32), axis=0))

    # Prediction and Grad-CAM calculation
    with tf.GradientTape() as tape:
        conv_outputs, predictions = cam_model(x)
        top_idx = tf.argmax(predictions[0])
        loss = predictions[:, top_idx]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2)).numpy()
    conv_outputs = conv_outputs[0].numpy()

    # Heatmap generation
    cam = np.zeros(conv_outputs.shape[0:2], dtype=np.float32)
    for i, w in enumerate(pooled_grads):
        cam += w * conv_outputs[:, :, i]

    cam = np.maximum(cam, 0)
    if np.max(cam) != 0:
        cam = cam / np.max(cam)

    cam = cv2.resize(cam, (orig_np.shape[1], orig_np.shape[0]))
    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    overlay = np.uint8(orig_np * 0.55 + cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB) * 0.45)

    _, buffer = cv2.imencode('.jpg', cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
    b64_cam = "data:image/jpeg;base64," + base64.b64encode(buffer).decode('utf-8')

    pred_probs = predictions[0].numpy()
    conf_dict = {CLASSES[i]: float(pred_probs[i]) for i in range(len(CLASSES))}

    return JSONResponse(content={"cam_image": b64_cam, "confidences": conf_dict})
