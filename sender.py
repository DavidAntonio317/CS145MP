from hmac import trans_36
import socket
import hashlib
import math
import time
import sys

# Checksum function
def checksum(packet):
    return hashlib.md5(packet.encode('utf-8')).hexdigest()

# Initialize main function
def main():
    # Parsing commandline arguments
    args = sys.argv
    filename = "e3e22884.txt"
    HOST = "10.0.7.141"
    PORT = 9000
    src_port = 6671
    ID = "e3e22884"

    for i in range(len(args)):
        if args[i] == "-f":
            filename = args[i+1]
        elif args[i] == "-a":
            HOST = args[i+1]
        elif args[i] == "-s":
            PORT = int(args[i+1])
        elif args[i] == "-c":
            src_port = int(args[i+1])
        elif args[i] == "-i":
            ID = args[i+1]

    # Initialization of  UDP connection
    UDP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Binding the UDP socket to host and port
    UDP_SOCKET.bind(('', src_port))
    UDP_SOCKET.settimeout(11)

    # Send an Intent Message
    UDP_SOCKET.sendto(f'ID{ID}'.encode(), (HOST, PORT))

    # Receive Acknowledgement
    data, addr = UDP_SOCKET.recvfrom(1024)
    transaction = data.decode()
    print(transaction)
    
    # Send Payload 

    # Open payload.txt
    FILE = open(filename)
    payload = FILE.read()
    dat_length = math.ceil(len(payload) / 95) # dat_length
    k = 0
    SN = 0
    z = 0
    flag = True
    initial_t = time.time()
    while k < len(payload):
        start_t = time.time()
        while (1):
            current_k = dat_length + k
            if current_k  < len(payload):data = payload[k:current_k]
            else:data = payload[k:]

            if current_k < len(payload):z = 0
            else:z = 1

            packet = f'ID{ID}SN{str(SN).zfill(7)}TXN{transaction}LAST{z}{data}'
            checker = checksum(packet)
            UDP_SOCKET.sendto(packet.encode(), (HOST,PORT))
            print(packet)
            try:
                ack = UDP_SOCKET.recv(64).decode()
                print(ack)
            except socket.timeout:
                dat_length = math.ceil(dat_length * 0.95)
                UDP_SOCKET.settimeout(UDP_SOCKET.gettimeout() + 2)
            else:
                if ack[-32:] == checker:
                    break
        k = current_k
        SN = SN + 1
        end_t = time.time()
        span = end_t - start_t
        UDP_SOCKET.settimeout(span + 2) 

        while flag:    
            # Calculate the number of packets that can be sent in the time remaining
            packetsLeft = math.ceil((95 - span) / span)  
            # Calculate the amount of characters in each packet
            dat_length = math.ceil((len(payload) - k) / packetsLeft)

            flag = False

    final_t = time.time()
    transaction_t = final_t - initial_t
    print(f'Transaction: {transaction_t}')

if __name__ == "__main__":
    main()
