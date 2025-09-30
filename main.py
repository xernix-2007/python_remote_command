import socket
import sys

def create_socket():
    try:
        global server
        global host
        global port
        host=''
        port=8888
        server = socket.socket()
    except socket.error as err:
        print(f'this error occured in create_socket{err}')

def bind_socket():
    try:
        server.bind((host, port))
        server.listen(5)
    except socket.error as msg:
        print('error in binging socket retrying....',msg)
        bind_socket()
def acceptConnections():
    conn,addr = server.accept()
    print(f'client connected with addr : {addr}')
    sendMessage(conn)
    conn.close()
def sendMessage(conn):
    while True:
        try:
            cmd = input('')
            if cmd == 'quit':
                conn.close()
                server.close()
                sys.exit('closed connections')
            else:
                command = conn.send(cmd.encode('utf-8'))
                recieve = conn.recv(4026).decode('utf-8')
                print(recieve,end='')
        except Exception as err:
            print("an error occured in appecting commands and sending",err)

def main():
    create_socket()
    bind_socket()
    acceptConnections()

main()