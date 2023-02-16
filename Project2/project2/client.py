import socket
import threading

def client():
    # Define ports for reverse and upper servers
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    try:
        csr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # connect to the reverse string server on local machine
    server_binding = (localhost_addr, port)
    csr.connect(server_binding)

    write_lines_from_server(csr, 'PROJ2-HNS.txt', 'RESOLVED.txt')

    # close the reverse client socket
    csr.close()
    

#method to read lines from input file, send to server, and write output to out_path
def write_lines_from_server(sock, in_path, out_path):
    lines = []
    with open(in_path, 'r') as in_file, open(out_path, 'w') as out_file:
        for line in in_file:
            sock.send(line.encode('utf-8'))
            data_from_server=sock.recv(200)
            out_file.write(data_from_server.decode('utf-8').strip() + '\n')

if __name__ == "__main__":
    client()
  #  t2 = threading.Thread(name='client', target=client)
  # t2.start()
