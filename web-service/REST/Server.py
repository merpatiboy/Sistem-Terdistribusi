__author__ = 'DickyIrwanto'

from flask import Flask,json,request,jsonify
import sys,os,re,operator

app = Flask(__name__)
all_task = []

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }
    resp = jsonify(message)
    return resp

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/security/', methods = ['GET'])
def security():
    result = dict()
    for data in all_task:
        result = combine_result(checkData(data),result)
    result = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    result = json.dumps(result)
    return result

def set_data(location):
    for r,d,f in os.walk(location):
        for file in f:
            file_ = open(location+'/'+file,'rb')
            data_file = file_.read()
            file_.close()
            all_task.append(data_file)


def combine_result(datas,all_result):
    for data in datas:
        if data in all_result:
            all_result[data] += datas[data]
        else:
            all_result[data] = datas[data]
    return all_result

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

if __name__ == '__main__':
    host = "127.0.0.1"
    location = '../task/'

    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        location = sys.argv[2]
    set_data(location)
    app.run(debug=True)