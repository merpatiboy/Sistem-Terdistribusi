__author__ = 'DickyIrwanto'

'''
    Special thanks: http://bayo.opadeyi.net/2013/10/simple-soap-service-with-pysimplesoap.html
'''

from pysimplesoap.server import SoapDispatcher, WSGISOAPHandler
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import re,os,sys,operator

all_task = []
host = "127.0.0.1"
location = '../task/'

def security():
    result = dict()
    result_last = ''
    for data in all_task:
        result = combine_result(checkData(data),result)
    result = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    for x in result:
        result_last += x[0]+' '+str(x[1])+'\n'
    return result_last

def set_data():
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



def show_security(data):
    return '..%s..' % data

def main():
    dispatcher = SoapDispatcher(
        'my_dispatcher',
        location='http://'+host+':8888/',
        action='http://'+host+'8888/',
        namespace='http://security.com/security_sort.wsdl', prefix='ns0',trace=True,ns=True)
    dispatcher.register_function('Security', show_security, returns={'resp': unicode}, args={'datas': security()})
    handler = WSGISOAPHandler(dispatcher)
    wsgi_app = tornado.wsgi.WSGIContainer(handler)
    tornado_app = tornado.web.Application([('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        location = sys.argv[2]
    set_data()
    main()

