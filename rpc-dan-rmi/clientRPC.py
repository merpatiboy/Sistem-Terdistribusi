__author__ = 'DickyIrwanto'
import xmlrpclib
import os
import threading
import time

#define global variable
global all_result
global all_task
global all_worker
all_result = dict()
#all task condition (data, flag{0,1,-1})
all_task = []
all_worker = []

class worker_Server(threading.Thread):
    def __init__(self,client_ip,client_port):
        self.client_ip = client_ip
        self.client_port = client_port
        threading.Thread.__init__(self)
    def run(self):
        connect_server(self.client_ip,self.client_port)


def connect_server(client_ip,client_port):
    while 1:
            url = 'http://'+client_ip +':'+client_port+'/'
            proxy = xmlrpclib.ServerProxy(url)
            flag = 0
            x = 0
            try:
                while x < len(all_task):
                    if all_task[x][1] == 0:
                        temp_task = list(all_task[x])
                        temp_task[1] = 1
                        all_task[x] = tuple(temp_task)
                        result = proxy.tambah(all_task[x][0])
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

def set_data(location):
    for r,d,f in os.walk(location):
        for file in f:
            file_ = open(location+'/'+file,'rb')
            data_file = file_.read()
            file_.close()
            all_task.append((data_file,0))

def combine_result(datas):
    for data in datas:
        if data in all_result:
            all_result[data] += datas[data]
        else:
            all_result[data] = 1

if __name__ == '__main__':
    all_worker.append(('localhost','8100'))
    all_worker.append(('localhost','8001'))
    set_data('task2')

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
    for key, value in sorted(all_result.iteritems(), key=lambda (k,v): (v,k),reverse=True):
        print "%s: %s" % (key, value)