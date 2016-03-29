__author__ = 'DickyIrwanto'
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import re

def add(data):
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

server  = SimpleXMLRPCServer(('localhost',8100))
server.register_function(add,'tambah')
server.serve_forever()
