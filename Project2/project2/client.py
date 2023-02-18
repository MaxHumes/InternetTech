import threading
import socket
import sys


def client():
    try:
        csr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # connect to to the LS
    server_binding = (sys.argv[1], int(sys.argv[2]))
    csr.connect(server_binding)

    write_lines_from_server(csr, 'PROJ2-HNS.txt', 'RESOLVED.txt')

    # close the client socket
    csr.close()
    

#method to read lines from input, send to server, and back to client and to output file
def write_lines_from_server(sock, in_path, out_path):
    lines = []
    with open(in_path, 'r') as in_file, open(out_path, 'w') as out_file:
        for line in in_file:
            sock.send(line.encode('utf-8'))
            data_from_server=sock.recv(200)
            out_file.write(data_from_server.decode('utf-8').strip() + '\n')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Error: Not enough arguments provided')
        exit()
    t1 = threading.Thread(name='client', target=client)
    t1.start()
