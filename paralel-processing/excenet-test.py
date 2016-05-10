__author__ = 'DickyIrwanto'
import execnet
import servefiles

gw = execnet.makegateway()
ch = gw.remote_exec(servefiles)
ch.send("listdir('c://')") # execute func-call remotely
x=ch.receive()
print x