import threading
import socket

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    with open('in-proj.txt', 'r') as in_file, open('out-proj.txt', 'w') as out_file:
        for line in in_file:
            cs.send(line.encode('utf-8'))
            data_from_server=cs.recv(200)
            out_file.write(data_from_server.decode('utf-8'))
    
    # close the client socket
    cs.close()
    exit()

if __name__ == "__main__":
    t2 = threading.Thread(name='client', target=client)
    t2.start()