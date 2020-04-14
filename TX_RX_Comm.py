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
            print(rcv)
            if(n%1000==0):
                DataCheck=DataString
                DataString=''
                dataSave(DataString)
        except:
            dataSave(DataString)
            break
    
def Stream_TXRX():
    GPIO.setmode(GPIO.BOARD)
    port = serial.Serial("/dev/ttyS0",baudrate=BAUD_RATE,timeout=None)
   
  #send start signal
    port.write(str.encode('A'))
    chunkString = port.read(50).decode('utf-8')
    chunk = chunkData.parse(chunkString)
    print("worked")
 
    while True:
        chunkString = port.read(50).decode('utf-8')
        chunk = chunkData.parse(chunkString)
        print(chunk)
        '''    
        except:
            print("Error in reading Data")
            break
            '''
       


class chunkData: # struct for data chunk
  def __init__(self,chunkString, chunkSize = CHUNK_SIZE):
                self.timeStamps, self.samples = self.parse(chunkString,chunkSize)   
  
  def append(self, chunkString, chunkSize = CHUNK_SIZE):
                tmp = self.parse(chunkString,chunkSize)
                self.timeStamps.append(tmp[0])
                self.values.append(tmp[1])

<<<<<<< HEAD
  def print(self):
                for ind, timeStamp in enumerate(self.timeStamps):
                        print('ts:', timeStamp, 'val:', self.values[enumerate]) # print human readable        
  
  def parse(chunkString):
                samples = np.array(chunkString.split(','))
                chunkSize = samples.shape
                timeStamps = np.zeros(chunkSize) # preallocate
                values = np.zeros(chunkSize)
                
                for ind in range(0,chunkSize[0]): # probably wont work, need to deal with * character other errors?
                    try:
                        tmp = samples[ind].split(":")
                        timeStamps[ind] = np.float(tmp[0])
                        values[ind] = np.float(tmp[1])
                    except:
                        continue
                
                return (timeStamps,values) 
      
=======
	def print(self):
		for ind, timeStamp in enumerate(self.timeStamps):
			print('ts:', timeStamp, 'val:', self.values[enumerate]) # print human readable				
	
	def parse(chunkString,chunkSize = CHUNK_SIZE):
		timeStamps = values = np.zeros(chunkSize) # preallocate
		samples = chunkString[:-1].split(",")
		for ind, sample in enumerate(samples): 
			tmp	= sample.split(":")
			timeStamps[ind] = np.float(tmp[0])
			values[ind]     = np.float(tmp[1])
		return (timeStamps,values)	
>>>>>>> 85ac0aa561cd4a310ec6c6c0272de16ff6233dcd


