import Adafruit_DHT as dht
import serial, struct, csv, os, time
from time import sleep

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
    
    data=['w','%.1f'%t,'%.1f'%h, str(pms7003_data[PMS7003_PM1P0]),
                         str(pms7003_data[PMS7003_PM2P5]), str(pms7003_data[PMS7003_PM10P0]),
                         '%02d.%02d.%02d'%(now.tm_year, now.tm_mon, now.tm_mday),
                         '%02d:%02d:%02d' %(now.tm_hour, now.tm_min, now.tm_sec),' ']
    
    if not os.path.isfile('data/%02d_%02d_%02d.csv'%(now.tm_year, now.tm_mon, now.tm_mday)):
        f = open('data/%02d_%02d_%02d.csv'%(now.tm_year, now.tm_mon, now.tm_mday), 'w')
        csv_writer = csv.writer(f)
        csv_writer.writerow(['name','temperature', 'humidity', 'PM1.0', 'PM2.5', 'PM10', 'date', 'time', 'CO2'])
        f.close()
        
    f = open('data/%02d_%02d_%02d.csv'%(now.tm_year, now.tm_mon, now.tm_mday), 'a')
    csv_writer = csv.writer(f)
    csv_writer.writerow(data)
    
    print(data)
    sleep(300)

