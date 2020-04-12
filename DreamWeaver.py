import threading
import time

DataString=''
def RefreshGraph():
    global DataString
    while True:
        try:
            x = np.load('SeisRecord')
            print(x.files)
        except:
            print('oops')

def dataSave():
    global DataString
    Data = DataString.split(",")
    rows = int(len(Data)//2+1)

    DataArray = np.zeros((rows,2))
    
    for j in range(0,len(Data)):  
        row = j//2
        col = j%2
        if (Data[j].find("ts: ")==0):
            #print(float(Data[j].replace('ts: ','')))
            DataArray[row,col] = float(Data[j].replace('ts: ',''))
        if (Data[j].find("d:")==0):
            DataArray[row,col] = float(Data[j].replace('d: ',''))
    np.savez("SeisRecord.npz",DataArray, delimiter=',')
            

def Run_TXRX():
    GPIO.setmode(GPIO.BOARD)
    port = serial.Serial("/dev/ttyS0",baudrate=115200,timeout=.01)
    global DataString
    DataString=''
    n=0
    while True:

        try:
            port.write(str.encode('A'))
            rcv = port.read(50)
            DataString+=rcv.decode() #DataString is an object that contains all recorded data
            n+=1
            if(n%1000==0):
                DataCheck=DataString
                DataString=''
                dataSave(DataString)
        except:
            dataSave(DataString)
            break
'''
D=0
def do_something():
    print("sleeping 1 second")
    time.sleep(1)
    print("Done Sleeping")
    
def Forever_Loop():
    global D
    while True:
        try:
            D+=1
            if(D==100):
                D=0
            print('D:',D)
        except:
            break
        
def Math_Loop():
    global D
    while True:
        try:
            y = 2*D
            print('y:',y)
        except:
            break
#Create two threads below:

t1=threading.Thread(target=Forever_Loop)
t2=threading.Thread(target=Math_Loop)
'''
t1 = threading.Thread(target = Run_TXRX)
t2 = threading.Thread(target = RefreshGraph)

t1.start()
t2.start()

t1.join()
t2.join()




