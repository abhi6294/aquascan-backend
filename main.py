import os
import io
import base64
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from huggingface_hub import hf_hub_download
from tensorflow.keras.applications import (
    EfficientNetB0, ResNet50, MobileNetV3Large, 
    VGG19, DenseNet121, InceptionV3
)
from tensorflow.keras.applications import (
    efficientnet, resnet50, mobilenet_v3, 
    vgg19, densenet, inception_v3
)

app = FastAPI(title="AquaScan Cloud Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REPO_ID = "abhimishra001/fish-disease-weights"

CLASSES = [
    'Bacterial Red disease',
    'Bacterial diseases - Aeromoniasis',
    'Bacterial gill disease',
    'Fungal diseases - Saprolegniasis',
    'Healthy Fish',
    'Parasitic diseases',
    'Viral diseases'
]

ENSEMBLE_WEIGHTS = {
    'efficientnetb0': 0.20,
    'resnet50': 0.20,
    'mobilenetv3': 0.15,
    'vgg19': 0.15,
    'densenet': 0.15,
    'inceptionv3': 0.15
}

WEIGHT_FILES = {
    'efficientnetb0': 'weights_efficientnetb0.weights.h5',
    'resnet50': 'weights_resnet50.weights.h5',
    'mobilenetv3': 'weights_mobilenetv3.weights.h5',
    'vgg19': 'weights_vgg19.weights.h5',
    'densenet': 'weights_densenet.weights.h5',
    'inceptionv3': 'weights_inceptionv3.weights.h5'
}

def build_model(model_name):
    target_size = (299, 299) if model_name == 'inceptionv3' else (224, 224)
    inputs = tf.keras.Input(shape=(*target_size, 3))
    
    if model_name == 'efficientnetb0':
        base = EfficientNetB0(include_top=False, weights=None, input_tensor=inputs)
        prep = efficientnet.preprocess_input
    elif model_name == 'resnet50':
        base = ResNet50(include_top=False, weights=None, input_tensor=inputs)
        prep = resnet50.preprocess_input
    elif model_name == 'mobilenetv3':
        base = MobileNetV3Large(include_top=False, weights=None, input_tensor=inputs)
        prep = mobilenet_v3.preprocess_input
    elif model_name == 'vgg19':
        base = VGG19(include_top=False, weights=None, input_tensor=inputs)
        prep = vgg19.preprocess_input
    elif model_name == 'densenet':
        base = DenseNet121(include_top=False, weights=None, input_tensor=inputs)
        prep = densenet.preprocess_input
    elif model_name == 'inceptionv3':
        base = InceptionV3(include_top=False, weights=None, input_tensor=inputs)
        prep = inception_v3.preprocess_input

    x = tf.keras.layers.GlobalAveragePooling2D()(base.output)
    x = tf.keras.layers.Dense(512, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.5)(x)
    x = tf.keras.layers.Dense(256, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(len(CLASSES), activation='softmax')(x)
    return tf.keras.Model(inputs=inputs, outputs=outputs), prep

print("Initializing models and loading weights...")
loaded_models = {}
loaded_prep = {}

for m_name in ENSEMBLE_WEIGHTS.keys():
    model, prep = build_model(m_name)
    path = hf_hub_download(repo_id=REPO_ID, filename=WEIGHT_FILES[m_name])
    model.load_weights(path)
    loaded_models[m_name] = model
    loaded_prep[m_name] = prep
    print(f"Loaded: {m_name}")

resnet = loaded_models['resnet50']
last_conv = [layer for layer in resnet.layers if len(layer.output.shape) == 4][-1]
cam_submodel = tf.keras.models.Model(inputs=[resnet.inputs], outputs=[last_conv.output, resnet.output])

@app.get("/")
def health_check():
    return {"status": "AquaScan AI Server Online"}

@app.post("/predict")
async def predict_api(file: UploadFile = File(...)):
    contents = await file.read()
    pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
    orig_np = np.array(pil_img)

    ensemble_preds = np.zeros(len(CLASSES), dtype=np.float32)
    for m_name, weight in ENSEMBLE_WEIGHTS.items():
        model = loaded_models[m_name]
        prep_fn = loaded_prep[m_name]
        target_size = (model.input_shape[1], model.input_shape[2])
        resized = cv2.resize(orig_np, target_size)
        x = prep_fn(np.expand_dims(resized.astype(np.float32), axis=0))
        pred = model(x, training=False).numpy()[0]
        ensemble_preds += weight * pred

    top_idx = int(np.argmax(ensemble_preds))

    x_cam = loaded_prep['resnet50'](np.expand_dims(cv2.resize(orig_np, (224, 224)).astype(np.float32), axis=0))
    with tf.GradientTape() as tape:
        conv_out, preds = cam_submodel(x_cam)
        loss = preds[:, top_idx]
    grads = tape.gradient(loss, conv_out)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2)).numpy()
    conv_out = conv_out[0].numpy()
    
    cam = np.zeros(conv_out.shape[0:2], dtype=np.float32)
    for i, w in enumerate(pooled_grads):
        cam += w * conv_out[:, :, i]
    cam = np.maximum(cam, 0)
    if np.max(cam) != 0:
        cam = cam / np.max(cam)
    cam = cv2.resize(cam, (orig_np.shape[1], orig_np.shape[0]))
    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    overlay = np.uint8(orig_np * 0.55 + cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB) * 0.45)
    
    _, buffer = cv2.imencode('.jpg', cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
    b64_cam = "data:image/jpeg;base64," + base64.b64encode(buffer).decode('utf-8')

    conf_dict = {CLASSES[i]: float(ensemble_preds[i]) for i in range(len(CLASSES))}
    return JSONResponse(content={"cam_image": b64_cam, "confidences": conf_dict})
