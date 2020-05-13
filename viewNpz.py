import numpy as np
import matplotlib.pyplot as plt
import datetime
import time

Data = np.load("StockRecording2020_5_12_19_1.npz")
UnixStart = Data["times"][0]
millisCorrect = Data["times"][1]
millis = Data["times"][2:]
deltas = millis-millisCorrect
unixTimestamps = (deltas/1000)+UnixStart
print(millis)
times = [datetime.datetime.fromtimestamp(ts) for ts in unixTimestamps]
print(times)
