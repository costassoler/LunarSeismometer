from imports import *

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

# startup prep
GPIO.setmode(GPIO.BOARD)
port = serial.Serial("/dev/ttyS0",baudrate=BAUD_RATE,timeout=10)
   
#send start signal 
port.write(str.encode('A'))
print("Start Command Sent")

#get current time 
startTime = datetime.datetime.now()
fileName  = 'recording' + str(startTime.year) + '_' + str(startTime.month) + '_' + str(startTime.day)+ '_' + str(startTime.hour)+'_'+str(startTime.second)

# open file
startSignal = 0

np.savez(fileName,signals=startSignal,times=startTime)

#setup graph:
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

# the main loop:
while True:
    try:
        chunkString = port.read_until(b'*')
        chunk = chunkData(chunkString)
    
        #collects new data:
        signal=chunk.values
        time=chunk.timeStamps

        #Plots newest data:
        ax.clear()
        ax.set_aspect(0.2)
        
            
        x,y = chunk.coords()
        line1 = ax.plot(x/1000,y*5/1023,'b-')
        plt.ylim(0,5)
        plt.xlabel("Time Since Start (seconds)")
        plt.ylabel("Signal (Volts)")
        fig.canvas.draw()
        
        #adds new data to npz file
        Data=np.load(fileName+".npz")
        signals = Data["signals"]
        times = Data["times"]

        
        
        signals=np.append(signals,signal)
        print(signals)
        times = np.append(times, time)

        np.savez(fileName,signals=signals, times=times)

        n=0
    
    except:
        print("Error!")
        n+=1
        if (n==10):
            break
    

     
    


    





