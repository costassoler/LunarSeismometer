# quick stuff to write raw int32 arrays to file
# better pass np arrays of int32 motherfucker

import numpy as np
import os

class file:
    def __init__(self,fileName):
        if True:
            self.file = open(fileName, 'wb')
        else:
            print('Creating File Failed')
            return None
    def write(self,data): # assumes you were smart and passed something thats the right size
        self.file.write(data.reshape(data.shape[0] * data.shape[1]).tobytes())
    def close(self):
        self.file.close()

def load(fileName, channels): 
    return np.frombuffer(open(fileName,'rb').read(),dtype = np.int32).reshape(-1,channels)


