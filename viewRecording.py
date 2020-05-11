from imports import *

# get filename from argument
fileName = sys.argv[1]

# load file data
wavFile = wave.open(fileName,mode='rb')
n = wavFile.getnframes()
bytesData = wavFile.readframes(n)
int16Data = np.frombuffer(bytesData,dtype = np.int16)


plt.plot(int16Data) 
plt.show()
