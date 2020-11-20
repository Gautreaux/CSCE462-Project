testPin = 11

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(testPin, GPIO.OUT)

GPIO.output(testPin, GPIO.HIGH)

try:
    while True:
        GPIO.output(testPin, GPIO.HIGH)
        sleep(1)
        GPIO.output(testPin, GPIO.LOW)
        sleep(1)
finally:
    GPIO.output(testPin, GPIO.LOW)