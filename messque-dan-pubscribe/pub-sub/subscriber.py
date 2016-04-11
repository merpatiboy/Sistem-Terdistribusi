__author__ = 'DickyIrwanto'
import zmq
import sys

if __name__ == "__main__":
    context = zmq.Context()
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"

    print(host)
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://%s:5070" % (host))
    subscriber.setsockopt(zmq.SUBSCRIBE, "")

    category_couter = dict()

    result = subscriber.recv_json()
    for key, value in result.items():
        if key in category_couter:
            category_couter[key] += value
        else:
            category_couter[key] = value

    sorted_result = sorted(category_couter, key=category_couter.__getitem__, reverse=True)
    for key in sorted_result:
            print("%s: %s" % (key, category_couter[key]))