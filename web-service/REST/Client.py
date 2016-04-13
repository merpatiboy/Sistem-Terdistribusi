__author__ = 'DickyIrwanto'
import json,urllib2,sys

url = 'http://localhost:5000/security'
if __name__ == '__main__':
    if len(sys.argv) > 1:
        url = sys.argv[1]
    response = urllib2.urlopen(url)
    try:
        result = json.load(response)
        print result
        try:
            for x in result:
                print x[0],x[1]
        except:
            print 'Error Extraction Proccess'
    except:
        print 'Error Connection'