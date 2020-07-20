from main import *

f = open("C:/Users/samaneh/Desktop/ChatRoom/port.txt", "r")
port = int(f.read())


def sendSocket(x):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", port))
        send = pickle.dumps(x)
        s.send(send)
        msg = s.recv(20000)
        s.close()
        data = pickle.loads(msg)
        return(data)
    except:
        return(False)
