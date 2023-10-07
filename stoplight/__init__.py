#!/usr/bin/python


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

app = FlaskAPI(__name__)


def runStopLight():
    print("Starting Stoplight")
    while True:
        GPIO.output(LIGHTS["green"], 0)
        GPIO.output(LIGHTS["yellow"], 1)
        GPIO.output(LIGHTS["red"], 1)
        time.sleep(3)
        GPIO.output(LIGHTS["green"], 1)
        GPIO.output(LIGHTS["yellow"], 0)
        GPIO.output(LIGHTS["red"], 1)
        time.sleep(3)
        GPIO.output(LIGHTS["green"], 1)
        GPIO.output(LIGHTS["yellow"], 1)
        GPIO.output(LIGHTS["red"], 0)
        time.sleep(3)


def shots(countDownTime, goTime):
    print("Shots!")
    # FUN FACT: 1 is off, 0 is on
    GPIO.output(LIGHTS["green"], 1)
    GPIO.output(LIGHTS["yellow"], 0)
    GPIO.output(LIGHTS["red"], 0)
    startTime = time.time()
    currentTime = time.time()
    while currentTime < int(countDownTime)-5.7:
        GPIO.output(LIGHTS["yellow"], 1)
        time.sleep(1)
        GPIO.output(LIGHTS["yellow"], 0)
        time.sleep(1)
        currentTime = startTime - time.time()

    while currentTime < int(countDownTime)-2.5:
        GPIO.output(LIGHTS["yellow"], 1)
        time.sleep(.5)
        GPIO.output(LIGHTS["yellow"], 0)
        time.sleep(.5)
        currentTime = startTime - time.time()

    while currentTime < int(countDownTime):
        GPIO.output(LIGHTS["yellow"], 1)
        time.sleep(.2)
        GPIO.output(LIGHTS["yellow"], 0)
        time.sleep(.2)
        currentTime = startTime - time.time()

    GPIO.output(LIGHTS["yellow"], 1)
    GPIO.output(LIGHTS["green"], 0)
    time.sleep(int(goTime))
    GPIO.output(LIGHTS["green"], 1)
    GPIO.output(LIGHTS["yellow"], 1)
    GPIO.output(LIGHTS["red"], 0)
    runStopLight()


@app.route('/', methods=["GET"])
def api_root():
    return {
        "led_url": request.url + "LIGHT/(mode)/",
        "led_url_POST": {"state": "(0 | 1)"}
    }


@app.route('/start', methods=["GET"])
def api_startStoplight():
    backProc = multiprocessing.Process(target=runStopLight, args=(), daemon=True)
    backProc.start()
    return 'started: ' + str(backProc.pid)


@app.route('/stop', methods=["GET"])
def api_stopStoplight():
    print("Stopping stoplight")
    GPIO.output(LIGHTS["green"], 1)
    GPIO.output(LIGHTS["yellow"], 1)
    GPIO.output(LIGHTS["red"], 1)
    backProc.terminate()
    return 'killed: ' + str(backProc.pid)


@app.route('/shots', methods=["GET"])
def api_shots():
    countDownTime = request.args.get("countDownTime")
    goTime = request.args.get("goTime")
    if backProc is not None:
        backProc.terminate()
    backProc = multiprocessing.Process(target=shots, args=(countDownTime, goTime), daemon=True)
    backProc.start()
    return 'started: ' + str(backProc.pid)


if __name__ == "__main__":
    app.run(use_reloader=False, host="0.0.0.0")
