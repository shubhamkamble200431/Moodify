import base64
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
import cv2
import tensorflow as tf
import time
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})
# Ensure the images directory exists
if not os.path.exists('images'):
    os.makedirs('images')

# Load the TensorFlow Keras model
def load_model():
    model = tf.keras.models.load_model('CNN.h5')
    return model

model = load_model()

def process_video(model, video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Cannot open video file")

    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    processed_frames = []
    processing_time_total = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame is None:
            print("Received None frame")
            continue  # Skip if frame is None

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = faceCascade.detectMultiScale(gray)
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
            final = classes[exp]

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f'Expression: {final}', (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)

            processing_time += end_time - start_time
            predictions.append(final)

        processed_frames.append(frame)
        processing_time_total += processing_time

    cap.release()

    if not processed_frames:
        raise ValueError("No frames processed")

    # Save the processed video
    processed_video_path = 'images/processed_video.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(processed_video_path, fourcc, 20.0, (processed_frames[0].shape[1], processed_frames[0].shape[0]))

    for processed_frame in processed_frames:
        out.write(processed_frame)

    out.release()
    return processing_time_total, predictions, processed_video_path

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['video']
    video_path = 'images/uploaded_video.mp4'
    file.save(video_path)

    try:
        processing_time, predictions, processed_video_path = process_video(model, video_path)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    # Convert video to base64
    with open(processed_video_path, 'rb') as video_file:
        processed_video_base64 = base64.b64encode(video_file.read()).decode('utf-8')
    print(predictions)
    data = {
        'processing_time': processing_time,
        'predictions': predictions,
        'video': processed_video_base64,  # Convert to base64 string for JSON serialization
        'video_url': f'http://127.0.0.1:5001/images/processed_video.mp4'
    }
   
    return jsonify(data)

@app.route('/images/<filename>')
def serve_file(filename):
    return send_from_directory('images', filename)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
