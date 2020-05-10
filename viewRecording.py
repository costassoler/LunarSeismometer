from imports import *

# get filename from argument
fileName = sys.argv[1]

# load file data
wavFile = wave.open(fileName,mode='rb')
n = wavFile.getnframes()
bytesData = wavFile.readframes(n)
int16Data = np.frombuffer(bytesData,dtype = np.int16)

fig = plt.figure()
fig.plot(int16Data) 

