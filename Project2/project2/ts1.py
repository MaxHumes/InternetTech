import threading
import socket
import time

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50009)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))

#Create a dictionary to store the data
#Stores key: google.com value: Address
    with open('ip.txt', 'r') as f:
        data_dict = {}
        for line in f:
            key, value = line.strip().split()
            data_dict[key] = value

    print(data_dict)      

#maybe an issue down here
    start = time.time()
    while((time.time() - start) < 5):
        client_bytes = csockid.recv(200)
        if(len(client_bytes) == 0):
            break

        client_str = client_bytes.decode('utf-8').strip()

        if client_str in data_dict:
            response_str = client_str + ' ' +  data_dict[client_str] + ' IN'
            response_bytes = response_str.encode('utf-8')
            csockid.send(response_bytes)
        else:
            #Send no Bytes (its empty I think)
            csockid.send(b'')
 
        print ("[S]: Closing server socket {}".format(host))
        ss.close()
        exit()

if __name__ == "__main__":
    t1 = threading.Thread(name='server', target=server)
    t1.start()


