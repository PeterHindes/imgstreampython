import cv2
from flask import Flask, Response
# from flask_cors import CORS
from flask import make_response

app = Flask(__name__)
# CORS(app, origins="*")  # Allow requests from any origin


def generate_frames():
    cap = cv2.VideoCapture(cv2.CAP_ANY)
    print(cv2.CAP_ANY)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    response = Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
    # return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
