import RPi.GPIO as GPIO
import time

# Setup the GPIO pin for the servo
servo_pin = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Setup PWM process
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz (20 ms PWM period)

# Start PWM by rotating to 90 degrees
pwm.start(7)

try:
    # Clockwise motion
    print("Clockwise Motion:")
    for ii in range(2, 13):  # Increment duty cycle from 2.0 to 12.0
        pwm.ChangeDutyCycle(ii)  # Rotate to specified angle
        print(f"Duty Cycle: {ii}")
        time.sleep(1)

    # Anticlockwise motion
    print("\nAnticlockwise Motion:")
    for ii in range(12, 1, -1):  # Decrement duty cycle from 12.0 to 2.0
        pwm.ChangeDutyCycle(ii)  # Rotate to specified angle
        print(f"Duty Cycle: {ii}")
        time.sleep(1)

finally:
    # Prevent jitter and cleanup
    pwm.ChangeDutyCycle(0)  # Stop PWM signal
    pwm.stop()  # Stop PWM
    GPIO.cleanup()  # Clean up GPIO
    print("\nProgram finished, GPIO cleaned up.")
