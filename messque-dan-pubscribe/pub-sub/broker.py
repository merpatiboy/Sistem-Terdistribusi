__author__ = 'DickyIrwanto'
import zmq
from threading import Thread

global sockets
sockets = []

def create_streamer(context, pull_ip, push_ip):

    pusher = context.socket(zmq.PUB)
    push_bind = "tcp://*:%d" % (push_ip)
    print("Bind publisher on %s" % (push_bind))
    pusher.bind(push_bind)

    puller = context.socket(zmq.SUB)
    pull_bind = "tcp://*:%d" % (pull_ip)
    print("Bind subscriber on %s" % (pull_bind))
    puller.bind(pull_bind)
    puller.setsockopt(zmq.SUBSCRIBE, "")

    sockets.append(pusher)
    sockets.append(puller)
    zmq.device(zmq.FORWARDER, puller, pusher)

if __name__ == "__main__":
    try:
        context = zmq.Context()

        create_streamer(context, 5060, 5070)
    except Exception as e:
        print(e)
        print("Shutdown streamer")
    finally:
        for socket in sockets:
            socket.close()
        context.term()
