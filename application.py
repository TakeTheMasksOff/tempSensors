"""
Demo Flask application to test the operation of Flask with socket.io

Aim is to create a webpage that is constantly updated with random numbers from a background python process.

30th May 2014

===================

Updated 13th April 2018

+ Upgraded code to Python 3
+ Used Python3 SocketIO implementation
+ Updated CDN Javascript and CSS sources

"""


# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
# from threading import Thread, Event
import threading
import requests
import datetime
import json

link_AHU1_AHU2_intake_supply_AHU1_mid = 'http://172.19.6.231/kbr/?pt=31&cmd=list'
link_AHU4_AHU3_intake_supply = 'http://172.19.6.231/kbr/?pt=30&cmd=list'
link_AHU2_3_4_mid = 'http://172.19.6.231/kbr/?pt=32&cmd=list'
link_outside = "http://172.19.6.231/kbr/?pt=33&cmd=list"

map_obj = {
    "a43f8f2f1401": "device_outside" ,
    "aaabe9191302": "AHU1_mid" ,
    "aaeb5c1a1302": "AHU2_mid",
    "89ab10301401": "AHU3_mid",
    "aa45ba1a1302": "AHU4_mid",
    "aa16691a1302": "AHU4_supply",
    "aa85b61a1302": "AHU4_intake",
    "aad0cc1a1302": "AHU3_supply" ,
    "fc546f2f1401": "AHU3_intake" ,
    "05b910301401": "AHU2_supply" ,
    "2ebabe2f1401": "AHU2_intake" ,
    "dc1d532f1401": "AHU1_supply",
    "aa89c61a1302": "AHU1_intake"
}

temps_obj = {
    "device_outside": 1,
    "AHU4_mid": 1,
    "AHU4_supply": 1,
    "AHU4_intake": 1,
    "AHU3_mid": 1,
    "AHU3_supply": 1,
    "AHU3_intake": 1,
    "AHU2_mid": 1,
    "AHU2_supply": 1,
    "AHU2_intake": 1,
    "AHU1_mid": 1,
    "AHU1_supply": 1,
    "AHU1_intake": 1
}

__author__ = 'TakeTheMasksOff'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

# #random number Generator Thread
# thread = Thread()
# thread_stop_event = Event()

# class RandomThread(Thread):
#     def __init__(self):
#         self.delay = 1
#         super(RandomThread, self).__init__()

#     def randomNumberGenerator(self):
#         """
#         Generate a random number every 1 second and emit to a socketio instance (broadcast)
#         Ideally to be run in a separate thread?
#         """
#         #infinite loop of magical random numbers
#         print("Making random numbers")
#         while not thread_stop_event.isSet():
#             number = round(random()*10, 3)
#             print(number)
#             socketio.emit('newnumber', {'number': number}, namespace='/test')
#             sleep(self.delay)

#     def run(self):
#         self.randomNumberGenerator()


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    # global threading
    print('Client connected')
    # #Start the random number generator thread only if the thread has not been started before.
    # if not thread.isAlive():
    #     print("Starting Thread")
    #     thread = RandomThread()
    #     thread.start()

    printit()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


def printit():
        threading.Timer(60, printit).start()
        init_transfer_obj()
        js_string = collect_data()
        print("json obj type=", type(js_string))
        print("json obj to send=", js_string)
        socketio.emit('sensors', js_string, namespace='/test')
        print("iteration end time", datetime.datetime.now().strftime("%c"))

def get_raw_devices_data(link, delay, time_out):
    if delay != 0:
        print("starts with delay=", delay)
        sleep(delay)
    else:
        print("starts without delay")
    try:
        r = requests.get(link, timeout=time_out)
        return r.text
    except requests.exceptions.Timeout:
        print("Timeout during calling ", link)
        return None


def collect_data():
    print("iteration start time", datetime.datetime.now().strftime("%c"))
    raw_data = get_raw_devices_data(
        link_AHU1_AHU2_intake_supply_AHU1_mid, 0, 5)
    print("link_AHU1_AHU2_intake_supply_AHU1_mid=", raw_data)
    if raw_data == None:
        raw_data = get_raw_devices_data(
            link_AHU1_AHU2_intake_supply_AHU1_mid, 0, 5)
        print("second call link_AHU1_AHU2_intake_supply_AHU1_mid=", raw_data)
    parse_from_device(raw_data)

    raw_data = get_raw_devices_data(link_AHU4_AHU3_intake_supply, 5, 5)
    print("link_AHU4_AHU3_intake_supply=", raw_data)
    if raw_data == None:
        raw_data = get_raw_devices_data(link_AHU4_AHU3_intake_supply, 5, 5)
        print("second call link_AHU4_AHU3_intake_supply=", raw_data)
    parse_from_device(raw_data)

    raw_data = get_raw_devices_data(link_AHU2_3_4_mid, 5, 5)
    print("link_AHU2_3_4_mid=", raw_data)
    if raw_data == None:
        raw_data = get_raw_devices_data(link_AHU2_3_4_mid, 5, 5)
        print("second call link_AHU2_3_4_mid=", raw_data)
    parse_from_device(raw_data)

    raw_data = get_raw_devices_data(link_outside, 5, 5)
    print("link_outside=", raw_data)
    if raw_data == None:
        raw_data = get_raw_devices_data(link_outside, 5, 5)
        print("second call link_outside=", raw_data)
    parse_from_device(raw_data)
    js_string = json.dumps(temps_obj)
    
    return js_string
    


def parse_from_device(raw_data):
    if raw_data:
        partial_devices_data = raw_data.split(";")
        print("separated data=", partial_devices_data)
        for sensor_data in partial_devices_data:
            sensor = sensor_data.split(":")
            print("sensor=", sensor)
            if sensor[0] in map_obj:
                key = map_obj[sensor[0]]
                print("key=", key)
                if sensor[1]:
                    temps_obj[key] = sensor[1]

def init_transfer_obj():
    for key in temps_obj:
        temps_obj[key] = None
    print("temps_obj=", temps_obj)

if __name__ == '__main__':
    socketio.run(app)
