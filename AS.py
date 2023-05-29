import socket
from socket import SHUT_RDWR
import os, binascii
import sys
import hashlib
import random
import string
import time
from SMTP import email_func
from sendlog import read_file
import logging
from datetime import datetime
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

# In AS(authentication server) form, we need to use r0 and b0 to calculate and proof that controller is legal or not.
# We do hash function with three parameters which are controller's ID, controller's key and random number r0.
# If the controller is illegal, the calculation(b00) isn't equal with b0 and we send "No" messge to router.
# If the controller is legal, the calculation(b00) is equal with b0 and we send "Yes" messge to router.

fp = open("aslog.txt","a")

def device_update():
#Read Databse and get device information (device_num,ip,port)
        key_manage = {'UNx-3232':'21e5bc4ba219d0e5'}#IDs:ks
        for_db_host = "127.0.0.1"
        for_db_port = 34221
        db_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        db_server.bind((for_db_host, for_db_port)) 
        db_server.listen(1)
        connect1, address1 = db_server.accept()
        print('Database Server has connected with AS!')
        daynum = datetime.now()
        daynum = str(daynum)
        fp.write(daynum+'$root$INFO$from Database Server (ip:192.168.3.192, port:34221) to AS(ip:192.168.3.24, port:34221) : connected.\n$')
        #logging.info('from Database Server (ip:192.168.3.192, port:34221) to AS(ip:192.168.3.24, port:34221) : connected.')
        device_msg = str(connect1.recv(1024), encoding = 'utf-8') #UNx-3232_192.168.11_4840
        device_list = []
        device_list.append(device_msg.split('#'))
        device_name = []
        for tp in device_list[0]:
            a,b,c = tp.split('_')
            key = binascii.b2a_hex(os.urandom(16))
            key = key[16:].decode('utf-8')
            key_manage.update({a:key})

        print("device information is appended in key_manage dictionary." + key_manage)
        fp.write(daynum+'$root$INFO$AS(ip:192.168.3.24, port:34221) has added the device information from Database Server (ip:192.168.3.192, port:34221).\n$')
        #logging.info('The new device from Database Server (ip:192.168.3.192, port:34221) has been added in AS(ip:192.168.3.24, port:34221) : device information exist.')
        connect1.close()
        fp.close()

def check_device():
################### Lathe Agent connect to AS Server ###################
        host = "192.168.3.133"
        #host = "127.0.0.1"
        port = 33123
        au_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        au_server.bind((host, port)) 
        au_server.listen(10)
        while(True):
                connect, address = au_server.accept()
                print('Lathe Agent has connected with AS!')
                daynum = datetime.now()
                daynum = str(daynum)
                fp.write(daynum+'$root$INFO$192.168.3.217$192.168.3.133$33123$socket connect$success.\n$')
                #logging.info('from OPCUA Server (ip:192.168.3.217, port:33123) to AS(ip:192.168.3.24, port:33123) : connected.')
                router_msg = str(connect.recv(1024), encoding = 'utf-8')

                #proof that db is legal or not
                if router_msg == '21e5bc4ba219d0e5':
                        print('Is that DB a legal equipment?')
                        daynum = datetime.now()
                        daynum = str(daynum)
                        fp.write(daynum+'$root$INFO$192.168.3.133$none$none$verified DB with IDs$legal device.\n$')
                        #logging.info('AS(ip:192.168.3.24, port:33123) verified OPCUA Client : legal device.')
                        print('\033[92myes\033[0m')
                        ans = 'y'
                        connect.send(ans.encode())
                        daynum = datetime.now()
                        daynum = str(daynum)
                        fp.write(daynum+'$root$INFO$192.168.3.133$192.168.3.217$33123$send db verify result$success.\n$')
                        #logging.info('from AS (ip:192.168.3.24, port:33123) to OPCUA Server(ip:192.168.3.217, port:33123) send result: connected.')
                else:
                        print('Is that DB a legal equipment?')
                        daynum = datetime.now()
                        daynum = str(daynum)
                        fp.write(daynum+'$root$WARNING$192.168.3.133$none$none$verified DB with IDs$illegal device.\n$')
                        #logging.warning('AS(ip:192.168.3.24, port:33123) verified OPCUA Client : illegal device.')
                        print('\033[91mno\033[0m')
                        ans = 'n'
                        connect.send(ans.encode())
                        daynum = datetime.now()
                        daynum = str(daynum)
                        fp.write(daynum+'$root$INFO$192.168.3.133$192.168.3.217$33123$send DB verify result$success.\n$')
                        #logging.info('from AS (ip:192.168.3.24, port:33123) to OPCUA Server(ip:192.168.3.217, port:33123) send result: connected.')
                        text = "AS_192.168.3.133_Illegal device_192.168.3.24_33123_2_"+daynum
                        email_func(text)
                        daynum = datetime.now()
                        daynum = str(daynum)
                        fp.write(daynum+'$root$INFO$192.168.3.133$none$80$send warning email to manager$finished.\n$')
                        #logging.info('AS(ip:192.168.3.24, port:33123) email to manager: finished.')
                        time.sleep(30)
                        print('Is that CNC agent \'s permission ok?')
                        print('\033[91mno,permission denied !\033[0m')
                        print('\033[91mWe have sent a warning message to the monitoring staff !\033[0m')
                #connect.close()
                #fp.close()

def warning_func():
        #opc ua client connect to AS
        #host_c = "127.0.0.1"
        host_c = "192.168.3.133"
        port_c = 31345
        oclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        oclient.bind((host_c, port_c)) 
        oclient.listen(10)
        while(True):
                connect_c, address_c = oclient.accept()
                print('OPC UA Client has connected with AS!')
                daynum = datetime.now()
                daynum = str(daynum)
                fp.write(daynum+'$root$INFO$192.168.3.190$192.168.3.133$socket connect$success.\n$')
                #logging.info('from OPCUA Client (ip:192.168.3.190, port:31345) to AS(ip:192.168.3.24, port:31345) : connected.')
                temp1_msg = str(connect_c.recv(1024), encoding = 'utf-8')
                temp1_msg = temp1_msg
                email_func(temp1_msg)
                daynum = datetime.now()
                daynum = str(daynum)
                fp.write(daynum+'$root$WARNING$192.168.3.133$none$none$send email to manager$finished.\n$')
                #logging.warning('AS(ip:192.168.3.24, port:33123) email to manager about opcua client verified opcua server illegal with HMAC2: finished.')

        try:
                connect.shutdown(socket.SHUT_RDWR)
        except(socket.error, OSError, ValueError):
                pass
        #fp.close()
        #connect_c.close()
        #read_file('aslog.txt')

