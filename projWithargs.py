import argparse
import hashlib
import math
import socket
import time

def checksum(packet):
    return hashlib.md5(packet.encode('utf-8')).hexdigest()

parser = argparse.ArgumentParser()
parser.add_argument('-f', default='payload.txt')
parser.add_argument('-a', default='127.0.0.1')
parser.add_argument('-s', default=9000)
parser.add_argument('-c', default=6671)
parser.add_argument('-i', default='e3e22884')
args = parser.parse_args()

FILE = args.f
DEST_HOST = args.a
DEST_PORT = int(args.s)
SRC_PORT = int(args.c)
ID = args.i

'''
    this implementation assumes that any payload can be sent in less than 90 seconds
    with proper timeout and packet length limit. packet length is estimated by
    computing number of packets that can be sent in the remaining time and divides
    remaining payload between those packets.
'''
with open(FILE) as f:
    payload = f.read()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('', SRC_PORT))
        sock.settimeout(11)
        # max packet length to send over 1 second, assuming delivery in less than 90 seconds
        data_len = max(1, math.ceil(len(payload) / 90))

        index = 0
        sqnum = 0
        probe = True

        # initiate transaction
        while True:
            sock.sendto(f'ID{ID}'.encode(), (DEST_HOST,DEST_PORT))
            try:
                txnID = sock.recv(64).decode()
            except socket.timeout:
                print('Request failed. Reattempting...')
            else:
                print(txnID)
                if txnID == 'Existing alive transaction':
                    time.sleep(5)
                else:
                    break

        t_start = time.time()

        # transmit payload
        while index < len(payload):
            start = time.time()

            # attempt to send a packet with data_len characters
            # reduce data_len by 5% if packet times out
            while True:
                if index + data_len < len(payload):
                    data = payload[index:index + data_len]
                else:
                    data = payload[index:]

                packet = f'ID{ID}SN{str(sqnum).zfill(7)}TXN{txnID}LAST{0 if index + data_len < len(payload) else 1}{data}'
                check = checksum(packet)
                sock.sendto(packet.encode(), (DEST_HOST,DEST_PORT))
                print(packet)

                try:
                    ack = sock.recv(64).decode()
                    print(ack)
                except socket.timeout:
                    print("got here")
                    data_len = int(data_len * 0.95)
                    sock.settimeout(sock.gettimeout() + 2)
                else:
                    # ensure that ack received is for sent packet
                    if ack[-32:] == check:
                        break
                print(index)
                print(data_len)

            end = time.time()
            duration = end - start
            sock.settimeout(duration + 2) # extra 2 seconds to account for delays

            index+=data_len
            sqnum+=1
            if probe:
                probe = False
                timeout = int(duration)
                # compute number of packets that can be sent in remaining time
                packet_num = (90 - timeout) / timeout
                # compute number of characters per packet
                data_len = math.ceil((len(payload) - index) / packet_num)

                print(data_len) # for testing

            print(data, duration) # for testing

        t_end = time.time()
        print(f'Transaction: {t_end - t_start}')