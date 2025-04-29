from flask import Blueprint, request, jsonify
from app.models import Sensor
from app import db

api = Blueprint('api', __name__)


@api.route('/sensors', methods=['POST'])
def add_sensor():
    data = request.get_json()
    if not data or 'name' not in data or 'location' not in data:
        return jsonify({'error': 'Missing name or location'}), 400

    sensor = Sensor(name=data['name'], location=data['location'])
    db.session.add(sensor)
    db.session.commit()
    return jsonify(sensor.to_dict()), 201


@api.route('/sensors', methods=['GET'])
def get_sensors():
    sensor_id = request.args.get('id')
    location = request.args.get('location')

    if sensor_id:
        sensor = Sensor.query.get(sensor_id)
        return jsonify(sensor.to_dict()) if sensor else (jsonify({'error': 'Sensor not found'}), 404)
    elif location:
        sensors = Sensor.query.filter_by(location=location).all()
        return jsonify([s.to_dict() for s in sensors])
    else:
        return jsonify({'error': 'Provide ID or location'}), 400


@api.route('/sensors/<int:id>', methods=['PUT'])
def update_sensor(id):
    sensor = Sensor.query.get(id)
    if not sensor:
        return jsonify({'error': 'Sensor not found'}), 404

    data = request.get_json()
    sensor.name = data.get('name', sensor.name)
    sensor.location = data.get('location', sensor.location)
    db.session.commit()
    return jsonify(sensor.to_dict())


@api.route('/sensors/<int:id>', methods=['DELETE'])
def delete_sensor(id):
    sensor = Sensor.query.get(id)
    if not sensor:
        return jsonify({'error': 'Sensor not found'}), 404

    db.session.delete(sensor)
    db.session.commit()
    return jsonify({'message': 'Sensor deleted'}), 200