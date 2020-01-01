import time
import csv
import socket
import pandas as pd
from time import sleep

HOST = '202.30.31.101'
PORT = 8888

now = time.localtime()

while True:
    msg = pd.read_csv('data/%02d_%02d_%02d.csv'%(now.tm_year, now.tm_mon, now.tm_mday))
    print(msg.tail(1))
    
    #s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    
    
    s.send(msg.encode(encoding='utf_8', errors='atriot'))    
    data=s.recv(1024)
    data = data.decode()
    if data == '0':
        continue
    else:
        #######  save to csv ########
        f = open('%02d_%02d_%02d.csv'%(now.tm_year, now.tm_mon, now.tm_mday), 'r')
        csv_writer = csv.writer(f)
        csv_writer.writerow(data)
        f.close()
        print(data)
        sleep(300)
        
s.close()
