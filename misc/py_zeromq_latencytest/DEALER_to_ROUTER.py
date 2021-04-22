import zmq
import sys
import threading
import time
from random import randint



def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()

class ClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self, id):
        self.id = id
        threading.Thread.__init__ (self)
        self.counter = 0
        self.time_sum = 0
        self.time1 = 0.0
        self.time2 = 0.0

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        identity = u'worker-%d' % self.id
        socket.identity = identity.encode('ascii')
        socket.connect('tcp://localhost:5570')
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        reqs = 0
        while True:
            reqs = reqs + 1
            time1 = time.time_ns()
            socket.send_string("!")
            for i in range(5):
                sockets = dict(poll.poll(0))
                if socket in sockets:
                    ret = socket.recv()
                    time2 = time.time_ns()
                    self.counter += 1
                    dt_us = (time2 - time1) / 1000.0
                    self.time_sum += dt_us
                    print("Times: ", time1, time2, dt_us)
                    print(
                        "ZMQ: sent: ! received: ",
                        ret,
                        " in ",
                        dt_us,
                        " µs, mean: ",
                        self.time_sum /
                        self.counter)

        socket.close()
        context.term()

class ServerTask(threading.Thread):
    """ServerTask"""
    def __init__(self):
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind('tcp://*:5570')

        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        workers = []
        for i in range(5):
            worker = ServerWorker(context)
            worker.start()
            workers.append(worker)

        zmq.proxy(frontend, backend)

        frontend.close()
        backend.close()
        context.term()

class ServerWorker(threading.Thread):
    """ServerWorker"""
    def __init__(self, context):
        threading.Thread.__init__ (self)
        self.context = context

    def run(self):
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        # tprint('Worker started')
        while True:
            ident, msg = worker.recv_multipart()
            # tprint('Worker received %s from %s' % (msg, ident))
            replies = randint(0,4)
            for i in range(replies):
            #     time.sleep(1. / (randint(1,10)))
                worker.send_multipart([ident, msg])

        worker.close()


def main():
    """main function"""
    server = ServerTask()
    server.start()
    for i in range(3):
        client = ClientTask(i)
        client.start()

    server.join()


if __name__ == "__main__":
    main()