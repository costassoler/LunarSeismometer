from imports import *
import time
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
UnixStart = time.time()
startTime = datetime.datetime.utcnow()
fileName  = 'StockRecording' + str(startTime.year) + '_' + str(startTime.month) + '_' + str(startTime.day)+ '_' + str(startTime.hour)+'_'+str(startTime.minute)

# open file
startSignal = 0

np.savez(fileName,signals=startSignal,times=UnixStart)

#setup graph:
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
sigPrev1 = 0
timePrev1 = 0
sigPrev2 = 0
timePrev2=0
sigPrev3 = 0
timePrev3 = 0


# the main loop:
n=0
err=0
firstTstamp = 0
while True:
    try:
        
        chunkString = port.read_until(b'*')
        chunk = chunkData(chunkString)
    
        #collects new data:
        signal=chunk.values
        time=chunk.timeStamps
        

        #Plots newest data:
        ax.clear()
        ax.set_aspect(0.75)
        
            
        x,y = chunk.coords()
        ax.plot(timePrev3/1000,sigPrev3*5/1023,'b-')
        ax.plot(timePrev2/1000,sigPrev2*5/1023,'b-')
        ax.plot(timePrev1/1000,sigPrev1*5/1023,'b-')
        ax.plot(x/1000,y*5/1023,'b-')
        #line2=ax.plot
        plt.ylim(0,5)
        plt.xlabel("Time Since Start (seconds)")
        plt.ylabel("Signal (Volts)")
        fig.canvas.draw()

        timePrev3 = timePrev2
        sigPrev3 = sigPrev2

        timePrev2 = timePrev1
        sigPrev2 = sigPrev1

        timePrev1 = x
        sigPrev1 = y

        
        #adds new data to npz file
        Data=np.load(fileName+".npz")
        signals = Data["signals"]
        times = Data["times"]

        
        
        signals=np.append(signals,signal)
        
        times = np.append(times, time)

        np.savez(fileName,signals=signals, times=times)

        n+=1
        if (n%100==0):
            np.savez("Backup"+fileName,signals=signals,times=times)
            
        err=0
    
    except:
        print("Error!")
        err+=1
        if (err==50):
            break
    

     
    


    





