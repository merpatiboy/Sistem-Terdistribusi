__author__ = 'DickyIrwanto'
import zmq
import re
import os
import sys

def send_file(path, context):
    file_counter = 0
    for file_name in os.listdir(path):
        if file_name.startswith("secure"):
            file_counter += 1
            logfile = open("%s/%s" % (path, file_name))
            category_counter = parse_log(logfile.read())
            logfile.close()
            context.send_json(category_counter)
    return file_counter

def parse_log(content):
    matcher = re.compile('\[\d+\]: (.+?) (for|from)')
    category_counter = dict()
    matches = matcher.finditer(content)
    file_length = len(content.splitlines())
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

if __name__ == "__main__":
    log_path = sys.argv[1] if len(sys.argv) > 1 else "../../task"
    host = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"

    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.connect("tcp://%s:5060" % (host))
    print(send_file(log_path, publisher))

    publisher.close()
    context.term()