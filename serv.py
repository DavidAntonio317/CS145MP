import hashlib
import socket
import time
import random

HOST = '127.0.0.1'
PORT = 6671
ADDR = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('',9000))

uid = sock.recv(512) # begin transaction
uid = uid.decode()
time.sleep(1)
sock.sendto(uid[2:].encode(), ADDR) # respond with id

def checksum(packet):
    return hashlib.md5(packet.encode('utf-8')).hexdigest()

i = 0
# while True:
#     time.sleep(1)
#     data = sock.recv(512)
#     data = data.decode()
#     print(data)

#     print('{} {}'.format(i, data))
    
#     sock.sendto('ACK{}TXN{}MD5{}'.format(str(i).zfill(7), uid, checksum(data)).encode(), ADDR)
#     i+=len(data[35:])

#     if data[34] == '1':
#         break