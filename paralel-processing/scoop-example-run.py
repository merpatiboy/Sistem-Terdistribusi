__author__ = 'DickyIrwanto'
import sys,subprocess

if __name__ == '__main__':
    if len(sys.argv) > 1 and len(sys.argv) < 2:
        data = sys.argv[1]
    else:
        data = 'scoop-security'
    #subprocess.call('python -m scoop --host 127.0.0.1 -vv -n 6 '+data+'.py')
    subprocess.call('python -m scoop -n 6 '+data+'.py')