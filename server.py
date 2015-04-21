import socket
import Queue

sock = socket.socket()
host = socket.gethostname()
port = 8888
sock.bind(('', port))

sock.listen(50)
while True:
    c, addr = sock.accept()
    print('got connection from', addr)
    c.send('hello person')
    c.close

