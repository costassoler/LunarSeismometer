from imports import *

#############Save Data Function ################
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
    
def Stream_TXRX():
    GPIO.setmode(GPIO.BOARD)
    port = serial.Serial("/dev/ttyS0",baudrate=115200,timeout=.01)
   
	#send start signal
    port.write(str.encode('A'))
 
    while True:

        try:
            rcv = port.read(50)
            print(rcv) #DataString is an object that contains all recorded data
            
        except:
            print("Error in reading Data")
            break                
  
