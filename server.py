import socket
import sys
import Queue
import threading
import time


def play(info):
    print(threading.currentThread().getName(), 'Starting') 

    # Set sockets
    playerOne = info[0][0]
    playerTwo = info[1][0]
    
    # The first player in queue is player, second is maker
    playerOne.send('player')
    playerTwo.send('maker')

    # Receive board from maker
    boardState = playerTwo.recv(1024)

    # Send back to player
    playerOne.send(boardState)

def main():
    sock = socket.socket()
    host = socket.gethostname()
    portOne = 8888
    portTwo = 9999
    portThree = 1010
    try:
        sock.bind(('', portOne))
        print('Connected on port ', portOne)
    except:
        try:
            sock.bind(('', portTwo))
            print('Connected on port ', portTwo)
        except:
            try:
                sock.bind(('', portThree))
                print('Connected on port ', portThree)
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
