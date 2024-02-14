import cv2
from flask import Flask, Response

app = Flask(__name__)


def generate_frames():
    cap1 = cv2.VideoCapture(cv2.CAP_ANY)
    if not cap1.isOpened():
        print("Camera 1 not available")
        return

    cap2 = cv2.VideoCapture(cv2.CAP_ANY)
    if not cap2.isOpened():
        print("Camera 2 not available")
        return

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        if not ret1 or not ret2:
            break
        else:
            # Resize frames to have the same height
            height = min(frame1.shape[0], frame2.shape[0])
            frame1 = cv2.resize(frame1, (int(frame1.shape[1] * height / frame1.shape[0]), height))
            frame2 = cv2.resize(frame2, (int(frame2.shape[1] * height / frame2.shape[0]), height))

            # Concatenate frames horizontally
            merged_frame = cv2.hconcat([frame1, frame2])

            ret, buffer = cv2.imencode('.jpg', merged_frame)
            if ret:
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)