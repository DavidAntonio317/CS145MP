import socket
import sys
import time

f = ""
a = ""
s = ""
c = ""
i = ""
port = 6671
ID = "IDWWWWWWWW"
arguments = sys.argv
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for k in range (len(arguments)):
    if arguments[k] == "-f":
        f = arguments[k+1]
    elif arguments[k] == "-a":
        a = arguments[k+1]
    elif arguments[k] == "-s":
        s = arguments[k+1]
    elif arguments[k] == "-c":
        c = arguments[k+1]
    elif arguments[k] == "-i":
        i = arguments[k+1]


msg = ID
# client_socket.sendto(msg.encode(),('127.0.0.1', 12345))
# data, addr = client_socket.recvfrom(4096)
# t_start = time.time()
# t_end = time.time()
# print(f'Time: {t_end - t_start}')
# print("Server says")
# print(str(data.decode()))


message = "ID{}SN{}TXN{}LAST{}PAYLOAD{}"

# Open file of payload
with open('payload.txt') as f:
    msg = f.read(10)
    while(msg):
        print(msg)
        msg = f.read(10)
    
    print("end")





# client_socket.close()



