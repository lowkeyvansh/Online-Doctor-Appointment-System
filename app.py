from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['doctor_appointment']
doctors_collection = db['doctors']
patients_collection = db['patients']
appointments_collection = db['appointments']

@app.route('/doctors', methods=['POST'])
def add_doctor():
    doctor = request.json
    doctors_collection.insert_one(doctor)
    return jsonify({'msg': 'Doctor added'}), 201

@app.route('/patients', methods=['POST'])
def add_patient():
    patient = request.json
    patients_collection.insert_one(patient)
    return jsonify({'msg': 'Patient added'}), 201

@app.route('/appointments', methods=['POST'])
def book_appointment():
    appointment = request.json
    appointment['appointment_date'] = datetime.strptime(appointment['appointment_date'], '%Y-%m-%d %H:%M')
    appointments_collection.insert_one(appointment)
    return jsonify({'msg': 'Appointment booked'}), 201

@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = list(appointments_collection.find({}, {'_id': 0}))
    return jsonify(appointments)

if __name__ == '__main__':
    app.run(debug=True)
