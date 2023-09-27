import os
from camera import Camera
from notifications import send_sms, get_api_key
from storage import list_videos_in_date_range, get_path
from flask_cors import CORS
from flask import Flask, jsonify, request


app = Flask(__name__)
CORS(app)

camera = Camera()


@app.route('/arm', methods=['POST'])
def arm():
    camera.arm()
    return jsonify(message="System armed."), 200


@app.route('/disarm', methods=['POST'])
def disarm():
    camera.disarm()
    return jsonify(message="System disarmed."), 200


@app.route('/get-armed', methods=['GET'])
def get_armed():
    return jsonify(armed=camera.armed), 200


@app.route('/motion_detected', methods=['POST'])
def motion_detected():
    data = request.get_json()

    if 'url' in data:
        print("URL: ", data['url'])
        recipients = [
            {
                "msidn": "2348066697348",  # Replace with recipient phone number
            },
        ]

        send_sms(recipients)
    else:
        print("'url' not in incoming data")

    return jsonify({}), 201


@app.route("/get-logs")
def get_logs():
    start_date = request.args.get("startDate")  # y-m-d
    end_date = request.args.get("endDate")  # y-m-d

    logs = list_videos_in_date_range(start_date, end_date)
    return jsonify({"logs": logs}), 200


@app.route("/video/<id>")
def get_video(id):
    return jsonify({"path": get_path(id)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
