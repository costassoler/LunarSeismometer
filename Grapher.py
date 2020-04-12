import matplotlib.pyplot as plt
import numpy as np
import csv
import matplotlib.animation as animation
from matplotlib import style
from TX_RX_Transceiver import *
#print (DataString)
Estyle.use('fivethirtyeight')
#fig=plt.figure()
#ax1=fig.addsubplot(1,1,1)
'''
def animate():
    graph_data=np.load('SeisRecord')
    x=graph_data
    print(x)
'''
def RefreshGraph():
    global DataString
    while True:
        try:
            x = np.load('SeisRecord')
            print(x.files)
        except:
            print('oops')
