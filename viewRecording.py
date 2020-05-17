from imports import *

# get filename from argument
fileName = sys.argv[1]

# load file data
fileData = ibw.load(fileName,channels=2)

plt.plot(fileData[0],fileData[1]) 
plt.show()
