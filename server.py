import socket
import sys
import Queue
import threading
import time


def play(info):
    print(threading.currentThread().getName(), 'Starting')
    print('first client ', info[0][1])
    print('second client ', info[1][1])
        

def main():
    sock = socket.socket()
    host = socket.gethostname()
    portOne = 8888
    portTwo = 9999
    portThree = 1010
    try:
        sock.bind(('', portOne))
    except:
        try:
            sock.bind(('', portTwo))
        except:
            try:
                sock.bind(('', portThree))
            except:
                print('count not bind socket')
                sys.exit()

    q = Queue.Queue()

    sock.listen(50)
    while True:
        c, addr = sock.accept()
        print('got connection from', addr)

        threadInfo = []
        threadInfo.append(c)
        threadInfo.append(addr)


        q.put(threadInfo)
        if q.qsize() == 1:
            print('queue has 1')
        else:
            twoThreadInfo = []
            twoThreadInfo.append(q.get())
            twoThreadInfo.append(q.get())
            print(twoThreadInfo)
            t = threading.Thread(target=play, args=(twoThreadInfo,))
            t.start()

main()
