import socket, os, time, csv, sys

HOST = '192.168.35.131'
PORT = 10001

def getFileSize(filename):
    fileSize = os.path.getsize("data/"+filename)
    return str(fileSize)

def send():
    #connect socket from server
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("error")
        sys.exit()
    print("connect")
    
    #get file name
    fileName = s.recv(1024)
    fileName = fileName.decode()
    print('fileName : '+ fileName)
    fileNameList = fileName.split(' ')
    print(fileNameList[0])

    #find file name
    for filename in fileNameList:
        if not os.path.isfile("data/%s" %filename):
            print("not hve (%s) file name")
            msg = "nameError"
            s.send(message.encode(encoding='utf_8', errors='atriot'))
            s.close()
    print("file is all here!!\n")

    #send file size
    filesize=''
    for filename in fileNameList:
        filesize = filesize + getFileSize(filename) + " "
    print("send filesize : " + filesize)
    s.send(filesize.encode())

    #wait ready sign
    ready = s.recv(1024)
    if ready.decode() == "ready":
        print("ready")
        count = 0
        while count < len(fileNameList):
            print(fileNameList[count] + " sending")
            with open("data/%s" %fileNameList[count], 'rb') as f:
                data = f.read(1024)
                #print(data)
                while data:
                    s.send(data)
                    data = f.read(1024)
                f.close()
            count = count + 1

    print("finish")
    s.close()

if __name__=="__main__":
    while True:
        send()
