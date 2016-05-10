__author__ = 'Dicky'
import re
from scoop import futures
import os
import time
def parse_log(content):
    matcher = re.compile('\[\d+\]: (.+?) (for|from)')
    while True:
        print("Got a job")
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

def get_data(path):
    file_counter = 0
    tasks = []
    results = []
    data_collector = dict()
    for file_name in os.listdir(path):
        if file_name.startswith("secure"):
            file_counter += 1
            logfile = open("%s/%s" % (path, file_name))
            tasks.append(logfile.read())
            logfile.close()
    results.append(list(futures.map(parse_log, tasks)))
    for result in results:
        for data in result:
            data_collector = receive_result(data_collector,data)
    return data_collector

def receive_result(all_result,datas):
    for data in datas:
        if data in all_result:
            all_result[data] += datas[data]
        else:
            all_result[data] = datas[data]
    return all_result

def main():
    path = 'tasks'
    task = futures.submit(get_data, path)
    futures.wait([task], return_when=futures.ALL_COMPLETED)
    result = task.result()
    sorted_result = sorted(result, key=result.__getitem__, reverse=True)
    for key in sorted_result:
        print("%s: %s" % (key, result[key]))
    return result

if __name__ == '__main__':
    start_time = time.time()
    main()
    print time.time()-start_time,'seconds'


