from hmac import trans_36
import socket
import hashlib
import math

# Initialize Variables
ID = 'e3e22884'
HOST = '10.0.7.141'
PORT = 6671
ADDR = (HOST, PORT)
ADDR2 = (HOST, 9000)

DEST_PORT = 9000
SRC_PORT = 6671

# Initiate UDP connection
UDP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Open payload.txt
# FILE = open('payload.txt')


# Checksum function
def checksum(packet):
    return hashlib.md5(packet.encode('utf-8')).hexdigest()

# Initialize main function
def main():

    # Bind the UDP scoket to host and port
    UDP_SOCKET.bind(('', PORT))
    # UDP_SOCKET.settimeout(11)


    # Send an Intent Message
    UDP_SOCKET.sendto(f'ID{ID}'.encode(), (HOST, DEST_PORT))

    # Receive Acknowledgement
    data, addr = UDP_SOCKET.recvfrom(1024)
    transaction = data.decode()
    print(transaction)



    
    # Send Payload 
    # payload = FILE.read()
    # data_len = max(1, math.ceil(len(payload) / 90)) 
    # print(data_len)



if __name__ == "__main__":
    main()

###### TEST ADD #####