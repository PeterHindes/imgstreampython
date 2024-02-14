from flask import Flask, Response, send_file
import cv2

app = Flask(__name__)

def generate_frames():
    # Open all available cameras
    cameras = []
    for i in range(10):  # Assuming up to 4 cameras are available
        cap = cv2.VideoCapture(cv2.CAP_ANY)
        if cap.isOpened():
            cameras.append(cap)
    if not cameras:
        print("No cameras available")
        return

    while True:
        frames = []
        for cap in cameras:
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
        if not frames:
            print("No frames")
            break
        else:
            # Resize frames to have the same height
            min_height = min(frame.shape[0] for frame in frames)
            resized_frames = [cv2.resize(frame, (int(frame.shape[1] * min_height / frame.shape[0]), min_height)) for frame in frames]

            # Concatenate all frames horizontally
            concatenated_frame = cv2.hconcat(resized_frames)

            ret, buffer = cv2.imencode('.jpg', concatenated_frame)
            if ret:
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return send_file('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
