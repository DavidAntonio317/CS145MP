import os
import socket

import hashlib
import math
import time

# select ip if local or prod
DEST_HOST = '127.0.0.1' if os.getenv('USER') == 'hech' else '10.0.7.141'
DEST_PORT = 9000
DEST_ADDR = (DEST_HOST,DEST_PORT)

# http://3.0.248.41:5000/get_data?student_id=4a682a5d
ID = '4a682a5d'

def checksum(packet):
    return hashlib.md5(packet.encode('utf-8')).hexdigest()

'''
    this implementation assumes that any payload can be sent in less than 90 seconds
    with proper timeout duration and packet length limit. packet length is estimated
    by computing number of characters to send in one second then multiplying by the
    timeout duration. packets to send is reduced by one by distributing it over all
    remaining packets.
'''
with open('payload.txt') as f:
    payload = f.read()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('', 6704))
        sock.settimeout(11)
        # max packet length to send over 1 second, assuming delivery in 90 seconds
        data_len = max(1, math.ceil(len(payload) / 90))

        index = 0
        sqnum = 0
        probe = True

        t_start = time.time()

        # initiate transaction
        while True:
            sock.sendto(f'ID{ID}'.encode(), DEST_ADDR)
            try:
                txnID = sock.recv(64).decode()
            except socket.error:
                print('Request failed. Reattempting...')
            else:
                print(txnID)
                break

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
                sock.sendto(packet.encode(), DEST_ADDR)
                try:
                    ack = sock.recv(64).decode()
                except socket.error:
                    data_len = int(data_len * .95)
                else:
                    # ensure that ack received is for sent packet
                    if ack[-32:] == check:
                        break

            end = time.time()
            timeout = end - start
            sock.settimeout(timeout + 2) # extra 2 seconds to account for delay

            index+=data_len
            sqnum+=1
            if probe:
                probe = False
                # let packet length be a function of timeout and payload length, assume delivery in 90 seconds with no delays.
                data_len = math.ceil(int(timeout) * len(payload) / 90)
                # compute number of packets needed for delivery
                packet_num = len(payload) // data_len
                # distribute a packet over all packets, dont count initial packet and distributed packet
                data_len += round(data_len / (packet_num - 2))

                print(data_len) # for testing

            print(data, timeout) # feedback of successful send

        t_end = time.time()
        print(f'Transaction: {t_end - t_start}')