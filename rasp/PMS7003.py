import Adafruit_DHT as dht
import serial
import struct
import time
import csv
import socket
from time import sleep

HOST = '202.30.31.101'
PORT = 8888
COM_PORT = '/dev/ttyUSB0'

PMS7003_FRAME_LENGTH = 0
PMS7003_PM1P0 = 1
PMS7003_PM2P5 = 2
PMS7003_PM10P0 = 3
PMS7003_PM1P0_ATM = 4
PMS7003_PM2P5_ATM = 5
PMS7003_PM10P0_ATM = 6
PMS7003_PCNT_0P3 = 7
PMS7003_PCNT_0P5 = 8
PMS7003_PCNT_1P0 = 9
PMS7003_PCNT_2P5 = 10
PMS7003_PCNT_5P0 = 11
PMS7003_PCNT_10P0 = 12
PMS7003_VER = 13
PMS7003_ERR_CODE = 14
PMS7003_CHECK_CODE = 15


new = time.localtime()

f = open('%02d_%02d_%02d.csv'%(new.tm_year, new.tm_mon, new.tm_mday), 'w')
csv_writer = csv.writer(f)
csv_writer.writerow(['Date', 'Temperature', 'Humidity', 'PM 1.0', 'PM 2.5', 'PM 10']) 

while True:
    h,t = dht.read_retry(dht.DHT22, 4)
    now = time.localtime()
    ser = serial.Serial(COM_PORT, 9600, timeout=0.1)
    while True:
        c = ser.read(1)
        if len(c) >= 1:
            if ord(c[0]) == 0x42:
                c = ser.read(1)
                if len(c) >= 1:
                    if ord(c[0]) == 0x4d:
                        break;

    buff = ser.read(30)

    check = 0x42 + 0x4d

    check += ord(buff[0:1])

    pms7003_data = struct.unpack('!HHHHHHHHHHHHHBBH', buff)

    print ('\n [%02d.%02d.%02d %02d:%02d:%02d]' 
            %(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
    print (' ---------------------------')
    print ('  Temperature [*C]   = %.1f' %t) 
    print ('  Humidity    ['+'%'+']    = %.1f' %h)
    print (' ---------------------------')
    print ('  PM 1.0 [up/m^3]    =', str(pms7003_data[PMS7003_PM1P0]))
    print ('  PM 2.5 [ug/m^3]    =', str(pms7003_data[PMS7003_PM2P5]))
    print ('  PM 10  [ug/m^3]    =', str(pms7003_data[PMS7003_PM10P0]))
    print (' ---------------------------\n')
    
#######  save to csv ########
#    csv_writer.writerow(['%02d.%02d.%02d %02d:%02d:%02d'
#        %(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec),
#        '{0:0.1f},{1:0.1f}'.format(t,h), str(pms7003_data[PMS7003_PM1P0]),
#            str(pms7003_data[PMS7003_PM2P5]), str(pms7003_data[PMS7003_PM10P0])])
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
    except socket.error:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

    msg1 = 'w'+' '+str(t)+' '+ str(h)+' '+str(pms7003_data[PMS7003_PM1P0])+' '+str(pms7003_data[PMS7003_PM2P5])+' '+str(pms7003_data[PMS7003_PM10P0])

    s.send(msg1.encode(encoding='utf_8', errors='atriot'))    
    data=s.recv(1024)
    data = data.decode()
    if data == '0':
        continue
    else:
        #######  save to csv ########
        f = open('%02d_%02d_%02d.csv'%(now.tm_year, now.tm_mon, now.tm_mday), 'a')
        csv_writer = csv.writer(f)
        csv_writer.writerow(data)
        f.close()
        print(data)
        sleep(300) 
s.close()
