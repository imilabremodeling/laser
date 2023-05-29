import socket
import os

def read_file():
    with open('aslog.txt','r') as f:
        line = f.readlines()

    parameters = ""
    host = "127.0.0.1"
    #host = "192.168.3.242"
    port = 32020
    ctrl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ctrl.connect((host, port))
    for i in range(len(line)-1):
        parameters += str(line[i])

    ctrl.send(parameters.encode())
    ctrl.close()

