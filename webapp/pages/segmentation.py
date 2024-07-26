import streamlit as st
from PIL import Image
import time
import torch
import torchvision.transforms as TF
from transformers import SegformerForSemanticSegmentation
from dataclasses import dataclass
import sqlite3
import io
import matplotlib.pyplot as plt
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

@dataclass
class Configs:
    NUM_CLASSES: int = 4
    CLASSES: tuple = ("Large bowel", "Small bowel", "Stomach")
    IMAGE_SIZE: tuple[int, int] = (266, 266)
    MEAN: tuple = (0.485, 0.456, 0.406)
    STD: tuple = (0.229, 0.224, 0.225)
    MODEL_NAME: str = "davidle7/segformer"

class2hexcolor = {
    "Stomach": "#FFA07A",
    "Small bowel": "#20B2AA",
    "Large bowel": "#9370DB"
}

def initialize_device():
    if torch.cuda.is_available():
        return torch.device("cuda:0")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")

DEVICE = initialize_device()

def get_model(model_name, num_classes):
    model = SegformerForSemanticSegmentation.from_pretrained(
        model_name,
        num_labels=num_classes,
        ignore_mismatched_sizes=True
    )
    return model

preprocess = TF.Compose([
    TF.Resize(size=Configs.IMAGE_SIZE[::-1]),
    TF.Lambda(lambda img: img.convert("RGB")),
    TF.ToTensor(),
    TF.Normalize(Configs.MEAN, Configs.STD, inplace=True),
])

try:
    model = get_model(model_name=Configs.MODEL_NAME, num_classes=Configs.NUM_CLASSES)
    model.to(DEVICE)
    model.eval()
except Exception as e:
    logging.error(f"An error occurred: {e}")
    exit(1)

def setup_database():
    database_dir = 'databases'
    database_path = os.path.join(database_dir, 'inference_data.db')
    
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
    
    conn = sqlite3.connect(database_path, timeout=10)
    try:
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS model_inference (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT,
                model_version TEXT,
                model_type TEXT,
                input_image BLOB,
                input_size TEXT,
                output_segmentation BLOB,
                inference_time REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                device TEXT,
                system_load REAL,
                accuracy REAL,
                loss REAL
            )''')
    finally:
        conn.close()

def predict(input_image):
    shape_H_W = input_image.size[::-1]
    input_tensor = preprocess(input_image)
    input_tensor = input_tensor.unsqueeze(0).to(DEVICE)

    start_time = time.time()
    with torch.inference_mode():
        outputs = model(pixel_values=input_tensor, return_dict=True)
    inference_time = time.time() - start_time

    predictions = torch.nn.functional.interpolate(outputs.logits, size=shape_H_W, mode="bilinear", align_corners=False)
    preds_argmax = predictions.argmax(dim=1).cpu().squeeze().numpy()
    seg_info = [(preds_argmax == idx, class_name) for idx, class_name in enumerate(Configs.CLASSES, 1)]

    return input_image, seg_info, preds_argmax, inference_time

def plot_segmentation(input_image, seg_info, preds_argmax):
    input_image = input_image.convert("L")
    plt.figure(figsize=(10, 10))
    plt.imshow(input_image, cmap='gray')
    for mask, class_name in seg_info:
        plt.contour(mask, colors=[class2hexcolor[class_name]], alpha=0.5)
    plt.axis('off')
    return plt

def save_inference_details(model_name, input_image, output_segmentation, inference_time):
    database_path = 'databases/inference_data.db'
    
    input_image_bytes = io.BytesIO()
    input_image.save(input_image_bytes, format='PNG')
    input_image_blob = input_image_bytes.getvalue()

    output_segmentation_bytes = io.BytesIO()
    np.save(output_segmentation_bytes, output_segmentation)
    output_segmentation_blob = output_segmentation_bytes.getvalue()

    conn = sqlite3.connect(database_path, timeout=10)
    try:
        with conn:
            conn.execute('''INSERT INTO model_inference (model_name, model_version, model_type, input_image, input_size, output_segmentation, inference_time, device, system_load)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (model_name, "1.0", "Segformer", input_image_blob, str(Configs.IMAGE_SIZE), output_segmentation_blob, inference_time, DEVICE.type, 0.5))
    finally:
        conn.close()

def show():
    setup_database()
    
    st.title("Image Segmentation Page")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            st.write("")
            st.write("Segmenting...")

            input_image, seg_info, preds_argmax, inference_time = predict(image)
            st.write(f"Inference Time: {inference_time:.4f} seconds")

            plot = plot_segmentation(input_image, seg_info, preds_argmax)
            st.pyplot(plot)

            st.markdown("### Class Labels")
            for class_name, color in class2hexcolor.items():
                st.markdown(f"<span style='color:{color};'>⬤</span> {class_name}", unsafe_allow_html=True)

            save_inference_details(Configs.MODEL_NAME, image, preds_argmax, inference_time)
            st.write("Inference details saved to database.")

        except Exception as e:
            st.error(f"An error occurred during segmentation: {e}")
            logging.error(f"An error occurred during segmentation: {e}")

if __name__ == "__main__":
    show()
