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
from threading import Thread, Event
import requests
import time


link_AHU1_AHU2_intake_supply = 'http://172.19.6.231/kbr/?pt=31&cmd=list'
link_AHU4_AHU3_intake_supply = 'http://172.19.6.231/kbr/?pt=30&cmd=list'
link_AHU2_3_4_mid = 'http://172.19.6.231/kbr/?pt=32&cmd=list'

AHU2_mid = "aaeb5c1a1302"
AHU3_mid = "89ab10301401"
AHU4_mid = "aa45ba1a1302"

AHU4_supply = "aa16691a1302"
AHU4_intake = "aa85b61a1302"
AHU3_supply = "aad0cc1a1302"
AHU3_intake = "fc546f2f1401"
AHU2_supply = "05b910301401"
AHU2_intake = "2ebabe2f1401"
AHU1_supply = "dc1d532f1401"
AHU1_intake = "aa89c61a1302"

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
    # global thread
    print('Client connected')

    # #Start the random number generator thread only if the thread has not been started before.
    # if not thread.isAlive():
    #     print("Starting Thread")
    #     thread = RandomThread()
    #     thread.start()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


def get_raw_devices_data(link, delay, time_out):
    if delay != 0:
        print("delay start. delay", delay)
        time.sleep(delay)
    print("delay end")
    try:
        r = requests.get(link, timeout=time_out)
        return r.text
    except requests.exceptions.Timeout:
        print("Timeout during calling ", link)
        return None

if __name__ == '__main__':
    # socketio.run(app)

    raw_data = get_raw_devices_data(link_AHU1_AHU2_intake_supply, 0, 5)
    print("link_AHU1_AHU2_intake_supply=", raw_data)
    if raw_data == None:
        raw_data = get_raw_devices_data(link_AHU1_AHU2_intake_supply, 0, 5)
        print("second call link_AHU1_AHU2_intake_supply=",raw_data)
    # parsing

    raw_data = get_raw_devices_data(link_AHU4_AHU3_intake_supply, 5, 5)
    print("link_AHU4_AHU3_intake_supply=", raw_data)
    if raw_data == None:
        raw_data = get_raw_devices_data(link_AHU4_AHU3_intake_supply, 5, 5)
        print("second call link_AHU4_AHU3_intake_supply=", raw_data)
    # parsing

    raw_data = get_raw_devices_data(link_AHU2_3_4_mid, 5, 5)
    print("link_AHU2_3_4_mid=", raw_data)
    if raw_data == None:
        raw_data = get_raw_devices_data(link_AHU2_3_4_mid, 5, 5)
        print("second call link_AHU2_3_4_mid=", raw_data)
    print("hi")
