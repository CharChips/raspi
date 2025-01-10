from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
import time

# Initialize Flask app
app = Flask(__name__)

# Setup the GPIO pin for the servo
servo_pin = 3
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)

# Setup PWM process
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz (20 ms PWM period)
pwm.start(7)  # Start PWM by rotating to 90 degrees
duty_cycle = 7  # Initial duty cycle


@app.route("/")
def home():
    return render_template("index.html", duty_cycle=duty_cycle)


@app.route("/rotate", methods=["POST"])
def rotate():
    global duty_cycle

    # Parse JSON data
    data = request.json
    action = data.get("action")

    # Adjust duty cycle based on action
    if action == "left" and duty_cycle < 12:
        duty_cycle += 1
    elif action == "right" and duty_cycle > 2:
        duty_cycle -= 1

    # Change the servo's duty cycle
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Allow time for the servo to move
    pwm.ChangeDutyCycle(0)  # Stop PWM signal to prevent jitter

    # Respond with updated duty cycle
    return jsonify({"duty_cycle": duty_cycle})


@app.route("/cleanup", methods=["POST"])
def cleanup():
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.cleanup()
    return "GPIO cleaned up. Stop the server to finalize."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Allow access from any device on the same network
