from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from time import sleep
import threading
import requests
import datetime
import json

link_AHU1_AHU2_intake_supply_AHU1_mid = 'http://172.19.6.231/kbr/?pt=31&cmd=list'
link_AHU4_AHU3_intake_supply = 'http://172.19.6.231/kbr/?pt=30&cmd=list'
link_AHU4_mid = 'http://172.19.6.231/kbr/?pt=32&cmd=list'
link_AHU2_mid = 'http://172.19.6.231/kbr/?pt=34&cmd=list'
link_AHU3_mid = 'http://172.19.6.231/kbr/?pt=35&cmd=list'
link_outside = "http://172.19.6.231/kbr/?pt=33&cmd=list"

map_obj = {
    "a43f8f2f1401": "device_outside",
    "aaabe9191302": "AHU1_mid",
    "aaeb5c1a1302": "AHU2_mid",
    "89ab10301401": "AHU3_mid",
    "aa45ba1a1302": "AHU4_mid",
    "aa16691a1302": "AHU4_supply",
    "aa85b61a1302": "AHU4_intake",
    "aad0cc1a1302": "AHU3_supply",
    "fc546f2f1401": "AHU3_intake",
    "05b910301401": "AHU2_supply",
    "2ebabe2f1401": "AHU2_intake",
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

# turn the flask app into a socketio app
socketio = SocketIO(app)
client_count = 0

@app.before_first_request
def start_requesting_sensors():
    
    print("client_count=", client_count)
    print("############################# STARTING SCHEDULE  #############################")
    my_schedule()


@app.route('/')
def index():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Client connected^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print("connection time", datetime.datetime.now().strftime("%c"))
    global client_count
    client_count += 1
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Total client count = ', client_count)
    


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Client disconnected^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print("disconnection time", datetime.datetime.now().strftime("%c"))
    global client_count
    client_count -= 1
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Total client count = ', client_count)


def my_schedule():
    print("*********************************")
    print("iteration start time", datetime.datetime.now().strftime("%c"))
    init_transfer_obj()
    js_string = collect_data()
    print("json obj to send=", js_string)
    socketio.emit('sensors', js_string, namespace='/test')
    print("iteration end time", datetime.datetime.now().strftime("%c"))
    print("=================================")
    threading.Timer(30, my_schedule).start()


def init_transfer_obj():
    for key in temps_obj:
        temps_obj[key] = None
    print("temps_obj=", temps_obj)


def collect_data():
    raw_data = get_raw_devices_data(link_AHU1_AHU2_intake_supply_AHU1_mid, 0, 5)
    print("link_AHU1_AHU2_intake_supply_AHU1_mid=", raw_data)
    if raw_data == None:
        raw_data = get_raw_devices_data(link_AHU1_AHU2_intake_supply_AHU1_mid, 5, 5)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  second call link_AHU1_AHU2_intake_supply_AHU1_mid=", raw_data)
    parse_from_device(raw_data)

    raw_data = get_raw_devices_data(link_AHU4_AHU3_intake_supply, 2, 5)
    print("link_AHU4_AHU3_intake_supply=", raw_data)
    if raw_data == None:
        raw_data = get_raw_devices_data(link_AHU4_AHU3_intake_supply, 5, 5)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  second call link_AHU4_AHU3_intake_supply=", raw_data)
    parse_from_device(raw_data)

    raw_data = get_raw_devices_data(link_AHU4_mid, 2, 5)
    print("link_AHU4_mid=", raw_data)
    if raw_data == None:
        raw_data = get_raw_devices_data(link_AHU4_mid, 5, 5)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  second call link_AHU4_mid=", raw_data)
    parse_from_device(raw_data)

    raw_data = get_raw_devices_data(link_AHU3_mid, 2, 5)
    print("link_AHU3_mid=", raw_data)
    if raw_data == None:
        raw_data = get_raw_devices_data(link_AHU3_mid, 5, 5)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  second call link_AHU3_mid=", raw_data)
    parse_from_device(raw_data)

    raw_data = get_raw_devices_data(link_AHU2_mid, 2, 5)
    print("link_AHU2_mid=", raw_data)
    if raw_data == None:
        raw_data = get_raw_devices_data(link_AHU2_mid, 5, 5)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  second call link_AHU2_mid=", raw_data)
    parse_from_device(raw_data)

    raw_data = get_raw_devices_data(link_outside, 2, 5)
    print("link_outside=", raw_data)
    if raw_data == None:
        raw_data = get_raw_devices_data(link_outside, 5, 5)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  second call link_outside=", raw_data)
    parse_from_device(raw_data)
    js_string = json.dumps(temps_obj)

    return js_string


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


if __name__ == '__main__':
    socketio.run(app)
