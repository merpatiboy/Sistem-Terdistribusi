__author__ = 'DickyIrwanto'
import socket
import select
import sys
import Pyro4.core
import Pyro4.naming
import threading
import Pyro4
import re
server_ip = socket.gethostbyname(socket.gethostname())
server_port = 8888
global serveruri
serveruri = None
class EmbededServer(object):
    def checkData(self,data):
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

class threading_soc(threading.Thread):
    def __init__(self):
        print server_ip,server_port
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.sock.bind((server_ip,server_port))
        self.sock.listen(100)
        threading.Thread.__init__(self)
    def run(self):
        input_sock = [self]
        while 1:
            a,b,c = select.select(input_sock,[],[])
            if self in a:
                client,socket = self.sock.accept()
                req = client.recv(1024)
                if req == '1':
                    x = str(serveruri)
                    client.send(x)
                client.close()
    def fileno(self):
        return self.sock.fileno()

if __name__ == '__main__':
    Pyro4.config.SERVERTYPE='thread'
    hostname = socket.gethostname()
    nameserverUri, nameserverDaemon, broadcastServer = Pyro4.naming.startNS(host=hostname)
    pyrodaemon = Pyro4.core.Daemon(host=hostname)
    serveruri = pyrodaemon.register(EmbededServer())
    nameserverDaemon.nameserver.register('embeded.server',serveruri)
    print 'server uri', serveruri
    threading_soc().start()
    while 1:
        pyroSockets = set(pyrodaemon.sockets)
        nameserverSockets = set(nameserverDaemon.sockets)
        rs=[broadcastServer]  # only the broadcast server is directly usable as a select() object
        rs.extend(nameserverSockets)
        rs.extend(pyroSockets)
        rs,_,_ = select.select(rs,[],[],3)
        eventsForNameserver=[]
        eventsForDaemon=[]
        for s in rs:
            if s is broadcastServer:
                broadcastServer.processRequest()
            elif s in nameserverSockets:
                eventsForNameserver.append(s)
            elif s in pyroSockets:
                eventsForDaemon.append(s)
        if eventsForNameserver:
            nameserverDaemon.events(eventsForNameserver)
        if eventsForDaemon:
            pyrodaemon.events(eventsForDaemon)

    nameserverDaemon.close()
    broadcastServer.close()
    pyrodaemon.close()