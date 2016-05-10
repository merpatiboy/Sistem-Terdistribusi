__author__ = 'DickyIrwanto'
import urllib2, bs4, sys

if __name__ == '__main__':
    url = 'localhost'
    if len(sys.argv) > 1:
        url = sys.argv[1]
    Resp = urllib2.urlopen("http://"+url+":8888/Security")
    soup = bs4.BeautifulSoup(Resp,"lxml")
    soup = soup.findAll('datas')
    for x in soup:
        print x