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
index = 0
sqnum = 0
probe = True

# Initiate UDP connection
UDP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Checksum function
def checksum(packet):
    return hashlib.md5(packet.encode('utf-8')).hexdigest()

# Initialize main function
def main():

    # Bind the UDP scoket to host and port
    UDP_SOCKET.bind((socket.gethostbyname(socket.gethostname()), PORT))

    # Send an Intent Message
    UDP_SOCKET.sendto(f'ID{ID}'.encode(), ADDR2)
    data, addr = UDP_SOCKET.recvfrom(1024)
    transaction = data.decode()
    print(transaction)

    
    # Send Payload 

    # Open payload.txt
    FILE = 'payload.txt'   
    with open(FILE) as f:
        payload = f.read()
        



if __name__ == "__main__":
    main()

###### TEST ADD #####