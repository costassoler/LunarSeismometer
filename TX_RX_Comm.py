from imports import *

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
    np.savez("SeisRecord.npz",DataArray, delimiter=',')            

def Run_TXRX():
    GPIO.setmode(GPIO.BOARD)
    port = serial.Serial("/dev/ttyS0",baudrate=115200,timeout=1)
    n=0
    port.write(str.encode('A'))
    print("wrote")
    while True:

        
        try:
            port.write(str.encode('A'))
            rcv = port.read_until(b'*')
            print(rcv)
            DataString+=rcv.decode() #DataString is an object that contains all recorded data
            
            
        except:
            
            continue
    
def Stream_TXRX():
    GPIO.setmode(GPIO.BOARD)
    port = serial.Serial("/dev/ttyS0",baudrate=BAUD_RATE,timeout=10)
   
    #send start signal
    port.write(str.encode('A'))
    print("worked")

    while True:
        #try:
        chunkString = port.read_until(b'*')
        chunk = chunkData(chunkString)
        chunk.print()
        
        
def Display_TXRX():
    GPIO.setmode(GPIO.BOARD)
    port = serial.Serial("/dev/ttyS0",baudrate=BAUD_RATE,timeout=10)
   
    #send start signal
    port.write(str.encode('A'))
    print("worked")

    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    n=0
    
 
    while True:
        #try:
        #
        try:
            ax.clear()
            ax.set_aspect(3)
            chunkString = port.read_until(b'*')
            chunk = chunkData(chunkString)
            #chunk.print()
            x,y = chunk.coords()
            line1 = ax.plot(x,y,'b-')
            plt.ylim(-100,100)
            fig.canvas.draw()
            
        except KeyboardInterrupt:
            break
        except:
            continue
        
        
        
class chunkData: # struct for data chunk
    def __init__(self,chunkString, chunkSize = CHUNK_SIZE):
        self.timeStamps, self.values = self.parse(chunkString,chunkSize)   
  
    def append(self, chunkString, chunkSize = CHUNK_SIZE):
        tmp = self.parse(chunkString,chunkSize)
        self.timeStamps.append(tmp[0])
        self.values.append(tmp[1])

    def print(self):
        for ind, timeStamp in enumerate(self.timeStamps):
            print('ts:', timeStamp, 'val:', self.values[ind]) # print human readable        
  
    def parse(self,chunkString,chunkSize):
        samples    = chunkString.decode()[:-1].split(',')
        timeStamps = np.zeros(chunkSize) # preallocate
        values     = np.zeros(chunkSize)
               
        for ind, sample in enumerate(samples): # probably wont work, need to deal with * character other errors?
            try:
                tmp             = sample.split(":")
                timeStamps[ind] = np.float(tmp[0])
                values[ind]     = np.float(tmp[1])
            except:
                continue
                
        return (timeStamps,values)
    
    def coords(self):
        x = self.timeStamps
        y = self.values
    
        return x,y
        

        
      


