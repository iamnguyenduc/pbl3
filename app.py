from flask import Flask, render_template, request, jsonify, redirect, url_for
import paho.mqtt.client as mqtt
import threading
import logging
import time

app = Flask(__name__)

broker_address = 'broker.emqx.io'
broker_port = 1883
topic_sensor = 'sensor'
topic_led = 'led'

# Initialize sensor_data with an initial value
sensor_data = "No data"
sensor_data_lock = threading.Lock()  # Lock to ensure thread safety

# Configure logging to prevent printing messages to console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MQTT Callback functions
def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code " + str(rc))
    client.subscribe(topic_sensor)

def on_message(client, userdata, msg):
    global sensor_data
    logger.info(msg.topic + " " + str(msg.payload, 'utf-8'))
    with sensor_data_lock:
        sensor_data = str(msg.payload, 'utf-8')

# Create MQTT client and set callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, broker_port, 60)
client.loop_start()

# Function to update sensor_data every second
def update_sensor_data():
    global sensor_data
    while True:
        time.sleep(0.1)
        # You should fetch data from the MQTT topic here
        # For simplicity, let's assume data is stored in a variable called 'data'
        with sensor_data_lock:
            # Replace the next line with your actual logic to fetch data from the MQTT topic
            mqtt_data = sensor_data  # Replace with your actual logic
            sensor_data = str(mqtt_data)

# Start the thread for updating sensor_data
update_thread = threading.Thread(target=update_sensor_data)
update_thread.daemon = True
update_thread.start()

# Routes
@app.route('/')
def index():
    # Return the actual sensor data to be displayed on the web page
    with sensor_data_lock:
        return render_template('index.html', sensor_data=sensor_data)

@app.route('/send_led_message', methods=['POST'])
def send_led_message():
    # Get message from the form
    led_message = request.form['led_message']

    # Publish the message to the MQTT topic "led"
    client.publish(topic_led, led_message)

    return redirect(url_for('index'))

# Route to get sensor data as JSON
@app.route('/get_sensor_data')
def get_sensor_data():
    global sensor_data
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(debug=True)
