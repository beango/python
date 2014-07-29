from sockchat import sockchat
import time, sys, threading
import signal



chat = sockchat()
signal.signal(signal.SIGINT, chat.closeServ)
signal.signal(signal.SIGTERM, chat.closeServ)

uid = chat.connectServ("user1")
print uid

chat.recvChat()

'''
t = threading.Thread(target=chat.recvChat, args=())
t.setDaemon(True)
t.start()
'''
'''
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 12345))
sock.send("1")
sock.send("1")
sock.send("1")
'''
chat.closeServ()