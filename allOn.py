import time

from flask import request
from flask_api import FlaskAPI
import multiprocessing
import RPi.GPIO as GPIO

backProc = None
LIGHTS = {"green": 11, "yellow": 13, "red": 15, }
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LIGHTS["green"], GPIO.OUT)
GPIO.setup(LIGHTS["yellow"], GPIO.OUT)
GPIO.setup(LIGHTS["red"], GPIO.OUT)


GPIO.output(LIGHTS["green"], 0)
GPIO.output(LIGHTS["yellow"], 0)
GPIO.output(LIGHTS["red"], 0)
while True:
    pass