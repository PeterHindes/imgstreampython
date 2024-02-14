from flask import Flask, Response, send_file
import cv2
import threading

app = Flask(__name__)

class FrameStreamer:
    def __init__(self):
        self.frames = []
        self.cameras = []
        self.lock = threading.Lock()

        # Open all available cameras
        for i in range(10):  # Assuming up to 10 cameras are available
            cap = cv2.VideoCapture(cv2.CAP_ANY)
            if cap.isOpened():
                self.cameras.append(cap)
        
        if not self.cameras:
            print("No cameras available")
            return

        self.thread = threading.Thread(target=self._capture_frames)
        self.thread.daemon = True
        self.thread.start()

    def _capture_frames(self):
        while True:
            frames = []
            for cap in self.cameras:
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

                with self.lock:
                    self.frames = concatenated_frame

    def get_frame(self):
        with self.lock:
            return self.frames

frame_streamer = FrameStreamer()

def generate_frames():
    while True:
        frame = frame_streamer.get_frame()

        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return send_file('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
