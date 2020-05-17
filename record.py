from imports import *
import time
class chunkData: # struct for data chunk
    def __init__(self,chunkString, chunkSize = CHUNK_SIZE):
        self.data = self.parse(chunkString,chunkSize)   
  
    def append(self, chunkString, chunkSize = CHUNK_SIZE):
        tmp = self.parse(chunkString,chunkSize)
        self.data.append(tmp)

    def parse(self,chunkString,chunkSize):
        samples    = chunkString.decode()[:-1].split(',')
        data       = np.zeros((chunkSize,2),dtype=np.int32)
        for ind, sample in enumerate(samples): 
            try:
                tmp             = sample.split(":")
                data[ind,0] = np.int32(tmp[0]) # time stamps
                data[ind,1] = np.int32(tmp[1]) # values
            except:
                continue
                
        return data
    
    def print(self): # we dont really use print anymore heres a quick shitty version
        print(self.data) #if we need it later :)

    def coords(self):
        x = self.data[:,0]
        y = self.data[:,1]
    
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
writeFile = ibw.file(fileName)

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

        writeFile.write(chunk.data)  
    
    except:
        print("Error!")
        err+=1
        if (err==50):
            break
