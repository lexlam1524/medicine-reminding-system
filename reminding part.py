import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

broker_address = "broker.emqx.io"  
broker_port = 1883  
topic = "SIT210/medicine"
buzzer_pin = 17

# Setup GPIO
GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.output(buzzer_pin, GPIO.LOW)

# Callback function for MQTT message received
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print("Received message: " + payload)

    if payload == "turn_on_buzzer":
        GPIO.output(buzzer_pin, GPIO.HIGH)
        print("Buzzer turned on")
    elif payload == "detected action":
        GPIO.output(buzzer_pin, GPIO.LOW)
        print("Buzzer turned off")

# Create MQTT client and connect to the broker
client = mqtt.Client("rpi_device")
client.connect(broker_address, broker_port)

# Set the message callback function
client.on_message = on_message

# Subscribe to the MQTT topic
client.subscribe(topic)

# Start the MQTT loop to process incoming messages
client.loop_start()

try:
    while True:
        # Continue the main program execution
        time.sleep(1)

except KeyboardInterrupt:
    # Clean up GPIO and disconnect from MQTT broker on program exit
    GPIO.output(buzzer_pin, GPIO.LOW)
    client.disconnect()
    client.loop_stop()
    GPIO.cleanup()