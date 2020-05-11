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
fileName  = 'recording' + str(startTime.year) + '_' + str(startTime.month) + '_' + str(startTime.day)+ '_' + str(startTime.hour)

# open file
wavFile = wave.open(fileName, mode = 'wb')

wavFile.setnchannels(1)    # mono channel
wavFile.setframerate(4000) # 4000 framerate upscale 1000 times 
wavFile.setsampwidth(2)    # 16 bit audio

# the main loop:
while True:
    try:
        chunkString = port.read_until(b'*')
        chunk = chunkData(chunkString)
    
        #0 - 1023 V = 2 ** 10 -> 16 bit
        wavFile.writeframes(np.int16((chunk.values / 1024) * 2 ** 16).tobytes())
    
    except:
        print("Error!")
    

     
    


    





