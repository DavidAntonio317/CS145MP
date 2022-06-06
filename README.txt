David Antonio
2018-00087
CS 145
Lab 1

Machine Problem
Parameter-Adaptive Reliable UDP-based Protocol
A.Y. 2021-2022, 2nd Semester
=================================================  README FILE  ========================================================

Instructions on how to run sender.py:

1. Get a copy of the sender.py file through Uvle or 
   through github: https://github.com/DavidAntonio317/CS145MP/blob/main/sender.py
2. Open an Instance of the AWS. SSH into the instance.
3. Sync code with your instance via SCP or git
4. Open directory that contains sender.py
5. Type: "python3 sender.py -f <path/to/file.txt> -a <IP address of receiver> -s <receiver port> -c
<Sender Port> -i <Unique ID>". Press Enter.
6. Wait until all packets are successfully delivered.If more than 120 seconds have passed 
   and not all packets have been sent, terminate the program using Ctrl + C.

**Note**
Remember to generate new payload file every test so that the transaction that you will use must 
only have Frequency Used: 1. This is to ensure that during the actual testing, you do not have prior 
knowledge about the data, and the hidden parameters tied to it.

Type this in the terminal to generat new payload file:

wget  http://3.0.248.41:5000/get_data?student_id=e3e22884 



==============================================  END OF README FILE  ========================================================



