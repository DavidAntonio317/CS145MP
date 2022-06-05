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
    DATA, addr = UDP_SOCKET.recvfrom(1024)
    transaction = DATA.decode()
    print(transaction)
    
    # Send Payload 

    # Open payload.txt
    FILE = open(filename)
    payload = FILE.read()
    dat_length = math.ceil(len(payload) / 80) # length of data sent per second
    k = 0 # index
    SN = 0 # Sequence Number
    z = 0 #  denotes the last packet in the transmission
    flag = True
    initial_t = time.time() # Variable that takes the start time of payload processing
    while k < len(payload):
        start_t = time.time()
        while (1):
            current_k = dat_length + k
            if current_k  < len(payload): DATA = payload[k:current_k] # take a portion of the payload having the size of the data length we specified earlier. 
            else: DATA = payload[k:]
            #  check if that portion of the payload is at the end of the payload or not
            if current_k < len(payload): z = 0 
            else: z = 1

            packet = f'ID{ID}SN{str(SN).zfill(7)}TXN{transaction}LAST{z}{DATA}' # format a packet according to the specs in the MP
            checker = checksum(packet)
            UDP_SOCKET.sendto(packet.encode(), (HOST,PORT)) # send packet to server
            print(packet)
            try: # try to receive an acknowledgement (ACK) message from the server
                ACK = UDP_SOCKET.recv(64).decode() # receive an acknowledgement (ACK) message from the server
                print(ACK)
            except socket.timeout: # If the packet was not received successfully
                dat_length = math.ceil(dat_length * 0.95) # trim data to be sent
                UDP_SOCKET.settimeout(UDP_SOCKET.gettimeout() + 2) # add additional 2 seconds for the next timeout.
            else:
                if ACK[-32:] == checker: # check if there erros in the transmission message
                    break
        k = current_k # update the current index 
        SN = SN + 1 # update sequence number
        end_t = time.time() 
        span = end_t - start_t # take the duration the roundtrip time
        UDP_SOCKET.settimeout(span + 2)  # account for the delay

        while flag:    
            # Calculate the number of packets that can be sent in the time remaining
            packetsLeft = math.ceil((95 - span) / span)  
            # Calculate the amount of characters in each packet
            dat_length = math.ceil((len(payload) - k) / packetsLeft)

            flag = False
    #  calculate the duration it took for the whole payload to be sent.
    final_t = time.time()
    transaction_t = final_t - initial_t
    print(f'Duration: {transaction_t}')

if __name__ == "__main__":
    main()
