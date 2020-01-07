import socket, os, time, csv, schedule, datetime

def getFileSize(filename):
    fileSize = os.path.getsize("data/"+filename)
    return str(fileSize)

def send():
    HOST = '192.168.35.131'
    PORT = 10001
    
    #connect socket from server
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print("connect")

    #send file name
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    filename = (yesterday.strftime('%Y_%m_%d')) + '.csv'
    print(filename)
    s.send(filename.encode())
    
    #send file size
    filesize=''
    filesize = filesize + getFileSize(filename)
    print("send filesize : " + filesize)
    s.send(filesize.encode())

    #wait ready sign
    ready = s.recv(1024)
    if ready.decode() == "ready":
        print("ready")
        with open("data/%s" %filename, 'rb') as f:
            data = f.read(1024)
            #print(data)
            while data:
                s.send(data)
                data = f.read(1024)
            f.close()

    print("finish")
    s.close()

if __name__=="__main__":
    schedule.every().day.at("00:01").do(send)
    while True:
        print("running")
        schedule.run_pending()
        time.sleep(20)