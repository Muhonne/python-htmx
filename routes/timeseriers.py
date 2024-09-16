from flask import Blueprint, jsonify
import json
import os
from datetime import datetime, timedelta

timeseries_bp = Blueprint('timeseries', __name__)
def get_timeseries_data():
    file_path = os.path.join(os.path.dirname(__file__), '../timeseries_data.json')

    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "Could not find file"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Could not parse file"}), 500


@timeseries_bp.route('/api/timeseries/latest', methods=['GET'])
def get_latest_timeseries_data():
    data=get_timeseries_data()[0]

    response = f"<p>BPM: {data['breathsPerMinute']}</p>"
    response += f"<p>HRV: {data['hrv']}</p>"
    response += f"<p>Heart Rate: {data['heartRate']}</p>"
    parsed_date = datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
    response += f"<p>Timestamp: {parsed_date}</p>"
    return response

    
@timeseries_bp.route('/api/timeseries/latesthour', methods=['GET'])
def get_last_hour_timeseries_data():
    data=get_timeseries_data()
    now = datetime.now()
    cutoff=now-timedelta(minutes=60)
    cutoff_index = 0
    for index, item in enumerate(data):
        item_datetime = datetime.strptime(item['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if item_datetime < cutoff:
            cutoff_index = index
            break
    
    last_hour_data = data[:cutoff_index]
    average_bpm = sum(item['breathsPerMinute'] for item in last_hour_data) / len(last_hour_data)
    average_hrv = sum(item['hrv'] for item in last_hour_data) / len(last_hour_data)
    average_heart_rate = sum(item['heartRate'] for item in last_hour_data) / len(last_hour_data)
    response = f"<p>BPM: {average_bpm}</p>"
    response += f"<p>HRV: {average_hrv}</p>"
    response += f"<p>Heart Rate: {average_heart_rate}</p>"
    parsed_date = datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
    response += f"<p>Timestamp: {parsed_date}</p>"
    return response
