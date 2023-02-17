import threading
import socket
import sys
import time

def ts1():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[ts1]: TS1 socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    #Create a dictionary to store the data
    #Stores key: Domain Name value: Address
    with open('PROJ2-DNSTS1.txt', 'r') as f:
        data_dict = {}
        for line in f:
            domain, ip, t = line.strip().split()
            data_dict[domain] = ip
    print(data_dict)

    server_binding = ('', int(sys.argv[1]))
    ss.bind(server_binding)
    ss.listen(1)
    csockid, addr = ss.accept()
    print ("[ts1]: Got a connection request from a client at {}".format(addr))     

    #maybe an issue down here
    while True:
        client_bytes = csockid.recv(200)
        if(len(client_bytes) == 0):
            break

        client_str = client_bytes.decode('utf-8').strip()

        if client_str in data_dict:
            response_str = client_str + ' ' +  data_dict[client_str] + ' IN'
            response_bytes = response_str.encode('utf-8')
            csockid.send(response_bytes)
        #otherwise don't send anything
        print('weiner')
    print ("[ts2]: Closing TS1 socket")
    ss.close()
    exit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Error: Not enough arguments provided')
        exit()
    t1 = threading.Thread(name='ts1', target=ts1)
    t1.start()
