from hmac import trans_36
import socket
import hashlib

# Initialize Variables
ID = 'e3e22884'
HOST = '10.0.7.141'
PORT = 6671
ADDR = (HOST, PORT)
ADDR2 = (HOST, 9000)

# Initiate UDP connection
UDP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Open payload.txt
FILE = open('payload.txt')


# Checksum function
def checksum(packet):
    return hashlib.md5(packet.encode('utf-8')).hexdigest()

# Initialize main function
def main():

    # Bind the UDP scoket to host and port
    UDP_SOCKET.bind((socket.gethostbyname(socket.gethostname()), PORT))

    # Send
    UDP_SOCKET.sendto(f'ID{ID}'.encode(), ADDR2)

    data, addr = UDP_SOCKET.recvfrom(1024)
    transaction = data.decode()
    print(transaction)



if __name__ == "__main__":
    main()

###### TEST ADD #####