import socket
import threading
import sys
import select

def ls():
    #create ls socket
    try:
        lssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[ls]: Load balancing server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    
    #get socket for ts1 and ts2
    ts1sock = get_ts_socket(sys.argv[2], int(sys.argv[3]))
    ts2sock = get_ts_socket(sys.argv[4], int(sys.argv[5]))
    print("[ls]: Connected to TS servers")

    #listen for client connection
    server_binding = ('', int(sys.argv[1]))
    lssock.bind(server_binding)
    lssock.listen(1)
    csockid, addr = lssock.accept()
    print ("[ls]: Got a connection request from a client at {}".format(addr))

    while True:
        #recieve domain name from client
        clientBytes = csockid.recv(200)
        if len(clientBytes) == 0:
            break

        #send bytes to TS1
        ts1sock.send(clientBytes)
        #send bytes to TS2
        ts2sock.send(clientBytes)
    
        #block with select and wait for timeout
        r,w,e = select.select([ts1sock, ts2sock],[],[],5)
        if not r:
            #timeout. (I added .strip because TIMED OUT was printing under) 
            timeout_str = '{} - TIMED OUT'.format(clientBytes.decode('utf-8').strip())
            csockid.send(timeout_str.encode('utf-8'))
        else:
            csockid.send(r[0].recv(200))

    # Close the server socket
    print ("[ls]: Closing load balancing server socket")
    #was ss not lssock (changed this)
    lssock.close()
    exit()

def get_ts_socket(host_name, listen_port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[ls]: TS client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # connect to the reverse string server on local machine
    server_binding = (host_name, listen_port)
    sock.connect(server_binding)

    return sock


if __name__ == "__main__":
    if len(sys.argv) < 6:
        print('Error: Not enough arguments provided')
        exit()
    t1 = threading.Thread(name='ls', target=ls)
    t1.start()
