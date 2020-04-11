import serial
import RPi.GPIO as GPIO
import os, time
import numpy as np

#############Save Data Function ################
def dataSave(DataString):
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
        np.savetxt("SeisRecord",DataArray, delimiter=',')
            
           
    print(DataArray)

    
GPIO.setmode(GPIO.BOARD)
port = serial.Serial("/dev/ttyS0",baudrate=115200,timeout=.01)
DataString=''


for i in range (0,100):
        try:
            port.write(str.encode('A'))
            rcv = port.read(50)
            DataString+=rcv.decode() #DataString is an object that contains all recorded data
        except:
            dataSave(DataString)
            break
    
                
print(DataString)
dataSave(DataString)    
    




