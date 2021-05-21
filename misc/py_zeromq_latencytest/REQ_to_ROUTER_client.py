#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import time

counter = 0
time_sum = 0
time1 = 0.0
time2 = 0.0


context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
while True:
    print("Sending request ...")

    time1 = time.time_ns()
    socket.send(b"!")

    #  Get the reply.
    message = socket.recv()
    time2 = time.time_ns()
    # calculation of mean value
    counter += 1
    dt_us = (time2 - time1) / 1000.0
    time_sum += dt_us
    print("Times: ", time1, time2, dt_us)
    print(
        "ZMQ: sent: ! received: ",
        message,
        " in ",
        dt_us,
        " µs, mean: ",
        time_sum /
        counter)
    time.sleep(0.5)
    print("Received reply [ %s ]" % message)