import threading
import socket

def client():
    # Define ports for reverse and upper servers
    rev_port = 50007
    up_port = 50008
    localhost_addr = socket.gethostbyname(socket.gethostname())

    ''' REVERSE '''
    try:
        csr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # connect to the reverse string server on local machine
    server_binding = (localhost_addr, rev_port)
    csr.connect(server_binding)

    write_lines_from_server(csr, 'in-proj.txt', 'outr-proj.txt')

    # close the reverse client socket
    csr.close()
    

    ''' UPPER CASE '''
    try:
        csu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # connect to the uppercase string server on local machine
    server_binding = (localhost_addr, up_port)
    csu.connect(server_binding)

    write_lines_from_server(csu, 'in-proj.txt', 'outup-proj.txt')

    csu.close()
    exit()

    '''
    # send lines to reverse server and write output to outr-proj.txt
    with open('in-proj.txt', 'r') as in_file, open('outr-proj.txt', 'w') as out_file:
        for line in in_file:
            cs.send(line.encode('utf-8'))
            data_from_server=cs.recv(200)
            out_file.write(data_from_server.decode('utf-8'))

    
    # send lines to uppercase server and write output to outup-proj.txt
    with open('in-proj.txt', 'r') as in_file, open('outup-proj.txt', 'w') as out_file:
        for line in in_file:
            cs.send(line.encode('utf-8'))
            data_from_server=cs.recv(200)
            out_file.write(data_from_server.decode('utf-8'))
    
    # close the client socket
    cs.close()
    exit()
    '''

#method to read lines from input file, send to server, and write output to out_path
def write_lines_from_server(sock, in_path, out_path):
    lines = []
    with open(in_path, 'r') as in_file, open(out_path, 'w') as out_file:
        for line in in_file:
            sock.send(line.encode('utf-8'))
            data_from_server=sock.recv(200)
            out_file.write(data_from_server.decode('utf-8').strip() + '\n')
            #out_file.write(data_from_server.decode('utf-8').strip())
        #out_file.writelines(lines)

if __name__ == "__main__":
    t2 = threading.Thread(name='client', target=client)
    t2.start()