import sys
import intByteWrite as ibw
from matplotlib import pyplot as plt

# get filename from argument
fileName = sys.argv[1]

# load file data
fileData = ibw.load(fileName,channels=2)

print(fileData[:100,:])

plt.figure()
plt.plot(fileData[:7 *60 * 60 * 40,0],fileData[:7 * 60 * 60 * 40,1]) 
plt.show()
