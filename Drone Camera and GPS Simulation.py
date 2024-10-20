from flask import Flask, render_template, Response
import cv2
from geopy.geocoders import Nominatim
import random

app = Flask(__name__)

# Function to access the camera (simulating drone camera)
def get_camera_feed():
    camera = cv2.VideoCapture(0)  # 0 for default webcam, replace with drone camera if available

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encoding the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield frame in HTTP byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Function to simulate GPS coordinates (replace with real GPS data)
def get_gps_location():
    # Random location generation for simulation
    latitude = 51.5 + random.uniform(-0.1, 0.1)
    longitude = -0.1 + random.uniform(-0.1, 0.1)

    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(f"{latitude}, {longitude}")

    return f"Latitude: {latitude}, Longitude: {longitude}, Location: {location.address}"

@app.route('/')
def home():
    gps_data = get_gps_location()
    return render_template('index.html', gps_data=gps_data)

# Route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(get_camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
