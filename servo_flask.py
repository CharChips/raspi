from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time

# Initialize Flask app
app = Flask(__name__)

# Setup the GPIO pin for the servo
servo_pin = 13
GPIO.setmode(GPIO.BCM)
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

    # Check the action
    action = request.form.get("action")
    if action == "increment" and duty_cycle < 12:
        duty_cycle += 1
    elif action == "decrement" and duty_cycle > 2:
        duty_cycle -= 1

    # Change the servo's duty cycle
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Allow time for the servo to move
    pwm.ChangeDutyCycle(0)  # Stop PWM signal to prevent jitter

    return render_template("index.html", duty_cycle=duty_cycle)


@app.route("/cleanup", methods=["POST"])
def cleanup():
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.cleanup()
    return "GPIO cleaned up. Stop the server to finalize."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Allow access from any device on the same network
