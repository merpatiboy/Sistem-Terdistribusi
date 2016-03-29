__author__ = 'DickyIrwanto'

import os
import zmq
import threading
import pickle
import time

global all_task
global all_worker
global all_result

all_result = dict()
all_task = []
all_worker = []

context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

def set_data(location):
    for r,d,f in os.walk(location):
        for file in f:
            file_ = open(location+'/'+file,'rb')
            data_file = file_.read()
            file_.close()
            all_task.append((data_file,0))

class worker_Server(threading.Thread):
    def __init__(self,client_ip,client_port):
        self.client_ip = client_ip
        self.client_port = client_port
        threading.Thread.__init__(self)
    def run(self):
        connect_server(self.client_ip,self.client_port)

def connect_server(client_ip,client_port):
    while 1:
        sender = context.socket(zmq.PUSH)
        sender.connect("tcp://"+client_ip+":"+client_port)
        flag = 0
        x = 0
        try:
            while x < len(all_task):
                if all_task[x][1] == 0:
                    temp_task = list(all_task[x])
                    temp_task[1] = 1
                    all_task[x] = tuple(temp_task)
                    mess = pickle.dumps(all_task[x][0])
                    sender.send(mess)
                    result = pickle.loads(receiver.recv())
                    combine_result(result)
                    temp_task = list(all_task[x])
                    temp_task[1] = -1
                    all_task[x] = tuple(temp_task)
                elif all_task[x][1] == -1:
                    flag += 1
                x += 1
            if flag == len(all_task):
                break
        except:
            temp_task = list(all_task[x])
            temp_task[1] = 0
            all_task[x] = tuple(temp_task)
            print 'Error to Connect',client_ip,':',client_port
            time.sleep(5)

def combine_result(datas):
    for data in datas:
        if data in all_result:
            all_result[data] += datas[data]
        else:
            all_result[data] = datas[data]

def mode_1():
    start_time  = time.time()
    all_worker.append(('localhost','5557'))
    for worker in all_worker:
        sender = context.socket(zmq.PUSH)
        sender.connect("tcp://"+worker[0]+":"+worker[1])
        sender.send('start')
    while True:
        mess = receiver.recv()
        if mess == 'end':
            break
        else:
            mess = pickle.loads(mess)
            combine_result(mess)
    print 'execution time: ', (time.time()-start_time), 'seconds'
    for key, value in sorted(all_result.iteritems(), key=lambda (k,v): (v,k),reverse=True):
        print "%s: %s" % (key, value)

def mode_2():
    start_time  = time.time()
    all_worker.append(('localhost','5557'))
    set_data('task')
    for worker in all_worker:
       worker_Server(worker[0],worker[1]).start()

    while 1:
        flag = 0
        for x in range(0,len(all_task)):
            if all_task[x][1] == -1:
                flag += 1

        if flag == len(all_task):
            print 'all task has done'
            break

    print 'execution time: ', (time.time()-start_time), 'seconds'
    for key, value in sorted(all_result.iteritems(), key=lambda (k,v): (v,k),reverse=True):
        print "%s: %s" % (key, value)

if __name__ == '__main__':
    _ = raw_input('Masukkan Mode:')
    if _ == '1':
        mode_1()

    elif _ == '2':
        mode_2()