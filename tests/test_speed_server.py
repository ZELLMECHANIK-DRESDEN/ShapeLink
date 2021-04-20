#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import zmq
import time


@profile
def server_example():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("inproc://test")

    message = 'first'
    term_message = b'termi'
    while term_message != message:
        #  Wait for next request from client
        if message == 'first':
            # this check pretty much negates the need for time tracking below
            #  because in kernprof we can now see the first run separately
            message = socket.recv()
        else:
            message = socket.recv()
        #  Send reply back to client
        socket.send(b"hello")


t1 = time.time()
WAIT = 2  # seconds
t1_and_WAIT = t1 + WAIT

while t1 < t1_and_WAIT:
    t1 = time.time()
else:
    server_example()
