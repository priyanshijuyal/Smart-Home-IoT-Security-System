from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mqtt import Mqtt

app = Flask(__name__)

# MQTT Configuration
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 60
mqtt = Mqtt(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# MQTT Callbacks
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    mqtt.subscribe("home/#")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = message.payload.decode()
    sensor_type = "Motion" if "motion" in message.topic else "Temp/Humid"
    new_data = SensorData(type=sensor_type, value=data)
    db.session.add(new_data)
    db.session.commit()
    print(f"New data saved: {data}")

# Routes
@app.route('/')
def home():
    data = SensorData.query.all()
    return render_template('dashboard.html', sensor_data=data)

@app.route('/api/data', methods=['GET'])
def get_sensor_data():
    data = SensorData.query.all()
    result = [{"type": d.type, "value": d.value, "timestamp": d.timestamp} for d in data]
    return jsonify(result)

@app.route('/api/register', methods=['POST'])
def register_user():
    # Mock API endpoint for user registration
    data = request.json
    return jsonify({"message": "User registered successfully", "data": data})

@app.route('/api/login', methods=['POST'])
def login_user():
    # Mock API endpoint for user login
    data = request.json
    return jsonify({"message": "Login successful", "data": data})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
