from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/control", methods=["POST"])
def control():
    action = request.form.get("action")
    num_blinks = int(request.form.get("num_blinks", 0))

    if action == "on":
        GPIO.output(11, GPIO.HIGH)
    elif action == "off":
        GPIO.output(11, GPIO.LOW)
    elif action == "blink" and num_blinks > 0:
        for _ in range(num_blinks):
            GPIO.output(11, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(11, GPIO.LOW)
            time.sleep(0.5)

    return "Action performed successfully! <a href='/'>Go back</a>"

@app.route("/cleanup")
def cleanup():
    GPIO.cleanup()
    return "GPIO cleaned up. <a href='/'>Go back</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
