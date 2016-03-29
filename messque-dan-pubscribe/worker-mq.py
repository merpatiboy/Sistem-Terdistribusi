__author__ = 'DickyIrwanto'

import os
import zmq
import re
import pickle

all_task = []

def checkData(data):
    lines = data.split('\n')
    category_counter = dict()
    matcher = re.compile('\[\d+\]: (.+?) (for|from)')
    matches = matcher.finditer(data)
    file_length = len(data.splitlines())
    matches_length = 0
    for match in matches:
        matches_length += 1
        key_string = ''
        if match.group(2) == 'for':
            key_string = match.group(1)
        else:
            separated_string = match.group(1).split(' ')
            if len(separated_string) > 1:
                key_string = (' ').join(separated_string[:-1])
            else:
                key_string = separated_string[0]
            if key_string in category_counter:
                category_counter[key_string] += 1
            else:
                category_counter[key_string] = 1
    category_counter["Unidentified"] = file_length - matches_length

    return category_counter

def set_data(location):
    for r,d,f in os.walk(location):
        for file in f:
            file_ = open(location+'/'+file,'rb')
            data_file = file_.read()
            file_.close()
            all_task.append((data_file,0))

def mode_1():
    set_data('task')
    while True:
        s = receiver.recv()
        if s != '':
            for task in all_task:
                result = checkData(task[0])
                result =pickle.dumps(result)
                sender.send(result)
            break

    sender.send('end')

def mode_2():
    while True:
        s = receiver.recv()
        if s != '' and s != 'end':
            s = pickle.loads(s)
            s = checkData(s)
            s = pickle.dumps(s)
            sender.send(s)
        elif s == 'end':
            break

context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5557")
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558")
if __name__ == '__main__':
    _  = raw_input('Masukkan Mode:')
    if _ == '1':
        mode_1()
    elif _ == '2':
        mode_2()

