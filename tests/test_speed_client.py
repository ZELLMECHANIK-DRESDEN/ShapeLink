#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import time


@profile
def client_example():
    context = zmq.Context()
    #  Socket to talk to server
    socket = context.socket(zmq.REQ)
    socket.connect("inproc://test")

    # for speed consistency set these here too
    message = ''
    term_message = b'termi'
    #  Do n requests, waiting each time for a response
    for request in range(1000):
        socket.send(b"hello")
        # Get the reply.
        socket.recv()
    socket.send(b'termi')


t1 = time.time()
WAIT = 2  # seconds
t1_and_WAIT = t1 + WAIT

while t1 < t1_and_WAIT:
    t1 = time.time()
else:
    client_example()

# kernprof -l -v tests\test_speed_client.py
# kernprof -l -v tests\test_speed_server.py