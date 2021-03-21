import threading
from socket import *
import sys
import os

portno = int(input())
serverName = '127.0.0.1'
def get_req(portno):
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((serverName, portno))
    file = ['/hello.txt','/sample.txt','/second.html']
    req = "GET /test.txt HTTP/1.1\r\n" 
    req += "Accept: */*\r\n"
    req += "Host: 127.0.0.1:" + str(portno) + "\r\n"
    req += "Accept-Encoding: gzip, deflate, br\r\n"
    req += "Connection: keep-alive\r\n"
    req += "Cookie: yeXQbSuyXM=wdiXTApprS\r\n\r\n"
    clientsocket.send(req.encode())
    res = clientsocket.recv(1024).decode()
    print(res)

def head_req(portno):
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((serverName, portno))
    file = ['/hello.txt','/sample.txt','/second.html']
    req = "HEAD / HTTP/1.1\r\n" 
    req += "Accept: */*\r\n"
    req += "Host: 127.0.0.1:" + str(portno) + "\r\n"
    req += "Accept-Encoding: gzip, deflate, br\r\n"
    req += "Connection: keep-alive\r\n"
    req += "Cookie: yeXQbSuyXM=wdiXTApprS\r\n\r\n"
    clientsocket.send(req.encode())
    res = clientsocket.recv(1024).decode()
    print(res)


while True:
    # thread = threading.Thread(target=head_req,args=(portno,))
    # thread.start()
    
    thread2 = threading.Thread(target=get_req,args=(portno,))
    thread2.start()
    # thread3 = threading.Thread(target=get_req,args=(portno,))
    # thread3.start()
