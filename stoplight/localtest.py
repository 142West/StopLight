import multiprocessing
import time



backProc = None

def runStopLight():
    print("Starting Stoplight")
    while True:
        print("red")
        time.sleep(1)
        print("green")
        time.sleep(1)
        print("yellow")
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

