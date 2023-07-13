from website import create_app
from flask import Flask, Blueprint, render_template, Response
import cv2
import numpy as np 
from ultralytics import YOLO
from roboflow import Roboflow
import os 
import datetime as date



app = create_app()

cap = cv2.VideoCapture(0)
model = YOLO('D:/flask_project/Project/runs/detect/train3/weights/best.pt')
threshold = 0.5
class_name_dict = {0: 'number_plate'}

# Set the desired frame rate
frame_rate = 30  # Adjust this value as per your requirements

# Calculate the delay between frames based on the desired frame rate
frame_delay = int(1000 / frame_rate)

# Set the desired frame size
frame_width = 640  # Desired width for resizing
frame_height = 480  # Desired height for resizing



def generate_frames():
    last_frame_time = 0
    while True:
        if (cv2.getTickCount() - last_frame_time) / cv2.getTickFrequency() < frame_delay / 1000.0:
            continue
        ret, frame = cap.read()

        if ret:
            frame = cv2.resize(frame, (frame_width, frame_height))
            results = model(frame)[0]

            for result in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = result

                if score > threshold:
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                    cv2.putText(frame, class_name_dict[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
                    
                    
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        # Update the last frame time
        last_frame_time = cv2.getTickCount()

@app.route('/detect')
def detect():
    return render_template("detect.html")

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)