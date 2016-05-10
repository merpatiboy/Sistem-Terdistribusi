__author__ = 'DickyIrwanto'
import os

# contents of: remotecmd.py
def simple(arg):
    return arg + 1

def listdir(path):
    return os.listdir(path)

if __name__ == '__channelexec__':
    for item in channel:
        print item
        channel.send(eval(item))