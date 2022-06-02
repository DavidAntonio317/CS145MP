from hmac import trans_36
import socket
import hashlib
import math
import time
import argparse

# Checksum function
def checksum(packet):
    return hashlib.md5(packet.encode('utf-8')).hexdigest()

# Initialize main function
def main():
    # Parsing commandline arguments
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-f', default='e3e22884.txt')
    argparser.add_argument('-a', default='10.0.7.141')
    argparser.add_argument('-s', default=9000)
    argparser.add_argument('-c', default=6671)
    argparser.add_argument('-i', default='e3e22884')
    args = argparser.parse_args()

    filename = args.f 
    dest_host = args.a
    dest_port = int(args.s)
    src_port = int(args.c)
    ID = args.i  

    # Initiate UDP connection
    UDP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the UDP scoket to host and port
    UDP_SOCKET.bind(('', src_port))
    UDP_SOCKET.settimeout(11)


    # Send an Intent Message
    UDP_SOCKET.sendto(f'ID{ID}'.encode(), (dest_host, dest_port))

    # Receive Acknowledgement
    data, addr = UDP_SOCKET.recvfrom(1024)
    transaction = data.decode()
    print(transaction)
    
    # Send Payload 

    # Open payload.txt
    FILE = open(filename)
    payload = FILE.read()
    packet_size = max(1, math.ceil(len(payload) / 90)) # packet_size

    k = 0
    SN = 0
    flag = True
    z = 0

    t_start = time.time()
    while k < len(payload):
        start = time.time()

        while True:
            if k + packet_size < len(payload):
                data = payload[k:k + packet_size]
            else:
                data = payload[k:]

            if k + packet_size < len(payload):
                z = 0
            else:
                z = 1

            packet = f'ID{ID}SN{str(SN).zfill(7)}TXN{transaction}LAST{z}{data}'
            check = checksum(packet)
            UDP_SOCKET.sendto(packet.encode(), (dest_host,dest_port))
            print(packet)
            try:
                ack = UDP_SOCKET.recv(64).decode()
                # print(ack)
            except socket.timeout:
                # print("got here")
                packet_size = int(packet_size * 0.95)
                UDP_SOCKET.settimeout(UDP_SOCKET.gettimeout() + 2)
            else:
                # check that the ack received is for the packet that was sent
                if ack[-32:] == check:
                    break

        end = time.time()
        duration = end - start
        UDP_SOCKET.settimeout(duration + 2) 

        k+=packet_size
        SN+=1
        if flag:
            flag = False
            timeout = int(duration)
            # compute number of packets that can be sent in remaining time
            packet_num = (90 - timeout) / timeout
            # compute number of characters per packet
            packet_size = math.ceil((len(payload) - k) / packet_num)


        # print(data, duration) # for testing

    t_end = time.time()
    print(f'Transaction: {t_end - t_start}')

if __name__ == "__main__":
    main()
