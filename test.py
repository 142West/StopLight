import multiprocessing
import time

import RPi.GPIO as GPIO

LIGHTS = {"green": 11, "yellow": 13, "red": 15, }
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LIGHTS["green"], GPIO.OUT)
GPIO.setup(LIGHTS["yellow"], GPIO.OUT)
GPIO.setup(LIGHTS["red"], GPIO.OUT)

backProc = None

def runStopLight():
    print("Starting Stoplight")
    while True:
        GPIO.output(LIGHTS["green"], 1)
        GPIO.output(LIGHTS["yellow"], 0)
        GPIO.output(LIGHTS["red"], 0)
        time.sleep(1)
        GPIO.output(LIGHTS["green"], 0)
        GPIO.output(LIGHTS["yellow"], 1)
        GPIO.output(LIGHTS["red"], 0)
        time.sleep(1)
        GPIO.output(LIGHTS["green"], 0)
        GPIO.output(LIGHTS["yellow"], 0)
        GPIO.output(LIGHTS["red"], 1)
        time.sleep(1)


def api_startStoplight():
    global backProc
    backProc = multiprocessing.Process(target=runStopLight(), args=(), daemon=True)
    backProc.start()
    print(backProc)

def stop():
    backProc.terminate()
    print("stoped")


api_startStoplight()
time.sleep(5)
stop()

