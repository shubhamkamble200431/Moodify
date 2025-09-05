from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import numpy as np
import cv2
import tensorflow as tf
import time
import os

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})  # Enable CORS for all routes

# Ensure the images directory exists
if not os.path.exists('images'):
    os.makedirs('images')
    
# Load the TensorFlow Keras model
def load_model():
    model = tf.keras.models.load_model('CNN.h5')
    return model

model = load_model()

def process_image(model, frame):
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(frame)
    processing_time = 0
    predictions = []

    for (x, y, w, h) in faces:
        face_region = frame[y:y+h, x:x+w]
        face_region = cv2.resize(face_region, (48, 48))
        face_region = face_region / 255.0
        face_region = face_region.reshape((1, 48, 48, 3))

        start_time = time.time()
        pred = model.predict(face_region)
        end_time = time.time()

        exp = np.argmax(pred)
        classes = ['sad', 'angry', 'surprise', 'happy', 'disgust', 'neutral', 'fear']
        final = classes[exp-1]

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f'Expression: {final}', (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)

        processing_time = end_time - start_time
        predictions.append(final)

    return processing_time, predictions, frame

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    npimg = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    processing_time, predictions, processed_frame = process_image(model, frame)

    text = f"Processing time: {processing_time:.4f} seconds"
    cv2.putText(processed_frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA)

    image_path = 'images/processed_image.jpg'
    cv2.imwrite(image_path, processed_frame)
    
    # Convert image to base64
    _, buffer = cv2.imencode('.jpg', processed_frame)
    processed_frame_base64 = base64.b64encode(buffer).decode('utf-8')

    data = {
        'processing_time': processing_time,
        'predictions': predictions,
        'image': processed_frame_base64,  # Convert to base64 string for JSON serialization
        'image_url': f'http://127.0.0.1:8001/images/processed_image.jpg'
    }

    return jsonify(data)

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

if __name__ == '__main__':
    app.run(port=8001, debug=True)
